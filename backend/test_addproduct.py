import unittest
import petstorageAPI as dbAPI
import sqlite3
import os

class TestAddProduct(unittest.TestCase):
    def setUp(self):
        self.db_filename = 'test_petstore.db'
        self.create_test_db()

    def teardown(self) -> None:
        return os.remove(self)
    
    def create_test_db(self):
        conn = sqlite3.connect(self.db_filename)
        c = conn.cursor()

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
        
        # Create the Suppliers table
        c.execute('''CREATE TABLE IF NOT EXISTS Suppliers (
                        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL
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
    
        c.execute('INSERT INTO Users (username, password, email, role) VALUES ("admin", "admin", "')

        conn.commit()
        conn.close()

    def test_add_product_empty_name(self):
        with self.assertRaises(ValueError) as context:
            dbAPI.add_product(self.db_filename, '', 'description', 10.00, 1, 1, 10)
        self.assertEqual(str(context.exception), 'Product name cannot be empty')

    def test_add_product_empty_description(self):
        with self.assertRaises(ValueError) as context:
            dbAPI.add_product(self.db_filename, 'product', '', 10.00, 1, 1, 10)
        self.assertEqual(str(context.exception), 'Product description cannot be empty')

    def test_add_product_negative_price(self):
        with self.assertRaises(ValueError) as context:
            dbAPI.add_product(self.db_filename, 'product', 'description', -10.00, 1, 1, 10)
        self.assertEqual(str(context.exception), 'Product price cannot be negative')

    def test_add_product_negative_quantity(self):
        with self.assertRaises(ValueError) as context:
            dbAPI.add_product(self.db_filename, 'product', 'description', 10.00, 1, 1, -10)
        self.assertEqual(str(context.exception), 'Product quantity cannot be negative')

    def test_add_product_success(self):
        # Add a product to the database
        product_id = dbAPI.add_product(self.db_filename, 'product', 'description', 10.00, 1, 1, 10)
        
        conn = sqlite3.connect(self.db_filename)
        c = conn.cursor()
        #Fetch the inserted product with the product_id
        c.execute('SELECT * FROM Products WHERE product_id = ?', (product_id,))
        product = c.fetchone()

        # Check if the product was inserted correctly
        self.assertEqual(product[1], 'product')
        self.assertEqual(product[2], 'description')
        self.assertEqual(product[3], 10.00)
        self.assertEqual(product[4], 1)
        self.assertEqual(product[5], 1)
        self.assertEqual(product[6], 10)
        conn.close()

if __name__ == '__main__':
    unittest.main()