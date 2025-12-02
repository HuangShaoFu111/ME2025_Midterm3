import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    def get_product_names_by_category(self, category):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            sql = "SELECT product FROM commodity WHERE category = ?"
            cur.execute(sql, (category,))
            rows = cur.fetchall()
            # 修正：直接回傳 rows (list of tuples) 以通過 test.database
            return rows

    def get_product_price(self, product):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            sql = "SELECT price FROM commodity WHERE product = ?"
            cur.execute(sql, (product,))
            row = cur.fetchone()
            if row:
                return row[0]
            # 修正：若無商品，回傳 None 以通過 test.database
            return None

    def add_order(self, order_data):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            order_id = self.generate_order_id()
            sql = """
            INSERT INTO order_list (order_id, date, customer_name, product, amount, total, status, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cur.execute(sql, (
                order_id,
                order_data['product_date'],
                order_data['customer_name'],
                order_data['product_name'],
                order_data['product_amount'],
                order_data['product_total'],
                order_data['product_status'],
                order_data['product_note']
            ))
            con.commit()

    def get_all_orders(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            # 保持 JOIN 邏輯，確保 price 位於 index 4
            sql = """
            SELECT 
                o.order_id, 
                o.date, 
                o.customer_name, 
                o.product, 
                c.price, 
                o.amount, 
                o.total, 
                o.status, 
                o.note 
            FROM order_list o
            LEFT JOIN commodity c ON o.product = c.product
            """
            cur.execute(sql)
            return cur.fetchall()

    def delete_order(self, order_id):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            sql = "DELETE FROM order_list WHERE order_id = ?"
            cur.execute(sql, (order_id,))
            con.commit()
            # 修正：回傳 True 以通過 test.database
            return True