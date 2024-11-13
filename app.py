#routes for render and flask

import psycopg2
# import petstore.db
# import login.db
# import suppliers.db
from flask import Flask, render_template
app = Flask(__name__)
# import sqlite3

@app.route('/')
def logging_in():
    return render_template('login.html') #, tables=[login.to_html(classes='data', header="true")])

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3308)
