import sqlite3


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


class DBHelper:
    def __init__(self, dbname="all_products.db"):
        self.dbname = dbname  # Зачем мне эта строчка я не знаю оставил зачем-то
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()

    def setup(self):
        command = """CREATE TABLE IF NOT EXISTS products(
                    productid INT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    coast INT,
                    photo BLOB NOT NULL);"""
        self.connection.execute(command)
        self.connection.commit()

    def add_item(self, product, file_name):
        bin_photo = convert_to_binary_data(file_name)
        product_info = product + (bin_photo,)
        self.cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?);", product_info)
        self.connection.commit()
        print("new product was successfully added")

    def get_items(self):
        command = "SELECT * FROM products"
        self.cursor.execute(command)
        all_result = self.cursor.fetchall()
        return all_result

    # def delete_item(self, item_text):
    #     stmt = "DELETE FROM items WHERE description = (?)"
    #     args = (item_text, )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()


# my_Db = DBHelper()
# my_Db.setup()
#
# result = my_Db.get_items()
#
# for elem in result:
#     print(elem[0], elem[1], elem[2], elem[3])