import sqlite3
from flet import *
import datetime
from utils.navbar import create_navbar
from const import *


BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"


class Report_Income(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
    
    def build(self):
        def fetch_data_from_db(
            year=datetime.datetime.now().year, month=datetime.datetime.now().month
        ):
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()

            # Extract the year and month from the input month
            # year = datetime.datetime.now().year

            # Build the SQL query to filter by year and month
            sql_query = (
                "SELECT * FROM financial_transaction WHERE strftime('%Y-%m', date) = ?"
            )

            # Execute the query with the provided month and year
            cursor.execute(sql_query, (f"{year:04}-{month:02}",))

            records = cursor.fetchall()
            result = [row for row in records]
            conn.close()
            return result

        global current_month, current_year, data
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year
        data = fetch_data_from_db(year=current_year, month=current_month)
        # print(f"data is: {data}")

        def update_views():
            outcome_income_expenses = create_outcome_income_expenses(data)
            piechart = create_piechart(data)
            statistics = create_statistics(data)
            report_income_page_child_container.content.controls[2] = outcome_income_expenses
            report_income_page_child_container.content.controls[4] = piechart
            report_income_page.controls[0].content.controls[1]  = statistics
            report_income_page_child_container.update()
            report_income_page.update()
            self.page.update()

        def create_header():
            
            # Create one text buttons.
            button_1 = Text("Báo cáo", color="white")

            # Add the buttons to the page.
            header = Row(
                alignment="spaceBetween",
                controls=[
                    Row(
                        controls=[
                            button_1,
                            # button_2,
                        ]
                    ),
                ],
            )
            return header

        def create_date():
            def update_date_display():
                # Định dạng tháng với số 0 trước nếu nhỏ hơn 10
                formatted_month = str(current_month).zfill(2)
                formatted_year = str(current_year).zfill(4)
                # Cập nhật ngày tháng trên giao diện
                date_header.controls[0].value = f"{formatted_month}/{formatted_year}"
                date_header.update()

            def get_next_month():
                global current_month, current_year, data
                # Tăng tháng
                current_month += 1

                # Nếu tháng là 13, thì tăng năm và đặt lại tháng về 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1
                data = fetch_data_from_db(current_year, current_month)
                # print(data)
                update_date_display()
                update_views()

            def get_prev_month():
                global current_month, current_year, data
                # Giảm tháng
                current_month -= 1

                # Nếu tháng là 0, thì giảm năm và đặt lại tháng về 12
                if current_month < 1:
                    current_month = 12
                    current_year -= 1
                data = fetch_data_from_db(current_year, current_month)
                # print(data)
                update_date_display()
                update_views()

            # Create a row to represent the date header.
            date_header = Row(
                alignment="spaceBetween",
                controls=[
                    # Create a text widget to display the month/year.
                    Text(datetime.date.today().strftime("%m/%Y"), color="white"),
                    # Create a row to contain the arrow buttons.
                    Row(
                        controls=[
                            # Create an icon button for the previous arrow.
                            IconButton(
                                icons.ARROW_LEFT,
                                icon_color="white",
                                on_click=lambda event: get_prev_month(),
                            ),
                            # Create an icon button for the next arrow.
                            IconButton(
                                icons.ARROW_RIGHT,
                                icon_color="white",
                                on_click=lambda event: get_next_month(),
                            ),
                        ]
                    ),
                ],
            )

            return date_header

        def create_outcome_income_expenses(month_data):
            # Create three text buttons.
            button_1 = Text(
                "Chi tiêu",color="White"
            )
            button_2 = Text(
                "Thu nhập", color="White"
            )
            button_3 = Text(
                "Thu chi", color="White"
            )
            # Calculate and format the total expense and income from the data
            total_expense = (int)(sum(row[3] for row in month_data if row[5] == "Tiền chi"))
            total_income = (int)(sum(row[3] for row in month_data if row[5] == "Tiền thu"))
            container_width = self.page.width- 60
            outcome_income_expenses = Column(
                controls=[
                    Row(
                        alignment="spaceBetween",
                        controls=[
                            Container(
                                # width=170,
                                # height=30,
                                width=container_width/2,
                                height=30,
                                border_radius=5,
                                bgcolor=GREY_COLOR,
                                padding=1,
                                content=Row(
                                    alignment="spaceBetween",
                                    controls=[
                                        button_1,
                                        Text(f"{'{:,}'.format(total_expense)} đ", color="white"),
                                    ],
                                ),
                            ),
                            Container(
                                # width=170,
                                # height=30,
                                width=container_width/2,
                                height=30,
                                border_radius=5,
                                bgcolor=GREY_COLOR,
                                padding=1,
                                content=Row(
                                    alignment="spaceBetween",
                                    controls=[
                                        button_2,
                                        Text(f"{'{:,}'.format(total_income)} đ", color="white"),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    Row(
                        controls=[
                            Container(
                                # width=340,
                                # height=30,
                                width=container_width,
                                height=30,
                                border_radius=5,
                                bgcolor=GREY_COLOR,
                                padding=1,
                                content=Row(
                                    alignment="spaceBetween",
                                    controls=[
                                        button_3,
                                        Text(f"{'{:,}'.format(total_income-total_expense)} đ", color="white"),
                                    ],
                                ),
                            )
                        ]
                    )

                ]
            )
            return outcome_income_expenses
        
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
                    self.page.go("/report_outcome"),
                ),
            )
            button_2 = TextButton(
                text="Thu nhập",
                style=ButtonStyle(color="White", bgcolor=PINK),
                on_click=lambda e: (
                    change_button_colors(button_2, button_1),
                    self.page.go("/report_income"),
                ),
            )
            container_width = self.page.width- 60
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

        def create_piechart(month_data):
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
            total_income = sum(row[3] for row in month_data if row[5] == "Tiền thu")
            if total_income != 0:
                tienluong = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Lương")
                    / total_income
                    * 100
                )
                phucap = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Phụ cấp")
                    / total_income
                    * 100
                )
                thuong = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Thưởng")
                    / total_income
                    * 100
                )
                dautu = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Đầu tư")
                    / total_income
                    * 100
                )
                lamthem = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Làm thêm")
                    / total_income
                    * 100
                )
                khac = "{:.2f}".format(
                    sum(
                        row[3]
                        for row in month_data
                        if row[4] == "Khác" and row[5] == "Tiền thu"
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
                        title="Khác" + str(f"{khac}") + "%",
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

        def create_statistics(month_data):
            statistics= ListView(
                height=65,
                width=340,
                # scroll='auto',
                spacing=1,
            )
            tienluong = (int)(sum(row[3] for row in month_data if row[4] == "Lương"))
            phucap = (int)(sum(row[3] for row in month_data if row[4] == "Phụ cấp"))
            thuong = (int)(sum(row[3] for row in month_data if row[4] == "Thưởng"))
            dautu = (int)(sum(row[3] for row in month_data if row[4] == "Đầu tư"))
            lamthem = (int)(sum(row[3] for row in month_data if row[4] == "Làm thêm"))
            khac = (int)(sum(
                row[3]
                for row in month_data
                if row[4] == "Khác" and row[5] == "Tiền thu"
            ))

            def create_statistics_row(category, icon, text, icon_color):
                statistics_row = Container(
                    width=340,
                    height=21,
                    border_radius=5,
                    bgcolor=GREY_COLOR,
                    padding=1,
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
        date_row = create_date()
        outcome_income_expenses = create_outcome_income_expenses(data)
        label = create_chart_label()
        piechart = create_piechart(data)
        statistics = create_statistics(data)
        navbar = create_navbar(self.page, 2)

        report_income_page_child_container = Container(
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                controls=[
                    header,
                    date_row,
                    outcome_income_expenses,
                    label,
                    piechart,
                ]
            ),
        )
        
        def update_size(e):
            report_income_page.controls[0].height = self.page.height
            report_income_page.controls[0].width = self.page.width
            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")
            report_income_page.update()
        self.page.on_resize = update_size

        report_income_page = ResponsiveRow(
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
                            report_income_page_child_container,
                            statistics,
                            navbar,
                        ],
                    ),
                )
            ]
        )

        return report_income_page
