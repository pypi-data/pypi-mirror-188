import typer

from gdshoplib.apps.crm.orders import Order

app = typer.Typer()


@app.command()
def on_request_update():
    # Взять все заказы, в нужном статусе
    # Обновить позиции на заказ
    for order in Order.query():
        order.on_request.update()


@app.command()
def update():
    # Обновить расчеты заказов
    Order.update()


@app.command()
def notify():
    # Разослать уведомление для менеджеров из CRM
    ...
