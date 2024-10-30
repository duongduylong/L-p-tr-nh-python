from flet import *
from const import *
from utils.navbar import create_navbar


class Other(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def create_row(icon, text, route):
            row = Container(
                bgcolor=BG_COLOR,
                padding=padding.only(30, 10, 30, 10),
                border=border.only(
                    bottom=border.BorderSide(0.5, "#3c3c3c"),
                    top=border.BorderSide(0.5, "#3c3c3c"),
                ),
                content=Row(
                    controls=[Icon(icon, color="white"), Text(text, color="white")]
                ),
                on_click=lambda e: self.page.go(route),
            )

            return row

        buttons = Column(
            spacing=15,
            controls=[
                Container(
                    padding=padding.only(left=30, top=30),
                    content=Text("Khác", color="white", size=15),
                ),
                create_row(icons.SETTINGS, "Cài đặt cơ bản", "/settings"),
                Column(
                    spacing=0,
                    controls=[
                        create_row(
                            icons.BAR_CHART,
                            "Báo cáo trong năm",
                            "/report_annual_expense",
                        ),
                        create_row(
                            icons.PIE_CHART,
                            "Báo cáo danh mục trong năm",
                            "/report_year_outcome",
                        ),
                        create_row(
                            icons.INSERT_CHART_OUTLINED,
                            "Báo cáo toàn kì",
                            "/report_all_time",
                        ),
                        create_row(
                            icons.PIE_CHART_OUTLINE,
                            "Báo cáo danh mục toàn kì",
                            "/report_outcome_category_all_time",
                        ),
                    ],
                ),
                Column(
                    spacing=0,
                    controls=[
                        create_row(icons.DOWNLOAD, "Đầu ra dữ liệu", "/export_data"),
                        create_row(icons.CLOUD_DOWNLOAD, "Sao lưu dữ liệu", "/"),
                    ],
                ),
                Column(
                    spacing=0,
                    controls=[
                        create_row(icons.QUESTION_MARK, "Trợ giúp", "/"),
                        create_row(icons.INFO, "Thông tin ứng dụng", "/"),
                    ],
                ),
            ],
        )

        navbar = create_navbar(self.page, 3)

        def update_size(e):
            other_page.controls[0].height = self.page.height
            other_page.controls[0].width = self.page.width

            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")

            other_page.update()

        self.page.on_resize = update_size

        other_page = ResponsiveRow(
            [
                Container(
                    width=self.page.width,
                    height=self.page.height,
                    border_radius=35,
                    bgcolor="#0d0d0d",
                    content=Column(
                        alignment="spaceBetween", controls=[buttons, navbar]
                    ),
                )
            ]
        )

        return other_page
