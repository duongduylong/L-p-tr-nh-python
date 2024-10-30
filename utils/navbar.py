from flet import *
from const import *


def create_navbar(page: Page, selected_index):
    def change_tab(e):
        my_index = e.control.selected_index
        if my_index == 0:
            page.go("/")
        elif my_index == 1:
            page.go("/calendar")
        elif my_index == 2:
            page.go("/report_outcome")
        elif my_index == 3:
            page.go("/other")

        page.update()

    nav_bar = NavigationBar(
        destinations=[
            NavigationDestination(
                icon=icons.EDIT,
                label="Nhập vào",
            ),
            NavigationDestination(
                icon=icons.CALENDAR_MONTH,
                label="Lịch",
            ),
            NavigationDestination(
                icon=icons.PIE_CHART,
                label="Báo cáo",
            ),
            NavigationDestination(
                icon=icons.MORE_HORIZ,
                label="Khác",
            ),
        ],
        bgcolor=BG_COLOR,
        selected_index=selected_index,
        on_change=change_tab,
    )

    return nav_bar
