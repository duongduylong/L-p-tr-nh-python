from flet import *
from const import *
import datetime
from utils.navbar import create_navbar
import sqlite3


class Outcome(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def create_header():
            """This function builds the header for the page"""

            # Define an inner function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton, button_2: TextButton):
                # Change the background color of button_1 to GREY_COLOR and button_2 to BG_COLOR.
                button_1.style.bgcolor = GREY_COLOR
                button_2.style.bgcolor = BG_COLOR
                header.update()  # Update the header to reflect the color changes.

            # Create two text buttons.
            button_1 = TextButton(
                text="Tiền chi",  # Set the text for button_1
                style=ButtonStyle(
                    color="White", bgcolor=GREY_COLOR
                ),  # Set initial background color to GREY_COLOR
                on_click=lambda e: (
                    change_button_colors(
                        button_1, button_2
                    ),  # Call change_button_colors to update colors
                    self.page.go("/"),  # Redirect to the home page
                ),
            )
            button_2 = TextButton(
                text="Tiền thu",  # Set the text for button_2
                style=ButtonStyle(
                    color="White"
                ),  # Set initial background color to its default
                on_click=lambda e: (
                    change_button_colors(
                        button_2, button_1
                    ),  # Call change_button_colors to update colors
                    self.page.go("/income"),  # Redirect to the income page
                ),
            )

            # Create a header that contains the two buttons and an edit icon.
            header = Row(
                alignment="spaceBetween",
                controls=[
                    Row(
                        controls=[
                            button_1,  # Add the first button to the header
                            button_2,  # Add the second button to the header
                        ]
                    ),
                    Icon(
                        name=icons.EDIT, color="White"
                    ),  # Add an edit icon to the header
                ],
            )

            return header  # Return the header as the result of the function.

        def create_date():
            """Create a date row for client to change the date of money expense"""

            # Define a function to get the next date and update the date header.
            def get_next_date(curr_date):
                curr_date_dt = datetime.datetime.strptime(curr_date, "%Y-%m-%d")
                next_date = curr_date_dt + datetime.timedelta(
                    days=1
                )  # Calculate the next date
                next_date_str = next_date.strftime("%Y-%m-%d")
                date_header.controls[
                    0
                ].text = next_date_str  # Update the displayed date
                date_header.update()  # Update the date header to reflect the changes

            # Define a function to get the previous date and update the date header.
            def get_prev_date(curr_date):
                curr_date_dt = datetime.datetime.strptime(curr_date, "%Y-%m-%d")
                prev_date = curr_date_dt - datetime.timedelta(
                    days=1
                )  # Calculate the previous date
                prev_date_str = prev_date.strftime("%Y-%m-%d")
                date_header.controls[
                    0
                ].text = prev_date_str  # Update the displayed date
                date_header.update()  # Update the date header to reflect the changes

            def get_input_date():
                def bs_dismissed(e):
                    print("Dismissed!")

                def show_bs(e):
                    bs.open = True
                    bs.update()

                def close_bs(e):
                    bs.open = False
                    bs.update()

                def check_date(date):
                    expected_format = "%Y-%m-%d"

                    try:
                        parsed_date = datetime.datetime.strptime(date, expected_format)
                        formatted_date = parsed_date.strftime(expected_format)

                        if date == formatted_date:
                            return True
                        else:
                            return False
                    except ValueError:
                        return False

                bs = BottomSheet(
                    content=Container(
                        content=Column(
                            controls=[
                                TextField(
                                    value=f"{date_header.controls[0].text}",
                                    label="Ngày",
                                ),
                                ElevatedButton(
                                    "Xác nhận", on_click=lambda e: check_update_date()
                                ),
                                ElevatedButton("Đóng", on_click=close_bs),
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

                def check_update_date():
                    new_date = bs.content.content.controls[0].value
                    if not check_date(new_date):
                        bs.content.content.controls[0].border_color = "red"
                        bs.update()
                    else:
                        bs.content.content.controls[0].border_color = "green"
                        bs.update()
                        bs.open = False
                        bs.update()
                        date_header.controls[0].text = new_date
                        date_header.update()

            # Create a row to represent the date header with date, arrows, and controls.
            date_header = Row(
                alignment="spaceBetween",
                controls=[
                    # Create a text widget to display the current date (initialized to today's date).
                    TextButton(
                        datetime.date.today(),
                        on_click=lambda e: get_input_date(),
                        # style=TextStyle(color="white"),
                    ),
                    # Create a row to contain the arrow buttons for navigation.
                    Row(
                        controls=[
                            # Create an icon button for the previous arrow that goes to the previous date.
                            IconButton(
                                icon=icons.ARROW_LEFT,
                                icon_color="White",
                                on_click=lambda event: get_prev_date(
                                    str(date_header.controls[0].text)
                                ),
                            ),
                            # Create an icon button for the next arrow that goes to the next date.
                            IconButton(
                                icon=icons.ARROW_RIGHT,
                                icon_color=colors.WHITE,
                                on_click=lambda event: get_next_date(
                                    str(date_header.controls[0].text)
                                ),
                            ),
                        ]
                    ),
                ],
            )

            return date_header  # Return the date header as the result of the function.

        def create_note():
            # Create a header with a label ("Ghi chú") and a text input field.
            note_header = Row(
                alignment="spaceBetween",
                # spacing=20,
                controls=[
                    Text("Ghi chú", color="White"),
                    TextField(
                        label="Nhập ghi chú",
                        label_style=TextStyle(color="White"),
                        width=250,
                        height=50,
                        border_color="White",
                        color="White",
                    ),
                ],
            )

            return note_header

        def create_money_input():
            money_input = Row(
                alignment="spaceBetween",
                controls=[
                    Text("Tiền chi", color="white"),
                    Row(
                        controls=[
                            TextField(
                                color="white",
                                hint_text="Nhập số tiền",
                                hint_style=TextStyle(
                                    color="White", weight=FontWeight.NORMAL, size=14
                                ),
                                border="underline",
                                width=200,
                                height=40,
                            ),
                            Text("đ", size=16, color="white"),
                        ]
                    ),
                ],
            )

            return money_input

        # category global variables
        global current_button
        current_button = None
        global selected_category
        selected_category = None

        def create_category():
            def create_category_button(text, icon, icon_color):
                category_button = Container(
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Icon(icon, color=icon_color, size=30),
                            Text(text, color="white"),
                        ],
                    ),
                    alignment=alignment.center,
                    bgcolor=BG_COLOR,
                    width=10,
                    height=10,
                    border=border.all(3, BORDER_COLOR),
                    border_radius=10,
                    on_click=lambda e: on_button_click(e, category_button),
                )

                return category_button

            def on_button_click(e, button):
                global current_button
                global selected_category
                # Set the border color of the current button to a new color.
                button.border = border.all(3, "#a9a9a9")

                # Set the border color of the previous button to the default color.
                if current_button is not None:
                    current_button.border = border.all(3, BORDER_COLOR)

                # Set the current button to the button that is clicked.
                current_button = button
                selected_category = button.content.controls[1].value
                category.update()

            category_header = Text("Danh mục")

            category_content = GridView(
                expand=0,
                runs_count=3,
                max_extent=90,
                child_aspect_ratio=1.09,
                spacing=5,
                run_spacing=5,
                controls=[
                    create_category_button("Ăn uống", icons.LOCAL_DINING, "#d78638"),
                    create_category_button(
                        "Gia dụng", icons.HOME_REPAIR_SERVICE, "#049c4b"
                    ),
                    create_category_button("Quần áo", icons.CHECKROOM, "#c9ae1d"),
                    create_category_button("Y tế", icons.EMERGENCY, "#c1455c"),
                    create_category_button("Giáo dục", icons.SCHOOL, "#66bb88"),
                    create_category_button("Tiền điện", icons.ELECTRIC_BOLT, "#dddddd"),
                    create_category_button("Tiền nhà", icons.HOUSE, "#d89825"),
                    create_category_button("Tiền nước", icons.WATER_DROP, "#23bbdc"),
                    create_category_button("Đi lại", icons.DIRECTIONS_BUS, "#fbc932"),
                    create_category_button("Khác", icons.QUESTION_MARK, "#d78638"),
                ],
            )

            category = Column(controls=[category_header, category_content])
            return category

        def create_submit():
            submit_button = TextButton(
                text="Nhập Khoản Tiền",
                style=ButtonStyle(color="White", bgcolor=GREY_COLOR),
                width=350,
                on_click=lambda e: submit(date_row, note_row, money_row),
            )

            return submit_button

        def submit(date, note, money):
            global selected_category

            date_value = date.controls[0].text
            note_value = note.controls[1].value
            money_value = money.controls[1].controls[0].value
            category_value = selected_category
            if category_value == None:
                category_value = "Khác"
            cash_flow = "Tiền chi"

            # Check if money_value is empty or negative
            if not money_value or int(money_value) < 0:

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
                                Text("Lỗi nhập số tiền"),
                                ElevatedButton("Đóng", on_click=close_bs),
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
                return False

            note.controls[1].value = ""
            money.controls[1].controls[0].value = ""
            note.update()
            money.update()

            try:
                # Kết nối đến cơ sở dữ liệu SQLite
                conn = sqlite3.connect("db/app.db")
                cursor = conn.cursor()

                # Sử dụng câu lệnh SQL để tạo bảng nếu chưa tồn tại
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS financial_transaction (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    date TEXT,
                                    note TEXT,
                                    money REAL,
                                    category TEXT,
                                    cash_flow TEXT
                                )"""
                )

                # Sử dụng câu lệnh SQL để chèn dữ liệu vào bảng
                cursor.execute(
                    "INSERT INTO financial_transaction (date, note, money, category, cash_flow) VALUES (?, ?, ?, ?, ?)",
                    (date_value, note_value, money_value, category_value, cash_flow),
                )

                # Lưu thay đổi và đóng kết nối
                conn.commit()
                conn.close()
                print("success")

                # popup msg
                # dlg = AlertDialog(
                #     title=Text("Ghi nhận thành công", color="white", size=16),
                #     on_dismiss=lambda e: print("Dialog dismissed!"),
                # )

                # def open_dlg():
                #     self.page.dialog = dlg
                #     dlg.open = True
                #     self.page.update()

                # open_dlg()

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
                                Text("Ghi nhận thành công"),
                                ElevatedButton("Đóng", on_click=close_bs),
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

                return True  # Trả về True nếu thành công
            except Exception as e:
                print("Lỗi khi thực hiện thao tác chèn dữ liệu:", str(e))
                dlg = AlertDialog(
                    title=Text(f"Lỗi {str(e)}"),
                    on_dismiss=lambda e: print("Dialog dismissed!"),
                )

                def open_dlg():
                    self.page.dialog = dlg
                    dlg.open = True
                    self.page.update()

                open_dlg()
                return False  # Trả về False nếu có lỗi

        header = create_header()
        date_row = create_date()
        note_row = create_note()
        money_row = create_money_input()
        category_row = create_category()
        submit_row = create_submit()
        nav_bar_row = create_navbar(self.page, 0)

        outcome_page_child_container = Container(
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                controls=[
                    header,
                    date_row,
                    note_row,
                    money_row,
                    category_row,
                ],
                # expand=True
            ),
            # expand=True
        )

        def update_size(e):
            outcome_page.controls[0].height = self.page.height
            outcome_page.controls[0].width = self.page.width

            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")

            outcome_page.update()
            outcome_page.page = self.page

        self.page.on_resize = update_size

        # define page 1 properties
        outcome_page = ResponsiveRow(
            controls=[
                Container(
                    width=self.page.width,
                    height=self.page.height,
                    border_radius=35,
                    bgcolor=BG_COLOR,
                    content=Column(
                        alignment="spaceBetween",
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            outcome_page_child_container,
                            submit_row,
                            nav_bar_row,
                        ],
                    ),
                )
            ],
        )

        return outcome_page
