#potentially needing to use this file to help connect with database and flask and backend

import psycopg2
from flask import Flask, render_template
app = Flask(__name__)
import sqlite3

@app.route('/')
def logging_in():
    return render_template('./static/login.html') #username=username

@app.route('/search')
def searching():
    return render_template('./static/searchpage.html') #username=username

@app.route('/mainproductlist')
def main_product():
    return render_template('./static/mainproductlist.html') #username=username


# def get_username():
#     # Connect to your database
#     conn = sqlite3.connect('your_database.db')
#     cursor = conn.cursor()
    
#     # Fetch the username (modify the query according to your database structure)
#     cursor.execute("SELECT username FROM users WHERE id = 1")  # Example query
#     username = cursor.fetchone()
    
#     conn.close()
    
#     return username[0] if username else "Guest"


# if __name__ == '__main__':
#     app.run(debug=True)
    # logging_in()
    # searching()
    # main_product()
