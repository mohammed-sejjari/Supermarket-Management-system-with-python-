import sqlite3
import time
import os

#--function for clear screen
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


connection = sqlite3.connect("products.db")
cursor = connection.cursor()

#--Create file of DataBase
# cursor.execute("""
#     CREATE TABLE products (
#             id INTEGER PRIMARY KEY,
#             Name TEXT NOT NULL,
#             Price INTEGER,
#             Quantity INTEGER
#             )
# """)


o_username = "admin"
o_password = "admin"

clear_screen()

print("\nHello on Supermarket Management System!")
print("-" * 30)
print("\nPlease enter your Username and Password to login:")


username = input("Enter your Username, Please: ")
password = input("Enter your password, Please: ")

#-- function for add products into the file DataBase
def add_product_indb(name, price, quantity):
    cursor.execute(f"""
        INSERT INTO products(Name, Price, Quantity)
        VALUES("{name}", "{price}", {quantity})
        """)

#-- function for remove products into the file DataBase    
def remove_products_indb(name):
    try:
        cursor.execute("""
            SELECT * FROM products
            WHERE name = ?
        """, (name,))

        product_row = cursor.fetchone()

        if product_row:
            cursor.execute("""
            DELETE FROM products
            WHERE name = ?
            """, (name,))
            print("The product removed successfully!!")
        else:
            print("The product not found!")

    except sqlite3.Error as e:
        print("An error accurred: ", e)

#-- function for edit the new details products into the file DataBase  
def edit_products_indb(name, price, quantity):
    try:
        cursor.execute("""
            SELECT * FROM products
            WHERE name = ?
        """, (name,))

        person_row = cursor.fetchone()

        if person_row:
            cursor.execute("""
            UPDATE products
            SET Price = ?, Quantity = ?
            WHERE name =?
            """, (price, quantity, name,))

            print("\nInformation modified successfully!!")
        else:
            print("Name not found in The products!")

    except sqlite3.Error as e:
        print("An error accurred: ", e)

#-- function for show all products into the file DataBase 
def show_products_indb():
    try:
        cursor.execute("SELECT * FROM products")
        all_rows = cursor.fetchall()

        cursor.execute("PRAGMA table_info(products)")
        column_info = cursor.fetchall()
        column_names = [info[1] for info in column_info]

        if all_rows:
            print("|".join(column_names))
            print("-"*30)

            for id, name, price, quantity in all_rows:
                # == print(str(id) + " | " + str(name) + " | " + str(price) + " | " + str(quantity))
                print(f" {id} | {name} | {price} | {quantity}")
        else:
            print("You don't have any products")

    except sqlite3.Error as e:
        print("An error accurred:", e)

#-- function for open invoice products into the file DataBase 
def open_invoice_indb(nams):
    prices = []
    names = nams
    names.pop(-1)

    try:
        for name in names:
            cursor.execute("""
                SELECT * FROM products
                WHERE name = ?
                """, (name, ))
            
            product_row = cursor.fetchone()

            if product_row:
                cursor.execute("""
                    UPDATE products
                    SET Quantity = Quntity - 1
                    WHRER name = ?
                    """, (name, ))
                
                cursor.execute("SELECT Price FROM products WHERE name = ?", (name, ))
                price = cursor.fetchone()
                #-- price --> (10,)
                prices.append(price[0])

            else:
                if name != "q":
                    print("The product not found!")

        print("-" * 30)
        print("Your Bill:")
        print("|".join(names))
        print("|".join(str(price) for price in prices))
        print("Total: " + str(sum(int(number) for number in prices)) + "$")
        print("-" * 30)

    except sqlite3.Error as e:
        print("An error accurred:", e)


if username == o_username and password == o_password:
    clear_screen()
    print("\nWelcome to  your Supermarket Management System!")
    print("\nPlease choose an option to start:")
    
    print("\t1. Add product")
    print("\t2. Remove product")
    print("\t3. Edit product")
    print("\t4. Show products")
    print("\t5. Open invoice")
    print("\t6. Exit")
    

    #-- function for add products
    def add_product():
        print("\nEnter the product details, Please:")
        name = input("\nEnter name's product: ")
        price = input("Enter price's product: ")
        quantity =input("enter the number of quantity: ")
        add_product_indb(name, price, quantity)
        print("\nProduct added successufully!!")
        
    #-- function for remove products
    def remove_product():
        print("\nPlease enter the name of product you want to remove: ")
        name = input("\n name of product: ")
        remove_products_indb(name)

    #-- function for remove products
    def edit_product():
        print("\nPlease enter the name of product you want to edit: ")
        name = input("\nname of product: ")
        price = input("Please, enter the new price: ")
        quantity = input("Please, enter the new number's quantity: ")
        edit_products_indb(name, price, quantity)

    #-- function for show all products   
    def show_products():
        print("This is all Products founded: ")
        show_products_indb()

    #-- function for show all products
    def open_invoice():
        names = []

        while True:
            print("To finish 'q' ")
            print("Please enter the name of product you want to buy: ")
            name = input("\n Enter your Name: ")
            names.append(name)
            if name.lower() == "q":
                open_invoice_indb(names)
                break

    option = input("\nEnter your Option, Please: ")

    if option == "1" or option.lower() == "add product":
        add_product()

    elif option == "2" or option.lower() == "remove product":
        remove_product()

    elif option == "3" or option.lower() == "edit product":
        edit_product()

    elif option == "4" or option.lower() == "show products":
        show_products()

    elif option == "5" or option.lower() == "open invoice":
        open_invoice()

    elif option == "6" or option.lower() == "exit":
        quit()

    else:
        print("Wrong Username or Password")
        quit()


connection.commit()
connection.close() 