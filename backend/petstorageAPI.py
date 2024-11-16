"""
dbAPI.py

Purpose:
    This module provides functionality to create a SQLite database with specific tables.

Author:
    Therese Goshen, Claire Lueking

Usage:
    Import the module and call the create function with the desired database filename.
    Example:
        from dbAPI import create
        create('petstore.db')
"""

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def create(db_filename):
    """
    Create a SQLite database with the following tables:
        - Products
        - Catagories
        - Suppliers 
        - Inventory
        - Orders
        - Users
    """ 
    conn = sqlite3.connect(db_filename) # Connect to the database
    c = conn.cursor() # Create a cursor object to execute SQL commands

    # Create the Products table
    c.execute('''CREATE TABLE IF NOT EXISTS Products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        price REAL NOT NULL,
                        category_id INTEGER,
                        supplier_id INTEGER,
                        stock_quantity INTEGER,
                        date_added TEXT,
                        FOREIGN KEY (category_id) REFERENCES Categories (category_id),
                        FOREIGN KEY (supplier_id) REFERENCES Suppliers (supplier_id)
                    )''')

    # Create the ProductImages table
    c.execute('''CREATE TABLE IF NOT EXISTS ProductImages (
                        image_id INTERGER PRIMARY KEY AUTOINCREMENT
                        product_id INTEGER,
                        image_path TEXT,
                        FOREIGN KEY (product_id) REFERENCES Products (product_id)
                    )''')
    
    # Create the Categories table
    c.execute('''CREATE TABLE IF NOT EXISTS Categories (
                        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                        description TEXT
                    )''')
    
    # Create the Suppliers table
    c.execute('''CREATE TABLE IF NOT EXISTS Suppliers (
                        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL
                    )''')
    
    
    # Create the Inventory table
    c.execute('''CREATE TABLE IF NOT EXISTS Inventory (
                        product_id INTEGER PRIMARY KEY,
                        stock_quantity INTEGER NOT NULL,
                        FOREIGN KEY (product_id) REFERENCES Products (product_id)
                    )''')
    
    #Create the Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        date TEXT,
                        FOREIGN KEY (user_id) REFERENCES Users (user_id),
                        FOREIGN KEY (product_id) REFERENCES Products (product_id)
                    )''')
    
    
    # Create the Users table
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL,
                        role TEXT NOT NULL
                    )''')
    
    conn.commit() # Commit the changes
    conn.close() # Close the connection






# WORKING CODE FOR FILLING AND DROPPING THE TABLE


def fill(db_filename):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    
    #category information inserted into Categories table except ID which is auto-generated and autoicremented
    categories = [
        ('Food','Items for consumption'), 
        ('Hygiene_Items','Personal care products'), 
        ('Clothing','Apparel'),
        ('Toys','Entertainment'),
        ('Basic Needs','Home Furnishings, dishes, etc.')
    ]
    c.executemany("INSERT OR IGNORE INTO Categories (name, description) VALUES (?, ?)", categories)

    #supplier information inserted into the Suppliers table except ID which is autogenerated and autoincremented
    suppliers = [
        ('LovePets', 'lovepets@lovepets.com', '5558923656'),
        ('PetGrub', 'petgrub@petgrub.com', '5559437783'),
        ('ToyTime', 'toytime@toytime.com', '5558127623'),
        ('PetFurniture', 'petfurniture@petfurniture.com', '5556753344'),
        ('BowlsNow', 'bowlsnow@bowlsnow.com', '5559724976'),
    ]
    c.executemany("INSERT OR REPLACE INTO Suppliers (name, email, phone) VALUES (?, ?, ?)", suppliers)

    #product information inserted into the Product table except ID which is autogenerated and autoincremented
    products = [
        ('DogFood', 12.50, 'dry dog food', 10, 3.2024 ),
        ('WaterBowl', 5.00, 'bowl', 12, 5.2024),
        ('Jacket', 10.00, 'clothing', 3, 1.2024)
    ]
    for name, description, price, category_id, supplier_id, stock_quantity, date_added in products:
        c.execute('''
            INSERT  OR REPLACE INTO Products (name, description, price, category_id, supplier_id, stock_quantity, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, price, category_id, supplier_id, stock_quantity, date_added))

    #user information inserted into the Users table except ID which is autogenerated and autoincremented
    users = [
        ('admin', 'admin123', 'admin@example.com', 'admin'),
        ('john_doe', 'password123', 'john@example.com', 'customer'),
        ('jane_doe', 'mypassword', 'jane@example.com', 'customer'),
        ('supplier_01', 'supplypass', 'supplier01@example.com', 'supplier'),
    ]
    c.executemany('''
        INSERT OR IGNORE INTO Users (username, password, email, role)
        VALUES (?, ?, ?, ?)
    ''', users)
    
    #inventory information inserted into the Inventory table except ID which is autogenerated and autoincremented
    inventory = [
        (1, 100),  # DogFood with 100 units in stock
        (3, 50),   # WaterBowl with 50 units in stock
        (4, 30)   # Jacket with 30 units in stock
    ]
    c.executemany('''
        INSERT OR IGNORE INTO Inventory (product_id, stock_quantity)
        VALUES (?, ?)
    ''', inventory)

    #order information inserted into the Orders table except ID which is autogenerated and autoincremented
    orders = [
        (2, 1, 2, '2024-02-01'),  # User 2 ordered 2 DogFood
        (3, 4, 1, '2024-02-03'),  
        (2, 5, 3, '2024-02-05'), 
    ]
    c.executemany('''
        INSERT OR IGNORE INTO Orders (user_id, product_id, quantity, date)
        VALUES (?, ?, ?, ?)
    ''', orders)

    #productimage information inserted into the ProductImages table except ID which is autogenerated and autoincremented
    product_images = [
        (1, '../images/dogfood.png'),  # Image for DogFood
        (2, '../images/waterbowl.png'),  # Image for WaterBowl
        (3, '../images/jacket.png'),  # Image for Jacket
    ]
    c.executemany('''
        INSERT OR IGNORE INTO ProductImages (product_id, image_path)
        VALUES (?, ?)
    ''', product_images)


    conn.commit()
    conn.close()


#drop table so there are no duplicates when calling
def drop(db_filename):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    #tables to drop
    tables = [
        "ProductImages",
        "Products",
        "Categories",
        "Suppliers",
        "Inventory",
        "Orders",
        "Users"
    ]

    # drop each table
    for table in tables:
        c.execute(f"DROP TABLE IF EXISTS {table}")

    conn.commit()
    conn.close()



if __name__ == '__main__':
    db_filename = 'petstore.db'
    create(db_filename)
    fill(db_filename)
    drop(db_filename) 
