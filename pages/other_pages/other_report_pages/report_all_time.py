import sqlite3
from flet import *
from const import *


class Report_All_Time(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db():
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            data = cursor.execute("""SELECT * FROM financial_transaction""")
            result = [row for row in data]
            conn.close()
            return result

        def create_header():
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            button_1 = Text("Báo cáo toàn kì", color="white")
            button_1.on_click = lambda event: change_button_colors(button_1)
            header = Row(
                spacing=10,
                alignment="spaceBetween",
                controls=[
                    IconButton(
                        icons.ARROW_BACK,
                        icon_color="white",
                        on_click=lambda e: self.page.go("/other"),
                    ),
                    button_1,
                    IconButton(icons.SEARCH, icon_color="white"),
                ],
            )
            return header

        def create_outcome_income_sum():
            data = fetch_data_from_db()
            # Create two text buttons.
            button_1 = Text("Chi tiêu", color="White")
            button_2 = Text("Thu nhập", color="White")
            button_3 = Text("Tổng", color="White")

            # Calculate and format the total expense and income from the data
            total_expense = (int)(sum(row[3] for row in data if row[5] == "Tiền chi"))
            total_income = (int)(sum(row[3] for row in data if row[5] == "Tiền thu"))

            outcome_income_sum = Column(
                alignment="spaceBetween",
                controls=[
                    Container(
                        padding=padding.only(30, 10, 30, 10),
                        border=border.only(
                            bottom=border.BorderSide(0.5, "#3c3c3c"),
                            top=border.BorderSide(0.5, "#3c3c3c"),
                        ),
                        content=Row(
                            alignment="spaceBetween",
                            controls=[
                                button_1,
                                Text(f"{'{:,}'.format(total_expense)} đ", color="white"),
                            ],
                        ),
                    ),
                    Container(
                        padding=padding.only(30, 10, 30, 10),
                        border=border.only(
                            bottom=border.BorderSide(0.5, "#3c3c3c"),
                            top=border.BorderSide(0.5, "#3c3c3c"),
                        ),
                        content=Row(
                            alignment="spaceBetween",
                            controls=[
                                button_2,
                                Text(f"{'{:,}'.format(total_income)} đ", color="white"),
                            ],
                        ),
                    ),
                    Container(
                        padding=padding.only(30, 10, 30, 10),
                        border=border.only(
                            bottom=border.BorderSide(0.5, "#3c3c3c"),
                            top=border.BorderSide(0.5, "#3c3c3c"),
                        ),
                        content=Row(
                            alignment="spaceBetween",
                            controls=[
                                button_3,
                                Text(f"{'{:,}'.format(total_income-total_expense)} đ", color="white"),
                            ],
                        ),
                    ),
                ],
            )

            return outcome_income_sum

        header = create_header()
        outcome_income_sum = create_outcome_income_sum()

        report_all_time_page_child_container = Container(
            padding=padding.only(left=10, top=30, right=30),
            content=Column(
                controls=[
                    header,
                ]
            ),
        )
        def update_size(e):
            report_all_time_page.controls[0].height = self.page.height
            report_all_time_page.controls[0].width = self.page.width

            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")

            report_all_time_page.update()

        self.page.on_resize = update_size

        report_all_time_page = ResponsiveRow(
            [
                Container(
                    width=self.page.width,
                    height=self.page.height,
                    border_radius=35,
                    bgcolor=BG_COLOR,
                    content=Column(
                        controls=[
                            report_all_time_page_child_container,
                            outcome_income_sum,
                        ],
                    ),
                )
            ]
        )

        return report_all_time_page

