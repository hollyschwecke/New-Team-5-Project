# Author: Claire Lueking, Therese Goshen , Holly Schwecke
# Purpose: Create routes for Flask application to connect pages and databases
# Usage: utilize imported packages, the petstore.db, and functions to be able to connect the databases to the proper pages

# import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)


def check_user_credentials(username, password):
    conn = sqlite3.connect('petstore.db')
    cur = conn.cursor()

    #query database
    cur.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()

    conn.close()
    return user # if found


# handles login authentication
@app.route('/login', methods=['POST'])
def logging_in():
    username = request.form.get('username')
    password = request.form.get('password')

    # check login credentials against database
    user = check_user_credentials(username, password)

    if user:
        return redirect(url_for('searching', username=username)) # user exists
    else:
        message = "Invalid username or password"
        return render_template('login.html', message=message)
    

@app.route('/search')
def searching():
    conn = sqlite3.connect('petstore.db')
    cur = conn.cursor()

    # Default query to fetch all products
    query = '''
        SELECT p.id, p.name, p.description, p.price, p.category, p.available_quantity, p.date_added, pi.image_path
        FROM Products p
        LEFT JOIN ProductImages pi ON p.id = pi.product_id
    '''
    parameters = []

    # Handle user input for searching or filtering
    if request.method == 'POST':
        search_term = request.form.get('search', '').strip()
        filter_category = request.form.get('category', '').strip()

        # Build query based on inputs
        if search_term:
            query += " WHERE p.name LIKE ? OR p.description LIKE ?"
            parameters.extend([f'%{search_term}%', f'%{search_term}%'])
        if filter_category:
            if 'WHERE' in query:
                query += " AND p.category = ?"
            else:
                query += " WHERE p.category = ?"
            parameters.append(filter_category)

    # Execute the query
    cur.execute(query, parameters)
    products = cur.fetchall()
    conn.close()

    # Process results to group images for each product
    grouped_products = {}
    for product in products:
        product_id = product[0]
        if product_id not in grouped_products:
            grouped_products[product_id] = {
                'id': product_id,
                'name': product[1],
                'description': product[2],
                'price': product[3],
                'category': product[4],
                'available_quantity': product[5],
                'date_added': product[6],
                'images': []
            }
        if product[7]:  # Add image if it exists
            grouped_products[product_id]['images'].append(product[7])

    final_products = list(grouped_products.values())

    return render_template('searchpage.html', products=final_products)

@app.route('/mainproductlist')
def main_product():
    # Connect to the database
    conn = sqlite3.connect('petstore.db')
    cursor = conn.cursor()

    # Fetch all products and their images
    cursor.execute('''
        SELECT p.id, p.name, p.description, p.price, p.category, p.available_quantity, p.date_added, 
               GROUP_CONCAT(pi.image_path) AS images
        FROM Products p
        LEFT JOIN ProductImages pi ON p.id = pi.product_id
        GROUP BY p.id
    ''')
    products = cursor.fetchall()
    conn.commit()
    conn.close()

    # Pass products to the HTML 
    return render_template('mainproductlist.html', products=products)


@app.route('/addproduct')
def adding_product():
    # get form data
    name = request.form['product-name']
    category = request.form['category']
    price = float(request.form['price'])
    description = request.form['description']
    available_quantity = int(request.form['quantity'])
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # handle image uploads
    image_files = request.files.getlist('picture')
    image_paths = []
    for img in image_files:
        if img:
            # save each image to a specific folder and store the file path
            img_path = f"uploads/{img.filename}"
            img.save(img_path)
            image_paths.append(img_path)

    # create connection to db
    conn = sqlite3.connect('petstore.db')
    cursor = conn.cursor()

    # insert product data into products table
    cursor.execute('''
        INSERT INTO Products (name, description, price, category, available_quantity, date_added)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, price, category, available_quantity, date_added))

    # get id of last inserted product
    product_id = cursor.lastrowid

    # insert image paths into the ProductImages table
    for img_path in image_paths:
        cursor.execute('''
            INSERT INTO ProductImages (product_id, image_path)
            VALUES (?, ?)
            ''', (product_id, img_path))

    conn.commit()
    conn.close()
    
    return render_template('addproduct.html', success=True)


@app.route('/createaccount', methods=['GET', 'POST'])
def creating_account():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Connect to the database
        conn = sqlite3.connect('petstore.db')
        cursor = conn.cursor()

        # Insert the new user into the database
        try:
            cursor.execute('''
                INSERT INTO Users (username, password, email, date_created)
                VALUES (?, ?, ?, ?)
            ''', (username, password, email, date_created))
            conn.commit()
            conn.close()
            return redirect(url_for('logging_in'))
        except Exception as e:
            conn.rollback()
            conn.close()
            return render_template('createaccount.html', error=str(e))

    return render_template('createaccount.html')
 

@app.route('/main_page')
def creating_main_page():
    return render_template('main_page.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3308)
