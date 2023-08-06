import time

from gdshoplib.apps.crm.on_request import OnRequestTable
from gdshoplib.apps.product import Product
from gdshoplib.core.settings import CRMSettings
from gdshoplib.services.notion.database import Database
from gdshoplib.services.notion.page import Page


class Order(Page):
    SETTINGS = CRMSettings()

    def __init__(self, *args, **kwargs):
        self._on_request = None
        self._products = None

        super(Order, self).__init__(*args, **kwargs)

    @classmethod
    def get(cls, sku):
        page = [
            page
            for page in Database(cls.SETTINGS.CRM_DB).pages(
                params={
                    "filter": {
                        "property": "ID заказа",
                        "rich_text": {
                            "equals": sku,
                        },
                    }
                }
            )
        ]
        if not page:
            return
        if len(page) > 1:
            raise OrderIDDuplicate

        page = page[0]

        return cls(page["id"], notion=page.notion, parent=page.parent)

    @classmethod
    def query(cls, filter=None, params=None, notion=None):
        for page in Database(cls.SETTINGS.CRM_DB, notion=notion).pages(
            filter=filter, params=params
        ):
            yield cls(page["id"], notion=page.notion, parent=page.parent)

    @property
    def on_request(self):
        if not self._on_request:
            self._on_request = OnRequestTable(
                [block for block in self.blocks(filter={"type": "table_row"})],
                notion=self.notion,
                parent=self,
            )

        return self._on_request

    @property
    def products(self):
        if not self._products:
            self._products = [Product(page.id) for page in self.products_field]
        return self._products

    @property
    def price(self):
        result = self.on_request.price()
        for product in self.products:
            result += product.price.now
        return result

    @property
    def profit(self):
        base_price = self.on_request.price("gross")
        for product in self.products:
            base_price += product.price.gross
        return self.price - base_price

    def generate_id(self):
        return f"{self.platform.key.lower()}.{int(time.time())}"

    @property
    def price_description(self):
        ...

    def set_id(self):
        # Установить ID
        self.notion.update_prop(
            self.id,
            params={
                "properties": {"ID заказа": [{"text": {"content": self.generate_id()}}]}
            },
        )

    def set_price_description(self):
        # Установка описания расчетов цены
        self.notion.update_prop(
            self.id,
            params={
                "properties": {
                    "Расчеты": [{"text": {"content": self.price_description or ""}}]
                }
            },
        )

    def set_price(self):
        # Установка итоговой цены
        self.notion.update_prop(
            self.id,
            params={"properties": {"Итого": {"number": self.price}}},
        )

    def set_profit(self):
        # Установка итоговой цены
        self.notion.update_prop(
            self.id,
            params={"properties": {"Прибыль": {"number": self.profit}}},
        )

    def load_tasks(self):
        # Загрузка задач в CRM из источников
        ...

    @classmethod
    def update(cls):
        # Обновление карточки Order
        for order in cls.query():
            order.on_request.update()
            order.set_price()
            order.set_profit()
            order.set_price_description()
            if not order.order_id:
                order.set_id()

    def notification(self):
        # Отправка уведомлений
        ...


class OrderIDDuplicate(Exception):
    ...
