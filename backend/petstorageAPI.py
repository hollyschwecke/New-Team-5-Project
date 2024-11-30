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
import psycopg2

app = Flask(__name__)


def create(db_connection_params):
    """
    Create a PostgreSQL database with the following tables:
        - Products
        - Categories
        - Suppliers
        - Inventory
        - Orders
        - Users
    """
    conn = psycopg2.connect(**db_connection_params)  # Connect to PostgreSQL
    c = conn.cursor()  # Create a cursor object to execute SQL commands

    # Create the Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category_id INTEGER,
            supplier_id INTEGER,
            stock_quantity INTEGER,
            date_added DATE,
            FOREIGN KEY (category_id) REFERENCES Categories (category_id),
            FOREIGN KEY (supplier_id) REFERENCES Suppliers (supplier_id)
        )
    ''')

    # Create the ProductImages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS ProductImages (
            image_id SERIAL PRIMARY KEY,
            product_id INTEGER,
            image_path TEXT,
            FOREIGN KEY (product_id) REFERENCES Products (product_id)
        )
    ''')

    # Create the Categories table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            category_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Create the Suppliers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Suppliers (
            supplier_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # Create the Inventory table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Inventory (
            product_id INTEGER PRIMARY KEY,
            stock_quantity INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Products (product_id)
        )
    ''')

    # Create the Orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id SERIAL PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            date DATE,
            FOREIGN KEY (user_id) REFERENCES Users (user_id),
            FOREIGN KEY (product_id) REFERENCES Products (product_id)
        )
    ''')

    # Create the Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    conn.commit()  # Commit the changes
    conn.close()  # Close the connection


def fill(db_connection_params):
    conn = psycopg2.connect(**db_connection_params) # Connect to PostgreSQL, the star operator unpacks the dictionary
    c = conn.cursor()

    # Insert category data into Categories table
    categories = [
        ('Food', 'Items for consumption'),
        ('Hygiene_Items', 'Personal care products'),
        ('Clothing', 'Apparel'),
        ('Toys', 'Entertainment'),
        ('Basic Needs', 'Home Furnishings, dishes, etc.')
    ]
    c.executemany("INSERT INTO Categories (name, description) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING", categories)

    # Insert supplier data into Suppliers table
    suppliers = [
        ('LovePets', 'lovepets@lovepets.com', '5558923656'),
        ('PetGrub', 'petgrub@petgrub.com', '5559437783'),
        ('ToyTime', 'toytime@toytime.com', '5558127623'),
        ('PetFurniture', 'petfurniture@petfurniture.com', '5556753344'),
        ('BowlsNow', 'bowlsnow@bowlsnow.com', '5559724976')
    ]
    c.executemany("INSERT INTO Suppliers (name, email, phone) VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING", suppliers)

    # Insert product data into Products table
    products = [
        ('DogFood', 12.50, 'dry dog food', 1, 1, 100, '2024-03-12'),
        ('WaterBowl', 5.00, 'bowl', 2, 2, 50, '2024-05-10'),
        ('Jacket', 10.00, 'clothing', 3, 3, 30, '2024-10-12')
    ]
    c.executemany('''
        INSERT INTO Products (name, description, price, category_id, supplier_id, stock_quantity, date_added)
        VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING
    ''', products)

    # Insert user data into Users table
    users = [
        ('admin', 'admin123', 'admin@example.com', 'admin'),
        ('john_doe', 'password123', 'john@example.com', 'customer'),
        ('jane_doe', 'mypassword', 'jane@example.com', 'customer'),
        ('supplier_01', 'supplypass', 'supplier01@example.com', 'supplier'),
    ]
    c.executemany('''
        INSERT INTO Users (username, password, email, role)
        VALUES (%s, %s, %s, %s) ON CONFLICT (username) DO NOTHING
    ''', users)

    # Insert inventory data into Inventory table
    inventory = [
        (1, 100),  # DogFood with 100 units in stock
        (2, 50),   # WaterBowl with 50 units in stock
        (3, 30)    # Jacket with 30 units in stock
    ]
    c.executemany('''
        INSERT INTO Inventory (product_id, stock_quantity)
        VALUES (%s, %s) ON CONFLICT (product_id) DO NOTHING
    ''', inventory)

    # Insert order data into Orders table
    orders = [
        (2, 1, 2, '2024-02-01'),
        (3, 2, 1, '2024-02-03'),
        (2, 3, 3, '2024-02-05')
    ]
    c.executemany('''
        INSERT INTO Orders (user_id, product_id, quantity, date)
        VALUES (%s, %s, %s, %s) ON CONFLICT (order_id) DO NOTHING
    ''', orders)

    # Insert product image data into ProductImages table
    product_images = [
        (1, '../images/dogfood.png'),
        (2, '../images/waterbowl.png'),
        (3, '../images/jacket.png')
    ]
    c.executemany('''
        INSERT INTO ProductImages (product_id, image_path)
        VALUES (%s, %s) ON CONFLICT (product_id) DO NOTHING
    ''', product_images)

    conn.commit()
    conn.close()


def select(db_connection_params, table_name, columns='*', where_clause=None, params=()):
    """
    Fetch data from a specified table in the database.

    Args:
        db_connection_params (dict): The connection parameters for PostgreSQL.
        table_name (str): The name of the table to query
        columns (str or list): The columns to retrieve, '*' for all columns
        where_clause (str, optional): SQL WHERE clause without 'WHERE' (default: None).
        params (tuple, optional): Parameters for the WHERE clause (default: empty tuple).

    Returns:
        list of tuples: The rows retrieved from the table.
    """
    conn = psycopg2.connect(**db_connection_params)
    c = conn.cursor()

    if isinstance(columns, list):
        columns = ', '.join(columns)

    query = f"SELECT {columns} FROM {table_name}"
    if where_clause:
        query += f" WHERE {where_clause}"

    c.execute(query, params)
    results = c.fetchall()

    conn.commit()
    conn.close()
    return results

def add_product(db_connection_params, name, description, price, category_id, supplier_id, stock_quantity):
    # Input validation
    if not name:
        raise ValueError("Product name cannot be empty")
    if not description:
        raise ValueError("Product description cannot be empty")
    if price < 0:
        raise ValueError("Product price cannot be negative")
    if stock_quantity < 0:
        raise ValueError("Product quantity cannot be negative")
    
    try:
        # Connect to the PostgreSQL database using db_params
        conn = psycopg2.connect(**db_connection_params)  # Unpack db_params dictionary
        cursor = conn.cursor()

        # Prepare the SQL query to insert a new product into the Products table
        query = '''
            INSERT INTO Products (name, description, price, category_id, supplier_id, stock_quantity) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING product_id;
        '''
        
        # Execute the query with the provided values
        cursor.execute(query, (name, description, price, category_id, supplier_id, stock_quantity))
        
        # Fetch the product_id of the newly inserted product
        product_id = cursor.fetchone()[0]

        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the product_id of the newly added product
        return product_id
   
    except psycopg2.Error as e:
        # This block handles any exception raised by psycopg2
        print(f"An error occurred: {e}")
        raise 


def drop(db_connection_params):
    conn = psycopg2.connect(**db_connection_params)
    c = conn.cursor()

    # Drop each table
    tables = [
        "ProductImages",
        "Products",
        "Categories",
        "Suppliers",
        "Inventory",
        "Orders",
        "Users"
    ]
    for table in tables:
        c.execute(f"DROP TABLE IF EXISTS {table} CASCADE")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    db_connection_params = {
    'host': 'dpg-csluug1u0jms73b9eflg-a.oregon-postgres.render.com',
    'database': 'schwecke_lab10_database',
    'user': 'schwecke_lab10_database_user',
    'password': '4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA'
    }
    create(db_connection_params)
    fill(db_connection_params)
    # drop(db_connection_params)