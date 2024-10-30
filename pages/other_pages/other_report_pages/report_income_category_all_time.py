import sqlite3
from flet import *
from const import *


class Report_Income_Category_All_Time(UserControl):
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

        global data
        data = fetch_data_from_db()

        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = Text("Toàn thời gian", color="white")

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1)

            # Add the buttons to the page.
            header = Row(
                alignment="spaceBetween",
                controls=[
                    IconButton(
                        icons.ARROW_BACK,
                        icon_color="white",
                        on_click=lambda e: self.page.go("/other"),
                    ),
                    button_1,
                    IconButton(icons.ACCESS_TIME, icon_color="white"),
                ],
            )
            return header

        def create_chart_label():
            def change_button_colors(button_1: TextButton, button_2: TextButton):
                button_1.style.bgcolor = PINK
                button_2.style.bgcolor = GREY_COLOR
                label.update()

            # Create two text buttons.
            button_1 = TextButton(
                text="Chi tiêu",
                style=ButtonStyle(color="white"),
                on_click=lambda e: (
                    change_button_colors(button_1, button_2),
                    self.page.go("/report_outcome_category_all_time"),
                ),
            )
            button_2 = TextButton(
                text="Thu nhập",
                style=ButtonStyle(color="White", bgcolor=PINK),
                on_click=lambda e: (
                    change_button_colors(button_2, button_1),
                    self.page.go("/report_income_category_all_time"),
                ),
            )
            container_width = self.page.width - 60
            label = Column(
                controls=[
                    Row(
                        alignment="spaceAround",
                        controls=[
                            button_1,
                            button_2,
                        ],
                    ),
                    Container(
                        width=container_width,
                        height=5,
                        border_radius=5,
                        bgcolor="white12",
                        padding=padding.only(left=container_width/2),
                        content=Container(
                            bgcolor=PINK,
                        ),
                    ),
                ]
            )

            return label

        def create_piechart(data):
            normal_radius = 50
            hover_radius = 60
            normal_title_style = TextStyle(
                size=10, color=colors.WHITE, weight=FontWeight.BOLD
            )
            normal_title_style2 = TextStyle(
                size=9, color=colors.WHITE, weight=FontWeight.BOLD
            )
            hover_title_style = TextStyle(
                size=10,
                color=colors.WHITE,
                weight=FontWeight.BOLD,
                shadow=BoxShadow(blur_radius=2, color=colors.BLACK54),
            )
            # total_expense = sum(row[3] for row in month_data if row[5] == "Tiền chi")
            total_income = sum(row[3] for row in data if row[5] == "Tiền thu")
            if total_income != 0:
                tienluong = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Lương")
                    / total_income
                    * 100
                )
                phucap = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Phụ cấp")
                    / total_income
                    * 100
                )
                thuong = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Thưởng")
                    / total_income
                    * 100
                )
                dautu = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Đầu tư")
                    / total_income
                    * 100
                )
                lamthem = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Làm thêm")
                    / total_income
                    * 100
                )
                khac = "{:.2f}".format(
                    sum(
                        row[3]
                        for row in data
                        if (row[4] == "Khác" and row[5] == "Tiền thu")
                    )
                    / total_income
                    * 100
                )

            else:
                tienluong = phucap = thuong = dautu = lamthem = khac = "0.00"

            def on_chart_event(e: PieChartEvent):
                for idx, section in enumerate(chart.sections):
                    if idx == e.section_index:
                        section.radius = hover_radius
                        section.title_style = hover_title_style
                    else:
                        section.radius = normal_radius
                        section.title_style = normal_title_style
                chart.update()

            chart = PieChart(
                sections=[
                    PieChartSection(
                        tienluong,
                        title="Tiền lương" + str(f"{tienluong}") + "%",
                        title_style=normal_title_style2,
                        color=colors.BLUE,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        phucap,
                        title="Phụ cấp" + str(f"{phucap}") + "%",
                        title_style=normal_title_style2,
                        color=colors.YELLOW,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        thuong,
                        title="Thưởng" + str(f"{thuong}") + "%",
                        title_style=normal_title_style2,
                        color=colors.PURPLE,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        dautu,
                        title="Đầu tư" + str(f"{dautu}") + "%",
                        title_style=normal_title_style2,
                        color=colors.GREEN,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        lamthem,
                        title="Làm thêm" + str(f"{lamthem}") + "%",
                        title_style=normal_title_style2,
                        color=colors.RED,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        khac,
                        title="Khác1" + str(f"{khac}") + "%",
                        title_style=normal_title_style2,
                        color=colors.BLACK,
                        radius=normal_radius,
                    ),
                ],
                sections_space=0,
                center_space_radius=70,
                # size=size(150, 150),
                on_chart_event=on_chart_event,
                expand=False,
            )
            return chart

        def create_statistics(data):
            statistics = ListView(
                height=150,
                width=340,
                # scroll='auto',
                spacing=1,
            )
            tienluong = (int)(sum(row[3] for row in data if row[4] == "Lương"))
            phucap = (int)(sum(row[3] for row in data if row[4] == "Phụ cấp"))
            thuong = (int)(sum(row[3] for row in data if row[4] == "Thưởng"))
            dautu = (int)(sum(row[3] for row in data if row[4] == "Đầu tư"))
            lamthem = (int)(sum(row[3] for row in data if row[4] == "Làm thêm"))
            khac = (int)(sum(
                row[3] for row in data if row[4] == "Khác" and row[5] == "Tiền thu"
            ))

            def create_statistics_row(category, icon, text, icon_color):
                statistics_row = Container(
                    width=340,
                    height=35,
                    border_radius=5,
                    bgcolor=GREY_COLOR,
                    padding=5,
                    content=Row(
                        alignment="spaceBetween",
                        controls=[
                            Row(
                                alignment="start",
                                controls=[
                                    Icon(name=icon, color=icon_color),
                                    Text(text, color="white"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{'{:,}'.format(category)}", color="white"),
                                    Text("đ", color="white"),
                                ],
                            ),
                        ],
                    ),
                )
                return statistics_row

            statistics.controls.extend(
                [
                    create_statistics_row(
                        tienluong, icons.ACCOUNT_BALANCE_WALLET, "Tiền lương", "blue"
                    ),
                    create_statistics_row(phucap, icons.ATTACH_MONEY, "Phụ cấp", "yellow"),
                    create_statistics_row(thuong, icons.CARD_GIFTCARD, "Thưởng", "purple"),
                    create_statistics_row(dautu, icons.DIAMOND, "Đầu tư", "green"),
                    create_statistics_row(lamthem, icons.WORK, "Làm thêm", "red"),
                    create_statistics_row(khac, icons.QUESTION_MARK, "Khác", "black"),
                ]
            )

            return statistics

        header = create_header()
        label = create_chart_label()
        piechart = create_piechart(data)
        statistics = create_statistics(data)

        report_income_category_all_time_page_child_container = Container(
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                controls=[
                    header,
                    label,
                    piechart,
                ]
            ),
        )
        def update_size(e):
            report_income_category_all_time_page.controls[0].height = self.page.height
            report_income_category_all_time_page.controls[0].width = self.page.width

            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")

            report_income_category_all_time_page.update()

        self.page.on_resize = update_size

        report_income_category_all_time_page = ResponsiveRow(
            [
                Container(
                    width=self.page.width,
                    height=self.page.height,
                    border_radius=35,
                    bgcolor=BG_COLOR,
                    content=Column(
                        alignment="spaceBetween",
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            report_income_category_all_time_page_child_container,
                            statistics,
                        ],
                    ),
                )
            ]
        )

        return report_income_category_all_time_page
