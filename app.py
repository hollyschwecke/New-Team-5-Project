wol#routes for render and flask

import psycopg2
# import petstore.db
# import login.db
# import suppliers.db
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)


def check_user_credentials(username, password):
    conn = sqlite3.connect('petstore.db')
    cur = conn.cursor()

    #query database
    cur.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    conn.close()
    return user # if found

@app.route('/')
def index():
    return render_template('index.html')

# handles login authentication
@app.route('/login', methods=['POST'])
def logging_in():
    username = request.form.get('username')
    password = request.form.get('password')

    # check login credentials against database
    user = check_user_credentials(username, password)

    if user:
        return redirect(url_for('creating_main_page', username=username)) # user exists
    else:
        message = "Invalid username or password"
        return render_template('login.html', message=message)
    #, tables=[login.to_html(classes='data', header="true")])

@app.route('/search')
def searching():
    return render_template('searchpage.html') #, tables=[petstore.to_html(classes='data', header="true")])

@app.route('/mainproductlist')
def main_product():
    return render_template('mainproductlist.html') #, tables=[petstore.to_html(classes='data', header="true")])

@app.route('/addproduct')
def adding_product():
    # get form data
    name = request.form['product-name']
    category = request.form['category']
    price = float(request.form['price'])
    description = request.form['description']
    available_quantity = int(request.form['quantity'])
    date_added = datetime.not().strftime('%Y-%m-%d %H:%M:$S')

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
    conn.sqlite3('petstore.db')
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
            ''', (product_id, image_path))

    conn.commit()
    conn.close()
    
    return render_template('addproduct.html', success=True) #, tables=[petstore.to_html(classes='data', header="true")])

@app.route('/createaccount')
def creating_account():
    return render_template('createaccount.html') #, tables=[login.to_html(classes='data', header="true")])

@app.route('/main_page')
def creating_main_page():
    return render_template('main_page.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3308)
