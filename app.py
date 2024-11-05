#routes for render and flask

import psycopg2
from flask import Flask, render_template
app = Flask(__name__)
# import sqlite3

@app.route('/')
def logging_in():
    return render_template('login.html') 

@app.route('/search')
def searching():
    return render_template('searchpage.html') 

@app.route('/mainproductlist')
def main_product():
    return render_template('mainproductlist.html') 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
