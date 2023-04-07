import sqlite3


class DBHelper:
    def __init__(self, dbname="all_products.db"):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()

    def setup(self):
        command = """CREATE TABLE IF NOT EXISTS products(
                    productid INT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    coast INT);"""
        self.connection.execute(command)
        self.connection.commit()

    def add_item(self, product):
        self.cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?);", product)
        self.connection.commit()

    def get_items(self):
        command = "SELECT * FROM products"
        all_result = self.cursor.fetchall()
        return all_result
    # def delete_item(self, item_text):
    #     stmt = "DELETE FROM items WHERE description = (?)"
    #     args = (item_text, )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()

