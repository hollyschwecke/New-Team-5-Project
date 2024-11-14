#routes for render and flask

import psycopg2
# import petstore.db
# import login.db
# import suppliers.db
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import sqlite3

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
    return render_template('login.html')

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
    return render_template('addproduct.html') #, tables=[petstore.to_html(classes='data', header="true")])

@app.route('/createaccount')
def creating_account():
    return render_template('createaccount.html') #, tables=[login.to_html(classes='data', header="true")])

@app.route('/main_page')
def creating_main_page():
    return render_template('main_page.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3308)
