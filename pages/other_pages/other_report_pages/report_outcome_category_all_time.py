import sqlite3
from flet import *
from const import *


class Report_Outcome_Category_All_Time(UserControl):
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
                style=ButtonStyle(color="white", bgcolor=PINK),
                on_click=lambda e: (
                    change_button_colors(button_1, button_2),
                    self.page.go("/report_outcome_category_all_time"),
                ),
            )
            button_2 = TextButton(
                text="Thu nhập",
                style=ButtonStyle(color="White"),
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
                        padding=padding.only(right=container_width/2),
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
            total_expense = sum(row[3] for row in data if row[5] == "Tiền chi")
            if total_expense != 0:
                anuong = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Ăn uống")
                    / total_expense
                    * 100
                )
                quanao = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Quần áo")
                    / total_expense
                    * 100
                )
                tiennha = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Tiền nhà")
                    / total_expense
                    * 100
                )
                tiendien = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Tiền điện")
                    / total_expense
                    * 100
                )
                giadung = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Gia dụng")
                    / total_expense
                    * 100
                )
                yte = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Y tế")
                    / total_expense
                    * 100
                )
                giaoduc = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Giáo dục")
                    / total_expense
                    * 100
                )
                dilai = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Đi lại")
                    / total_expense
                    * 100
                )
                tiennuoc = "{:.2f}".format(
                    sum(row[3] for row in data if row[4] == "Tiền nước")
                    / total_expense
                    * 100
                )
                khac = "{:.2f}".format(
                    sum(
                        row[3]
                        for row in data
                        if (row[4] == "Khác" and row[5] == "Tiền chi")
                    )
                    / total_expense
                    * 100
                )
            else:
                anuong = (
                    quanao
                ) = (
                    tiennha
                ) = (
                    tiendien
                ) = giadung = yte = giaoduc = dilai = tiennuoc = khac = "0.00"

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
                        quanao,
                        title="Quần áo" + str(f"{quanao}") + "%",
                        title_style=normal_title_style2,
                        color=colors.BLUE,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        tiennha,
                        title="Tiền nhà" + str(f"{tiennha}") + "%",
                        title_style=normal_title_style2,
                        color=colors.YELLOW,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        tiendien,
                        title="Tiền điện" + str(f"{tiendien}") + "%",
                        title_style=normal_title_style2,
                        color=colors.PURPLE,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        anuong,
                        title="Ăn uống" + str(f"{anuong}") + "%",
                        title_style=normal_title_style2,
                        color=colors.GREEN,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        giadung,
                        title="Gia dụng" + str(f"{giadung}") + "%",
                        title_style=normal_title_style2,
                        color=colors.RED,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        yte,
                        title="Y tế" + str(f"{yte}") + "%",
                        title_style=normal_title_style2,
                        color=colors.ORANGE,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        giaoduc,
                        title="Giáo dục" + str(f"{giaoduc}") + "%",
                        title_style=normal_title_style2,
                        color=colors.PINK,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        tiennuoc,
                        title="Tiền nước" + str(f"{tiennuoc}") + "%",
                        title_style=normal_title_style2,
                        color=colors.BROWN,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        dilai,
                        title="Đi lại" + str(f"{dilai}") + "%",
                        title_style=normal_title_style2,
                        color=colors.GREY,
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

        def create_statistics(data):
            statistics = ListView(
                height=150,
                width=340,
                # scroll='auto',
                spacing=1,
            )
            anuong = (int)(sum(row[3] for row in data if row[4] == "Ăn uống"))
            quanao = (int)(sum(row[3] for row in data if row[4] == "Quần áo"))
            tiennha = (int)(sum(row[3] for row in data if row[4] == "Tiền nhà"))
            tiendien = (int)(sum(row[3] for row in data if row[4] == "Tiền điện"))
            giadung = (int)(sum(row[3] for row in data if row[4] == "Gia dụng"))
            yte = (int)(sum(row[3] for row in data if row[4] == "Y tế"))
            giaoduc = (int)(sum(row[3] for row in data if row[4] == "Giáo dục"))
            dilai = (int)(sum(row[3] for row in data if row[4] == "Đi lại"))
            tiennuoc = (int)(sum(row[3] for row in data if row[4] == "Tiền nước"))
            khac = (int)(sum(
                row[3] for row in data if row[4] == "Khác" and row[5] == "Tiền chi"
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
                    create_statistics_row(tiennha, icons.HOUSE, "Tiền nhà", "yellow"),
                    create_statistics_row(
                        tiendien, icons.ELECTRIC_BOLT, "Tiền điện", "purple"
                    ),
                    create_statistics_row(quanao, icons.CHECKROOM, "Quần áo", "blue"),
                    create_statistics_row(anuong, icons.LOCAL_DINING, "Ăn uống", "green"),
                    create_statistics_row(
                        giadung, icons.HOME_REPAIR_SERVICE, "Gia dụng", "red"
                    ),
                    create_statistics_row(yte, icons.EMERGENCY, "Y tế", "orange"),
                    create_statistics_row(giaoduc, icons.SCHOOL, "Giáo dục", "pink"),
                    create_statistics_row(dilai, icons.DIRECTIONS_BUS, "Đi lại", "grey"),
                    create_statistics_row(
                        tiennuoc, icons.WATER_DROP, "Tiền nước", "brown"
                    ),
                    create_statistics_row(khac, icons.QUESTION_MARK, "Khác", "black"),
                ]
            )

            return statistics

        header = create_header()
        label = create_chart_label()
        piechart = create_piechart(data)
        statistics = create_statistics(data)

        report_outcome_category_all_time_page_child_container = Container(
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
            report_outcome_category_all_time_page.controls[0].height = self.page.height
            report_outcome_category_all_time_page.controls[0].width = self.page.width

            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")

            report_outcome_category_all_time_page.update()

        self.page.on_resize = update_size

        report_outcome_category_all_time_page = ResponsiveRow(
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
                            report_outcome_category_all_time_page_child_container,
                            statistics,
                        ],
                    ),
                )
            ]
        )

        return report_outcome_category_all_time_page