# Table 1
* Table Name: Users
* Table Description: Table will have the information needed for a user to login
* For each field of the table, provide name and short description.:
  - username: a unique username for each user
  - password: a secure password that
  - email: user email to link login information
  - user_id: unique numeric identifier of user
  - role: role in organization
* List of tests for verifying each table
  ### Use case name : 
  Verify login with valid user name and password
    - Description:
      Test the Inventory System login page
    - Pre-conditions (what needs to be true about the system before the test can be applied):
      User has valid user name and password
    - Test steps:
      1. Navigate to login page
      2. Provide valid user name
      3. Provide valid password
      4. Click login button
    - Expected result:
      User should be able to login
    - Actual result (when you are testing this, how can you tell it worked):
      User is navigated to welcome page/initial search page with successful login
    - Status (Pass/Fail, when this test was performed)
      Pass
    - Notes:
      N/A
    - Post-conditions (what must be true about the system when the test has completed successfully):
      User is validated with database and successfully signed into their account.
      The account session details are logged in database. 
  
# Table 2
* Table Name: Products
* Table Description: Information on existing products such product ID and name, category, price, quantity avialable, quantity sold
* For each field of the table, provide name and short description.
  - product ID: positive integer that is sequential with previous product ids that is a unique identifer of a product
  - product name: name of product
  - category: a classifer for the product that can be reused to classify other similar products
  - description: text description of product
  - price: amount that a customer needs to pay (in US dollars)
  - stock quantity: number of a specific product in stock that are available to purchase by customers
  - supplier_id: unique numeric identifer for supplier
  
* List of tests for verifying each table
  ### Use case name : 
   Verify product has its information attached to it
    - Description:
      Test the Inventory System main product list page
    - Pre-conditions (what needs to be true about the system before the test can be applied):
      User knows product information that they need (either ID, name, category, price, etc.)
    - Test steps:
      1. Navigate to main product list page
      2. Provide search information
      4. Click search button
    - Expected result:
      User should be able to see a list of products based on their search parameters
    - Actual result (when you are testing this, how can you tell it worked):
      User is navigated to product list page with correct products from search
    - Status (Pass/Fail, when this test was performed)
      Pass
    - Notes:
      N/A
    - Post-conditions (what must be true about the system when the test has completed successfully):
      Products are validated with database and successfully able to see the product or products they searched for.
      The account session details are logged in database.

  ### Use case name : 
   Verify adding products is able to attach information to the database
   - Description:
      Test the Inventory System add product page
    - Pre-conditions (what needs to be true about the system before the test can be applied):
      User knows product information that they need to fill in the add product page (ID, name, category, price, quantity available, quantity sold etc.)
    - Test steps:
      1. Navigate to add product page
      2. Provide product information to fill in fields
      4. Click add product button button
    - Expected result:
      User should be able to see a new products added based on their information provided for each product 
    - Actual result (when you are testing this, how can you tell it worked):
      User is navigated to product list page with successful adding of product
    - Status (Pass/Fail, when this test was performed)
      Pass
    - Notes:
      N/A
    - Post-conditions (what must be true about the system when the test has completed successfully):
      Products are validated with database and successfully able to be seen (the product or products they added).
      The account session details are logged in database.
    
# Table 3
* Table Name: Suppliers
* Table Description: Table with information regarding product suppliers
* For each field of the table, provide name and short description.
  - supplier_id: unique numeric indentifer of supplier
  - name: supply company name
  - address: supply company address
  - phone: positive integer number or sets of numbers with dashes (-) for the supply company
  - email: supply company email
* List of tests for verifying each table
  ### Use case name : 
  Verify supply company database has all the information in it
    - Description:
      Test the Inventory System Supplier search function
    - Pre-conditions (what needs to be true about the system before the test can be applied):
      User knows some information about the supplier (supplier_id, phone number, address, name, etc.)
    - Test steps:
      1. Navigate to search page
      2. Provide valid information about supplier
      3. Click search button
    - Expected result:
      User should be able to see supplier information
    - Actual result (when you are testing this, how can you tell it worked):
      User is navigated to the product list page with supplier information upon successful search
    - Status (Pass/Fail, when this test was performed)
      Pass
    - Notes:
      N/A
    - Post-conditions (what must be true about the system when the test has completed successfully):
      Supplier is validated with database and successfully had information pulled up when attached to a product.
      The account session details are logged in database. 
