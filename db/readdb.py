import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect("db/app.db")
cursor = conn.cursor()

# Thực hiện truy vấn SQL
cursor.execute("SELECT * FROM financial_transaction")
records = cursor.fetchall()

print(records)
# In dữ liệu
# for record in records:
#     print(record)

# Đóng kết nối
conn.close()
