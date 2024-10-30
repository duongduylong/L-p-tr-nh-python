import sqlite3
from flet import *
import csv
from const import *


class Exportdata(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def export_data_from_db():
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            data1 = cursor.execute("""SELECT * FROM financial_transaction""")
            data = [row for row in data1]
            csv_file = "data.csv"

            with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
                # writer = csv.writer(file)
                writer = csv.writer(file, delimiter=",")
                # Write the header row
                writer.writerow(
                    [
                        "ID",
                        "Date",
                        "Description",
                        "Amount",
                        "Category",
                        "Transaction Type",
                    ]
                )

                # Write the data rows
                for row in data:
                    writer.writerow(row)

            print(f"Data has been written to {csv_file}")
            conn.close()
        

        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = Text("Xuất toàn bộ dữ liệu", color="white", weight="bold")

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1)

            # Add the buttons to the page.
            header = Row(
                alignment=MainAxisAlignment.START,
                controls=[
                    IconButton(
                        icons.ARROW_BACK,
                        icon_color="white",
                        on_click=lambda e: self.page.go("/other"),
                    ),
                    button_1,
                ],
            )
            return header
        def on_row_click():
            def delete_data_and_close_dlg(e):
                export_data_from_db()
                close_bs(e)

            def bs_dismissed(e):
                print("Dismissed!")

            def show_bs(e):
                bs.open = True
                bs.update()

            def close_bs(e):
                bs.open = False
                bs.update()

            bs = BottomSheet(
                Container(
                    Column(
                        [
                            Text("Bạn có chắc chắn muốn xuất tất cả dữ liệu dưới dạng csv không"),
                            ElevatedButton(
                                "Yes", on_click=lambda e: delete_data_and_close_dlg(e)
                            ),
                            ElevatedButton("No", on_click=lambda e: close_bs(e)),
                        ],
                        tight=True,
                    ),
                    padding=20,
                ),
                open=True,
                on_dismiss=bs_dismissed,
            )
            self.page.overlay.append(bs)
            self.page.add(ElevatedButton("", on_click=show_bs))

        def create_delete_row():
            # def open_dlg(e):
            #     self.page.dialog = dlg_modal
            #     dlg_modal.open = True
            #     self.page.update()

            # def close_dlg(e):
            #     dlg_modal.open = False
            #     self.page.update()

            # def export_data_and_close_dlg(e):
            #     export_data_from_db()
            #     close_dlg(e)

            # dlg_modal = AlertDialog(
            #     modal=True,
            #     title=Text("Vui lòng xác nhận"),
            #     content=Text(
            #         "Bạn có chắc chắn muốn xuất tất cả dữ liệu dưới dạng csv không"
            #     ),
            #     actions=[
            #         TextButton("Yes", on_click=lambda e: export_data_and_close_dlg(e)),
            #         TextButton("No", on_click=lambda e: close_dlg(e)),
            #     ],
            #     actions_alignment=MainAxisAlignment.END,
            #     on_dismiss=lambda e: print("Modal dialog dismissed!"),
            # )

            row = Container(
                bgcolor=BG_COLOR,
                padding=padding.only(30, 10, 30, 10),
                border=border.only(
                    bottom=border.BorderSide(0.5, "#3c3c3c"),
                    top=border.BorderSide(0.5, "#3c3c3c"),
                ),
                content=Row(
                    controls=[
                        Text("Xuất toàn bộ dữ liệu", color="yellow"),
                    ]
                ),
                on_click=lambda e: on_row_click(),
            )

            return row

        header = create_header()
        delete_row = create_delete_row()

        exportdata_page_child_container = Container(
            padding=padding.only(left=10, top=30, right=30),
            content=Column(controls=[header, delete_row]),
        )

        def update_size(e):
            exportdata_page.controls[0].height = self.page.height
            exportdata_page.controls[0].width = self.page.width

            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")

            exportdata_page.update()

        self.page.on_resize = update_size

        exportdata_page = ResponsiveRow(
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
                            exportdata_page_child_container,
                        ],
                    ),
                )
            ]
        )

        return exportdata_page
