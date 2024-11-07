"""
dbAPI.py

Purpose:
    This module provides functionality to create a SQLite database with specific tables.

Author:
    Therese Goshen

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
    
    # Create the Categories table
    c.execute('''CREATE TABLE IF NOT EXISTS Categories (
                        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                        discription TEXT
                    )''')
    
    
    
    # Create the Inventory table
    c.execute('''CREATE TABLE IF NOT EXISTS Inventory (
                        product_id INTEGER PRIMARY KEY,
                        stock_quantity INTEGER NOT NULL,
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


if __name__ == '__main__':
    create('petstore.db') 