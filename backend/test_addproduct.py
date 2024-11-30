import unittest
import petstorageAPI as dbAPI
import psycopg2
import os

class TestAddProduct(unittest.TestCase):
    def setUp(self):
        # Database connection parameters
        self.db_connection_params = {
            'host': 'dpg-csluug1u0jms73b9eflg-a.oregon-postgres.render.com',
            'database': 'schwecke_lab10_database',
            'user': 'schwecke_lab10_database_user',
            'password': '4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA'
        }
        self.create_test_db()

    def tearDown(self):
        # Establish connection
        conn = psycopg2.connect(**self.db_connection_params)
        c = conn.cursor()
        # Drop tables to clean up after tests
        c.execute("DROP TABLE IF EXISTS Products CASCADE")
        c.execute("DROP TABLE IF EXISTS Categories CASCADE")
        c.execute("DROP TABLE IF EXISTS Suppliers CASCADE")
        c.execute("DROP TABLE IF EXISTS Orders CASCADE")
        c.execute("DROP TABLE IF EXISTS Inventory CASCADE")
        c.execute("DROP TABLE IF EXISTS Users CASCADE")
        conn.commit()
        conn.close()

    def create_test_db(self):
        # Establish connection
        conn = psycopg2.connect(**self.db_connection_params)
        c = conn.cursor()

        # Create necessary tables
        c.execute('''CREATE TABLE IF NOT EXISTS Categories (
                        category_id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Suppliers (
                        supplier_id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Products (
                        product_id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        price REAL NOT NULL,
                        category_id INTEGER,
                        supplier_id INTEGER,
                        stock_quantity INTEGER,
                        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES Categories (category_id),
                        FOREIGN KEY (supplier_id) REFERENCES Suppliers (supplier_id)
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Users (
                        user_id SERIAL PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL,
                        role TEXT NOT NULL
                    )''')
        c.execute('''INSERT INTO Users (username, password, email, role) 
                     VALUES ('admin', 'admin', 'admin@example.com', 'admin')''')
        c.execute('''CREATE TABLE IF NOT EXISTS Inventory (
                        product_id INTEGER PRIMARY KEY,
                        stock_quantity INTEGER NOT NULL,
                        FOREIGN KEY (product_id) REFERENCES Products (product_id)
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        order_id SERIAL PRIMARY KEY,
                        user_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES Users (user_id),
                        FOREIGN KEY (product_id) REFERENCES Products (product_id)
                    )''')
        c.execute('''INSERT INTO Users (username, password, email, role) 
                     VALUES ('admin', 'admin', 'admin@example.com', 'admin')''')

        conn.commit()
        conn.close()

    def test_add_product_empty_name(self):
        conn = psycopg2.connect(**self.db_connection_params)
        with self.assertRaises(ValueError) as context:
            dbAPI.add_product(self.db_connection_params, name='', description='description', price=10.00, category_id=1, supplier_id=1, stock_quantity=10)
        self.assertEqual(str(context.exception), 'Product name cannot be empty')
        conn.close()

    def test_add_product_empty_description(self):
        conn = psycopg2.connect(**self.db_connection_params)
        with self.assertRaises(ValueError) as context:
            dbAPI.add_product(self.db_connection_params, name='product', description='', price=10.00, category_id=1, supplier_id=1, stock_quantity=10)
        self.assertEqual(str(context.exception), 'Product description cannot be empty')
        conn.close()

    def test_add_product_negative_price(self):
        conn = psycopg2.connect(**self.db_connection_params)
        with self.assertRaises(ValueError) as context:
            dbAPI.add_product(self.db_connection_params, name='product', description='description', price=-10.00, category_id=1, supplier_id=1, stock_quantity=10)
        self.assertEqual(str(context.exception), 'Product price cannot be negative')
        conn.close()

    def test_add_product_negative_quantity(self):
        conn = psycopg2.connect(**self.db_connection_params)
        with self.assertRaises(ValueError) as context:
            dbAPI.add_product(self.db_connection_params, name='product', description='description', price=10.00, category_id=1, supplier_id=1, stock_quantity=-10)
        self.assertEqual(str(context.exception), 'Product quantity cannot be negative')
        conn.close()

    def test_add_product_success(self):
        # Insert a category into the Categories table (to ensure category_id 1 exists)
        conn = psycopg2.connect(**self.db_connection_params)
        c = conn.cursor()
        c.execute('''INSERT INTO Categories (name, description) VALUES (%s, %s) RETURNING category_id''', ('Test Category', 'Test category description'))
        category_id = c.fetchone()[0]
        
        # Insert a supplier into the Suppliers table (to ensure supplier_id 1 exists)
        c.execute('''INSERT INTO Suppliers (name, email, phone) VALUES (%s, %s, %s) RETURNING supplier_id''', 
          ('Test Supplier', 'test@supplier.com', '555-1234'))
        supplier_id = c.fetchone()[0]
        conn.commit()

        # Now you can insert a product with category_id and supplier_id
        product_id = dbAPI.add_product(self.db_connection_params, name='product', description='description', price=10.00, category_id=category_id, supplier_id=supplier_id, stock_quantity=10)

        # Fetch the inserted product
        c.execute('SELECT * FROM Products WHERE product_id = %s', (product_id,))
        product = c.fetchone()

        # Check if the product was inserted correctly
        self.assertEqual(product[1], 'product')
        self.assertEqual(product[2], 'description')
        self.assertEqual(product[3], 10.00)
        self.assertEqual(product[4], category_id)  # Validate category_id matches
        self.assertEqual(product[5], supplier_id)  # Validate supplier_id matches
        self.assertEqual(product[6], 10)  # Validate stock_quantity
        conn.close()


if __name__ == '__main__':
    unittest.main()