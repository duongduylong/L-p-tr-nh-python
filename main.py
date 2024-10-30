from flet import *
from const import *
from views import views_handler


# main
def main(page: Page):
    def route_change(route):
        page.views.clear()
        page.views.append(views_handler(page)[page.route])

    page.on_route_change = route_change

    page.go("/")


app(target=main)
