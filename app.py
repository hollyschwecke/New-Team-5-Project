# Author: Claire Lueking, Therese Goshen , Holly Schwecke
# Purpose: Create routes for Flask application to connect pages and databases
# Usage: utilize imported packages, the petstore.db, and functions to be able to connect the databases to the proper pages
import psycopg2
import os
# import petstorageAPI
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
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
    conn = psycopg2.connect("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database") # Connect to the database
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


def fill(db_filename):
    conn = psycopg2.connect("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database")
    c = conn.cursor()
    
    #category information inserted into Categories table except ID which is auto-generated and autoicremented
    categories = [
        ('Food','Items for consumption'), 
        ('Hygiene_Items','Personal care products'), 
        ('Clothing','Apparel'),
        ('Toys','Entertainment'),
        ('Basic Needs','Home Furnishings, dishes, etc.')
    ]
    c.executemany("INSERT OR IGNORE INTO Categories (name, description) VALUES (%s, %s)", categories)

    #supplier information inserted into the Suppliers table except ID which is autogenerated and autoincremented
    suppliers = [
        ('LovePets', 'lovepets@lovepets.com', '5558923656'),
        ('PetGrub', 'petgrub@petgrub.com', '5559437783'),
        ('ToyTime', 'toytime@toytime.com', '5558127623'),
        ('PetFurniture', 'petfurniture@petfurniture.com', '5556753344'),
        ('BowlsNow', 'bowlsnow@bowlsnow.com', '5559724976'),
    ]
    c.executemany("INSERT OR REPLACE INTO Suppliers (name, email, phone) VALUES (%s, %s, %s)", suppliers)

    #product information inserted into the Product table except ID which is autogenerated and autoincremented
    products = [
        ('DogFood', 12.50, 'dry dog food', 10, 3-12-2024 ),
        ('WaterBowl', 5.00, 'bowl', 12, 5-10-2024),
        ('Jacket', 10.00, 'clothing', 3, 10-12-2024)
    ]
    for name, description, price, category_id, supplier_id, stock_quantity, date_added in products:
        c.execute('''
            INSERT  OR REPLACE INTO Products (name, description, price, category_id, supplier_id, stock_quantity, date_added)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
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
        VALUES (%s, %s, %s, %s)
    ''', users)
    
    #inventory information inserted into the Inventory table except ID which is autogenerated and autoincremented
    inventory = [
        (1, 100),  # DogFood with 100 units in stock
        (3, 50),   # WaterBowl with 50 units in stock
        (4, 30)   # Jacket with 30 units in stock
    ]
    c.executemany('''
        INSERT OR IGNORE INTO Inventory (product_id, stock_quantity)
        VALUES (%s, %s)
    ''', inventory)

    #order information inserted into the Orders table except ID which is autogenerated and autoincremented
    orders = [
        (2, 1, 2, '2024-02-01'),  # User 2 ordered 2 DogFood
        (3, 4, 1, '2024-02-03'),  
        (2, 5, 3, '2024-02-05'), 
    ]
    c.executemany('''
        INSERT OR IGNORE INTO Orders (user_id, product_id, quantity, date)
        VALUES (%s, %s, %s, %s)
    ''', orders)

    #productimage information inserted into the ProductImages table except ID which is autogenerated and autoincremented
    product_images = [
        (1, '../images/dogfood.png'),  # Image for DogFood
        (2, '../images/waterbowl.png'),  # Image for WaterBowl
        (3, '../images/jacket.png'),  # Image for Jacket
    ]
    c.executemany('''
        INSERT OR IGNORE INTO ProductImages (product_id, image_path)
        VALUES (%s, %s)
    ''', product_images)


    conn.commit()
    conn.close()

def select(db_filename, table_name, columns='*', where_clause=None, params=()):
    """
    Fetch data from a specified table in the database.

    Args:
        db_filename (str): The database filename.
        table_name (str): The name of the table to query.
        columns (str or list): The columns to retrieve, '*' for all columns (default).
        where_clause (str, optional): SQL WHERE clause without 'WHERE' (default: None).
        params (tuple, optional): Parameters for the WHERE clause (default: empty tuple).

    Returns:
        list of tuples: The rows retrieved from the table.
    """
    conn = psycopg2.connect("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database")
    c = conn.cursor()

    # Convert list of columns to a comma-separated string
    if isinstance(columns, list):
        columns = ', '.join(columns)

    # Build the query
    query = f"SELECT {columns} FROM {table_name}"
    if where_clause:
        query += f" WHERE {where_clause}"

    # Execute the query
    c.execute(query, params)
    results = c.fetchall()

    conn.commit()
    conn.close()
    return results

#drop table so there are no duplicates when calling
def drop(db_filename):
    conn = psycopg2.connect("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database")
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

def check_user_credentials(username, password):
    #conn = sqlite3.connect('petstore.db')
    conn = psycopg2.connect("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database")
    cur = conn.cursor()

    #query database
    cur.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()

    conn.close()
    return user # if found


# handles login authentication
@app.route('/login', methods=['GET', 'POST'])
def logging_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # check login credentials against database
        user = check_user_credentials(username, password)

        if user:
            return redirect(url_for('searching', username=username)) # user exists
        else:
            message = "Invalid username or password"
            return render_template('login.html', message=message)
        
    return render_template("login.html")
    



@app.route('/search', methods=['GET', 'POST'])
def searching():
    try:
        conn = psycopg2.connect(os.getenv("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database"))
        cur = conn.cursor()

        # Default query to fetch all products
        query = '''
            SELECT p.product_id, p.name, p.description, p.price, p.category_id, p.stock_quantity, p.date_added, i.image_path
            FROM Products p
            LEFT JOIN ProductImages i ON i.product_id = p.product_id
        '''
        parameters = []

        # Handle user input for searching or filtering
        if request.method == 'POST':
            search_term = request.form.get('search', '').strip()
            filter_category = request.form.get('category', '').strip()

            # Build query based on inputs
            if search_term:
                query += " WHERE p.name LIKE %s OR p.description LIKE %s"
                parameters.extend([f'%{search_term}%', f'%{search_term}%'])
            if filter_category:
                if 'WHERE' in query:
                    query += " AND p.category_id = %s"
                else:
                    query += " WHERE p.category_id = %s"
                parameters.append(filter_category)

        cur.execute(query, parameters)
        results = cur.fetchall()
        cur.close()
        return render_template("searchpage.html", results=results)
    
    except Exception as e:
        print(f"Database error: {e}")
        return "An error occurred while processing your request.", 500


@app.route('/mainproductlist')
def main_product():
    try:
        # Connect to the database
        conn = psycopg2.connect("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database")
        
        # Fetch all products and their images
        query = '''
            SELECT p.product_id, p.name, p.description, p.price, p.category_id, 
                   p.stock_quantity, p.date_added, 
                   STRING_AGG(pi.image_path, ',') AS images
            FROM Products p
            LEFT JOIN ProductImages pi ON pi.product_id = p.product_id
            GROUP BY p.product_id
        '''
        
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                products = cursor.fetchall()
        
        # Pass products to the HTML 
        return render_template('mainproductlist.html', products=products)

    except Exception as e:
        print(f"Database error: {e}")
        return "An error occurred while processing your request.", 500


@app.route('/addproduct', methods=['GET', 'POST'])
def adding_product():
    # get form data
    name = request.form['product-name']
    category = request.form['category']
    price = float(request.form['price'])
    description = request.form['description']
    available_quantity = int(request.form['quantity'])
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # handle image uploads
    image_files = request.files.getlist('images')
    image_paths = []
    for img in image_files:
        if img:
            # save each image to a specific folder and store the file path
            img_path = f"uploads/{img.filename}"
            img.save(img_path)
            image_paths.append(img_path)

    # create connection to db
    #conn = sqlite3.connect('petstore.db')
    conn = psycopg2.connect("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database")
    cursor = conn.cursor()

    # insert product data into products table
    cursor.execute('''
        INSERT INTO Products (name, description, price, category, available_quantity, date_added)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, description, price, category, available_quantity, date_added))

    # get id of last inserted product
    product_id = cursor.fetchone()[0]

    # insert image paths into the ProductImages table
    for img_path in image_paths:
        cursor.execute('''
            INSERT INTO ProductImages (product_id, image_path)
            VALUES (%s, %s)
            ''', (product_id, img_path))

    conn.commit()
    conn.close()
    
    return redirect(url_for('addproduct.html'))


@app.route('/createaccount', methods=['GET', 'POST'])
def creating_account():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Connect to the database
        #conn = sqlite3.connect('petstore.db')
        conn = psycopg2.connect("postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database")
        cursor = conn.cursor()

        # Insert the new user into the database
        try:
            cursor.execute('''
                INSERT INTO Users (username, password, email, date_created)
                VALUES (%s, %s, %s, %s)
            ''', (username, password, email, date_created))
            conn.commit()
            conn.close()
            return redirect(url_for('logging_in'))
        except Exception as e:
            conn.rollback()
            conn.close()
            return render_template('createaccount.html', error=str(e))

    return render_template('createaccount.html')
 

@app.route('/') 
def creating_main_page():
    return render_template('main_page.html')

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=3308)
    app.run(debug=True)
    # db_filename = 'petstore.db'
    # create(db_filename)
    # fill(db_filename)
    # select(db_filename)
    # drop(db_filename) 
