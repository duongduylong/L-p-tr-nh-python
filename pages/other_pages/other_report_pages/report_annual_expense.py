import math
import sqlite3
from flet import *
import datetime
from const import *


class Report_During_The_Year_Expense(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db(year=datetime.datetime.now().year):
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            # Build the SQL query to filter by year and month
            sql_query = (
                "SELECT * FROM financial_transaction WHERE strftime('%Y', date) = ?"
            )
            # Execute the query with the provided month and year
            cursor.execute(sql_query, (f"{year}",))
            records = cursor.fetchall()
            result = [row for row in records]
            conn.close()
            return result

        global current_month, current_year, data
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year
        data = fetch_data_from_db(year=current_year)
        # data = fetch_data_from_db()

        def update_views():
            print("this is baocaotrongnam")
            print(data)
            # chitieu_thunhap_thuchi = create_chitieu_thunhap_thuchi(data)
            bieu_do_cot = create_barchart(data)
            thongke1 = create_statistics(data)
            # chitieu_thunhap_thuchi.update()
            # bieu_do_tron.update()
            # thongke1.update()
            # page_3_child_container.content.controls[2] = chitieu_thunhap_thuchi
            baocaotrongnam.controls[0].content.controls[3] = bieu_do_cot
            baocaotrongnam.controls[0].content.controls[4] = thongke1
            baocaotrongnam.update()
            self.page.update()

        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = Text("Báo cáo trong năm", color="white")

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

        def create_date():
            def update_date_display():
                # Định dạng tháng với số 0 trước nếu nhỏ hơn 10
                # formatted_month = str(current_month).zfill(2)
                # Cập nhật ngày tháng trên giao diện
                date_header.controls[0].value = f"{current_year}"
                date_header.update()

            def get_next_year():
                global current_year, data
                # Tăng tháng
                current_year += 1

                # Nếu tháng là 13, thì tăng năm và đặt lại tháng về 1
                # if current_month > 12:
                #     current_month = 1
                #     current_year += 1
                data = fetch_data_from_db(current_year)
                # print(data)
                update_date_display()
                update_views()

            def get_prev_year():
                global current_year, data
                # Giảm tháng
                current_year -= 1

                # Nếu tháng là 0, thì giảm năm và đặt lại tháng về 12
                # if current_month < 1:
                #     current_month = 12
                #     current_year -= 1
                data = fetch_data_from_db(current_year)
                # print(data)
                update_date_display()
                update_views()

            # Create a row to represent the date header.
            date_header = Row(
                alignment="spaceBetween",
                controls=[
                    # Create a text widget to display the month/year.
                    Text(datetime.date.today().strftime("%Y"), color="white"),
                    # Create a row to contain the arrow buttons.
                    Row(
                        controls=[
                            # Create an icon button for the previous arrow.
                            IconButton(
                                icons.ARROW_LEFT,
                                icon_color="white",
                                on_click=lambda event: get_prev_year(),
                            ),
                            # Create an icon button for the next arrow.
                            IconButton(
                                icons.ARROW_RIGHT,
                                icon_color="white",
                                on_click=lambda event: get_next_year(),
                            ),
                        ]
                    ),
                ],
            )

            return date_header

        def create_chart_label():
            def change_button_colors(button_1: TextButton, button_2: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                button_2.style.bgcolor = BG_COLOR
                # button_3.style.bgcolor = BLUE
                label.update()

            button_1 = TextButton(
                text="Chi tiêu",
                style=ButtonStyle(color="white", bgcolor=GREY_COLOR),
                on_click=lambda e: (
                    change_button_colors(button_1, button_2),
                    self.page.go("/report_annual_expense"),
                ),
            )
            button_2 = TextButton(
                text="Thu nhập",
                style=ButtonStyle(
                    color="white",
                ),
                on_click=lambda e: (
                    change_button_colors(button_2, button_1),
                    self.page.go("/report_annual_income"),
                ),
            )
            # button_3 = TextButton(
            #     text="Tổng", style=ButtonStyle(color="white", bgcolor=GREY_COLOR)
            # )
            container_width = self.page.width
            label = Column(
                alignment=MainAxisAlignment.START,
                controls=[
                    Row(
                        alignment="spaceAround",
                        controls=[
                            # Text('Chi tiêu'),
                            # Text('Thu nhập'),
                            button_1,
                            button_2,
                        ],
                    ),
                    Container(
                        width=container_width,
                        height=5,
                        border_radius=5,
                        bgcolor="white12",
                        # padding=padding.only(right=container_width/2),
                        # content=Container(
                        #     bgcolor=PINK,
                        # ),
                    ),
                ],
            )

            return label

        def create_barchart(data):
            total_expense = sum(row[3] for row in data if row[5] == "Tiền chi")
            total_income = sum(row[3] for row in data if row[5] == "Tiền thu")

            def create_money(x):
                month = "{:.2f}".format(
                    sum(
                        row[3]
                        for row in data
                        if int(row[1][5:7]) == x and row[5] == "Tiền chi"
                    )
                )
                return month

            month_max = 0
            for i in range(1, 12):
                if month_max < float(create_money(i)):
                    month_max = float(create_money(i))

            def round_up(num):
                if num < 100:
                    base = 10
                elif num < 1000:
                    base = 100
                elif num < 1000000:
                    base = 1000
                elif num < 100000000:
                    base = 1000000
                else:
                    base = 100000000

                return math.ceil(num / base) * base

            if total_expense != 0:
                thang1_expense = str(create_money(1))
                thang2_expense = str(create_money(2))
                thang3_expense = str(create_money(3))
                thang4_expense = str(create_money(4))
                thang5_expense = str(create_money(5))
                thang6_expense = str(create_money(6))
                thang7_expense = str(create_money(7))
                thang8_expense = str(create_money(8))
                thang9_expense = str(create_money(9))
                thang10_expense = str(create_money(10))
                thang11_expense = str(create_money(11))
                thang12_expense = str(create_money(12))
            else:
                thang1_expense = (
                    thang2_expense
                ) = (
                    thang3_expense
                ) = (
                    thang4_expense
                ) = (
                    thang5_expense
                ) = (
                    thang6_expense
                ) = (
                    thang7_expense
                ) = (
                    thang8_expense
                ) = (
                    thang9_expense
                ) = thang10_expense = thang11_expense = thang12_expense = "0.00"

            chart = BarChart(
                bar_groups=[
                    BarChartGroup(
                        x=0,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang1_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 1",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=1,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang2_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 2",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=2,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang3_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 3",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=3,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang4_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 4",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=4,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang5_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 5",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=5,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang6_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 6",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=6,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang7_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 7",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=7,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang8_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 8",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=8,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang9_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 9",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=9,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang10_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 10",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=10,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang11_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 11",
                                border_radius=0,
                            )
                        ],
                    ),
                    BarChartGroup(
                        x=11,
                        bar_rods=[
                            BarChartRod(
                                from_y=0,
                                to_y=f"{thang12_expense}",
                                width=10,
                                color=colors.BLUE,
                                tooltip="Tháng 12",
                                border_radius=0,
                            )
                        ],
                    ),
                ],
                border=border.all(1, colors.GREY_400),
                bottom_axis=ChartAxis(
                    labels=[
                        ChartAxisLabel(
                            value=0,
                            label=Container(Text("T1", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=1,
                            label=Container(Text("T2", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=2,
                            label=Container(Text("T3", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=3,
                            label=Container(Text("T4", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=4,
                            label=Container(Text("T5", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=5,
                            label=Container(Text("T6", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=6,
                            label=Container(Text("T7", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=7,
                            label=Container(Text("T8", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=8,
                            label=Container(Text("T9", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=9,
                            label=Container(Text("T10", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=10,
                            label=Container(Text("T11", color="white"), padding=2),
                        ),
                        ChartAxisLabel(
                            value=11,
                            label=Container(Text("T12", color="white"), padding=2),
                        ),
                    ],
                    labels_size=20,
                ),
                left_axis=ChartAxis(labels_size=45),
                horizontal_grid_lines=ChartGridLines(
                    color=colors.GREY_300, width=1, dash_pattern=[3, 3]
                ),
                tooltip_bgcolor=colors.with_opacity(0.5, colors.GREY_300),
                max_y=round_up(month_max),
                interactive=True,
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

            def create_money(x):
                money = (int)(
                    sum(
                        row[3]
                        for row in data
                        if int(row[1][5:7]) == x and row[5] == "Tiền chi"
                    )
                )
                return money

            thang1 = create_money(1)
            thang2 = create_money(2)
            thang3 = create_money(3)
            thang4 = create_money(4)
            thang5 = create_money(5)
            thang6 = create_money(6)
            thang7 = create_money(7)
            thang8 = create_money(8)
            thang9 = create_money(9)
            thang10 = create_money(10)
            thang11 = create_money(11)
            thang12 = create_money(12)

            def create_statistics_row(month, money):
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
                                    Text(month, color="white"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{'{:,}'.format(money)}", color="white"),
                                    Text("đ", color="white"),
                                ],
                            ),
                        ],
                    ),
                )
                return statistics_row

            statistics.controls.extend(
                [
                    create_statistics_row("Tháng 1", thang1),
                    create_statistics_row("Tháng 2", thang2),
                    create_statistics_row("Tháng 3", thang3),
                    create_statistics_row("Tháng 4", thang4),
                    create_statistics_row("Tháng 5", thang5),
                    create_statistics_row("Tháng 6", thang6),
                    create_statistics_row("Tháng 7", thang7),
                    create_statistics_row("Tháng 8", thang8),
                    create_statistics_row("Tháng 9", thang9),
                    create_statistics_row("Tháng 10", thang10),
                    create_statistics_row("Tháng 11", thang11),
                    create_statistics_row("Tháng 12", thang12),
                ]
            )

            return statistics

        header = create_header()
        date_row = create_date()
        label = create_chart_label()
        barchart = create_barchart(data)
        statistical = create_statistics(data)

        def update_size(e):
            baocaotrongnam.controls[0].height = self.page.height
            baocaotrongnam.controls[0].width = self.page.width

            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")

            baocaotrongnam.update()

        self.page.on_resize = update_size

        baocaotrongnam = ResponsiveRow(
            controls=[
                Container(
                    width=self.page.width,
                    height=self.page.height,
                    border_radius=35,
                    bgcolor=BG_COLOR,
                    padding=padding.only(top=30),
                    content=Column(
                        # alignment="spaceBetween",
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            header,
                            date_row,
                            label,
                            barchart,
                            statistical,
                        ],
                    ),
                )
            ]
        )

        return baocaotrongnam
