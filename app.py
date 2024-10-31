#potentially needing to use this file to help connect with database and flask and backend


from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_username():
    # Connect to your database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    
    # Fetch the username (modify the query according to your database structure)
    cursor.execute("SELECT username FROM users WHERE id = 1")  # Example query
    username = cursor.fetchone()
    
    conn.close()
    
    return username[0] if username else "Guest"

@app.route('/')
def index():
    username = get_username()
    return render_template('index.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
