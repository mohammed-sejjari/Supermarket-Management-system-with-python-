import sqlite3

connection = sqlite3.connect("products.db")
cursor = connection.cursor()

cursor.execute ('''
                CREATE TABLE products (
                    id INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Price INTEGER,
                    Quantity INTEGER
                )   
''')

connection.commit()
connection.close() 