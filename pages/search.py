import sqlite3
from flet import *
from const import *
from datetime import datetime


class Search(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db():
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            # Build the SQL query to filter by year and month
            sql_query = "SELECT * FROM financial_transaction"
            # Execute the query with the provided month and year
            cursor.execute(sql_query)
            records = cursor.fetchall()
            result = [row for row in records]
            conn.close()
            return result

        global data, user_input
        user_input = "!"
        data = fetch_data_from_db()

        def update_views():
            search_report_row_new = create_search_report(user_input, data)
            search_page.controls[0].content.controls[2] = search_report_row_new
            search_page.update()
            self.page.update()

        def delete_data_from_db_by_id(id):
            global data
            print(id)
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            # Build the SQL query to delete a record by ID
            sql_query = "DELETE FROM financial_transaction WHERE id = ?"
            cursor.execute(sql_query, (id,))
            conn.commit()
            conn.close()
            data = fetch_data_from_db()
            update_views()

        def update_data_from_db_by_id(id, date, category, note, amount):
            def bs_dismissed(e):
                print("Dismissed!")

            def show_bs(e):
                bs.open = True
                bs.update()

            def close_bs(e):
                bs.open = False
                bs.update()

            bs = BottomSheet(
                content=Container(
                    content=Column(
                        controls=[
                            TextField(value=f"{date}", label="Ngày"),
                            TextField(value=f"{note}", label="Ghi chú"),
                            TextField(value=f"{int(abs(amount))}", label="Tiền"),
                        ],
                        tight=True,
                    ),
                    padding=20,
                ),
                open=True,
                on_dismiss=bs_dismissed,
            )

            expense_radio_group = ListView(
                height=100,
                controls=[
                    RadioGroup(
                        content=Column(
                            controls=[
                                Radio(value="Ăn uống", label="Ăn uống"),
                                Radio(value="Gia dụng", label="Gia dụng"),
                                Radio(value="Quần áo", label="Quần áo"),
                                Radio(value="Y tế", label="Y tế"),
                                Radio(value="Giáo dục", label="Giáo dục"),
                                Radio(value="Tiền điện", label="Tiền điện"),
                                Radio(value="Tiền nhà", label="Tiền nhà"),
                                Radio(value="Tiền nước", label="Tiền nước"),
                                Radio(value="Đi lại", label="Đi lại"),
                                Radio(value="Khác", label="Khác"),
                            ]
                        ),
                    )
                ],
            )

            income_radio_group = ListView(
                height=100,
                controls=[
                    RadioGroup(
                        content=Column(
                            controls=[
                                Radio(value="Lương", label="Lương"),
                                Radio(value="Phụ cấp", label="Phụ cấp"),
                                Radio(value="Thưởng", label="Thưởng"),
                                Radio(value="Đầu tư", label="Đầu tư"),
                                Radio(value="Làm thêm", label="Làm thêm"),
                                Radio(value="Khác", label="Khác"),
                            ]
                        ),
                    )
                ],
            )

            if amount > 0:
                bs.content.content.controls.append(income_radio_group)
            else:
                bs.content.content.controls.append(expense_radio_group)

            bs.content.content.controls.extend(
                [
                    ElevatedButton("Cập nhật", on_click=lambda e: check_update()),
                    ElevatedButton("Đóng", on_click=close_bs),
                ]
            )
            self.page.overlay.append(bs)
            self.page.add(ElevatedButton("", on_click=show_bs))

            def check_date(date):
                expected_format = "%Y-%m-%d"

                try:
                    parsed_date = datetime.strptime(date, expected_format)
                    formatted_date = parsed_date.strftime(expected_format)

                    if date == formatted_date:
                        return True
                    else:
                        return False
                except ValueError:
                    return False

            def check_update():
                new_date = bs.content.content.controls[0].value
                new_note = bs.content.content.controls[1].value
                new_amount = bs.content.content.controls[2].value
                new_category = bs.content.content.controls[3].controls[0].value
                print(new_category)

                if not check_date(new_date):
                    bs.content.content.controls[0].border_color = "red"
                    bs.update()
                else:
                    bs.content.content.controls[0].border_color = "green"
                    bs.content.content.controls[1].border_color = "green"
                    bs.update()
                    if new_amount == "" or int(new_amount) <= 0:
                        bs.content.content.controls[2].border_color = "red"
                        bs.update()
                    else:
                        bs.content.content.controls[2].border_color = "green"
                        bs.update()
                        if new_category == None:
                            print("haven't found new category")
                        else:
                            update_db(id, new_date, new_note, new_amount, new_category)

            def update_db(id, new_date, new_note, new_amount, new_category):
                global data
                print(id, new_date, new_note, new_amount, new_category)
                conn = sqlite3.connect("db/app.db")
                cursor = conn.cursor()

                # Build the SQL query to update the record
                sql_query = "UPDATE financial_transaction SET date=?, note=?, money=?, category=? WHERE id=?"

                # Execute the query with the new data and id
                cursor.execute(
                    sql_query, (new_date, new_note, new_amount, new_category, id)
                )

                conn.commit()
                conn.close()
                data = fetch_data_from_db()
                update_views()
                bs.open = False
                bs.update()

        def create_header():
            # Create two text buttons.
            header_text = Text("Tìm kiếm (toàn thời gian)", color="white")

            header = Container(
                # bgcolor="black",
                padding=padding.only(bottom=10),
                content=Row(
                    # alignment="spaceBetween",
                    controls=[
                        IconButton(
                            icons.ARROW_BACK,
                            icon_color="white",
                            on_click=lambda e: self.page.go("/calendar"),
                        ),
                        header_text,
                        # IconButton(icons.SEARCH, icon_color="white"),
                    ],
                ),
            )
            return header

        def create_search_textfield():
            def on_submit_search():
                global user_input
                user_input = text_field.controls[0].value
                update_views()

            text_field = Row(
                alignment="spaceBetween",
                controls=[
                    TextField(
                        color="white",
                        label="Nhập từ khóa",
                        label_style=TextStyle(color="white"),
                        on_blur=lambda e: on_submit_search(),
                    ),
                    IconButton(
                        icons.SEARCH,
                        icon_color="white",
                        on_click=lambda e: on_submit_search(),
                    ),
                ],
            )

            return text_field

        def create_search_report(user_input, data):
            result = []
            for item in data:
                for field in item:
                    if str(user_input).lower() in str(field).lower():
                        result.append(item)
                        break  # Once a match is found, move to the next item
            # print(result)
            # print(len(result))
            money_expense = 0
            money_income = 0

            for item in result:
                if item[5] == "Tiền thu":
                    money_income += item[3]
                elif item[5] == "Tiền chi":
                    money_expense += item[3]

            money_total = money_income - money_expense

            income_container = Container(
                # padding=padding.only(left=20, right=20),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tiền thu", weight="bold", color="white"),
                        Text(
                            value=f"{'{:,}'.format(int(money_income))}", color="#50b4d1"
                        ),
                    ],
                ),
            )

            outcome_container = Container(
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tiền chi", weight="bold", color="white"),
                        Text(value=f"{'{:,}'.format(int(money_expense))}", color="red"),
                    ],
                )
            )

            total_container = Container(
                # padding=padding.only(left=20, right=20),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tổng", weight="bold", color="white"),
                        Text(value=f"{'{:,}'.format(int(money_total))}"),
                    ],
                ),
            )

            if money_total >= 0:
                total_container.content.controls[1].color = "#50b4d1"
            else:
                total_container.content.controls[1].color = "red"

            def create_report_row(id, date, category, note, amount):
                report_row = Column(
                    spacing=0,
                    controls=[
                        Divider(height=20, opacity=0),
                        Container(
                            padding=padding.only(top=2, bottom=2),
                            bgcolor="#313131",
                            content=Row(controls=[Text(date, color="white")]),
                        ),
                        Container(
                            content=Row(
                                alignment="spaceBetween",
                                controls=[
                                    Text(category, color="white", size=12),
                                    Text(note, color="white", size=12),
                                    Text(
                                        value=f"{'{:,}'.format(int(amount))}",
                                        color="white",
                                        size=12,
                                    ),
                                    Row(
                                        alignment=MainAxisAlignment.END,
                                        spacing=1,
                                        controls=[
                                            IconButton(
                                                icons.EDIT,
                                                on_click=lambda e: update_data_from_db_by_id(
                                                    id, date, category, note, amount
                                                ),
                                                icon_size=12,
                                            ),
                                            IconButton(
                                                icons.DELETE_OUTLINE,
                                                on_click=lambda e: delete_data_from_db_by_id(
                                                    id
                                                ),
                                                icon_size=12,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            on_click=lambda e: print(id),
                        ),
                    ],
                )
                return report_row

            def create_report_row_no_date(id, date, category, note, amount):
                report_row = Column(
                    spacing=0,
                    controls=[
                        Container(
                            content=Row(
                                alignment="spaceBetween",
                                controls=[
                                    Text(category, color="white", size=12),
                                    Text(note, color="white", size=12),
                                    Text(
                                        value=f"{'{:,}'.format(int(amount))}",
                                        color="white",
                                        size=12,
                                    ),
                                    Row(
                                        spacing=0,
                                        controls=[
                                            IconButton(
                                                icons.EDIT,
                                                on_click=lambda e: update_data_from_db_by_id(
                                                    id, date, category, note, amount
                                                ),
                                                icon_size=12,
                                            ),
                                            IconButton(
                                                icons.DELETE_OUTLINE,
                                                on_click=lambda e: delete_data_from_db_by_id(
                                                    id
                                                ),
                                                icon_size=12,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            on_click=lambda e: print(id, category, note, amount),
                        ),
                    ],
                )
                return report_row

            def create_report_list(result):
                date_rows = {}
                for item in result:
                    id = item[0]
                    date = item[1]
                    category = item[4]
                    note = item[2]
                    if item[5] == "Tiền chi":
                        amount = -item[3]
                    else:
                        amount = item[3]

                    if date not in date_rows:
                        date_rows[date] = create_report_row(
                            id, date, category, note, amount
                        )
                    else:
                        date_rows[date].controls.append(
                            create_report_row_no_date(id, date, category, note, amount)
                        )
                return list(date_rows.values())

            search_report_list_view = ListView(
                height=400,
                spacing=1,
            )

            if len(result) > 0:
                result.sort(key=lambda x: x[1])
                search_report_list_view.controls.extend(create_report_list(result))

            search_report = Column(
                controls=[
                    Row(
                        alignment="spaceBetween",
                        controls=[
                            income_container,
                            outcome_container,
                            total_container,
                        ],
                    ),
                    search_report_list_view,
                ]
            )

            return search_report

        header = create_header()
        text_field_row = create_search_textfield()
        search_report_row = create_search_report(user_input, data)

        def update_size(e):
            search_page.controls[0].height = self.page.height
            search_page.controls[0].width = self.page.width

            print(f"self.page.height is: {self.page.height}")
            print(f"self.page.width is: {self.page.width}")

            search_page.update()

        self.page.on_resize = update_size

        search_page = ResponsiveRow(
            [
                Container(
                    width=self.page.width,
                    height=self.page.height,
                    border_radius=35,
                    bgcolor=BG_COLOR,
                    padding=padding.only(left=30, top=30, right=30),
                    content=Column(
                        # alignment="spaceBetween",
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[header, text_field_row, search_report_row],
                    ),
                )
            ]
        )

        return search_page
