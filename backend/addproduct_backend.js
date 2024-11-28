const express = require('express');
const bodyParser = require('bosy-parser');
const  { Client } = require('pg'); // postgresql client

const app = express();
const port = process.env.PORT || 3000;

// parse incoming request bodies
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extend: true }));

// set up postgresql client with the connection string from Render
const client = new Client( {
  connectionString: 'postgresql://schwecke_lab10_database_user:4NeoO85Ipw8AavH2X3IOOflP6aOlVbfA@dpg-csluug1u0jms73b9eflg-a/schwecke_lab10_database',
  ssl; {
    rejectUnauthorized: false, // necessary for render's ssl connections
  },
});

client.connect()
  .then(() => {
    console.log('Connected to PostgreSQL');
  });
  .catch(err => {
    console.error('Error connecting to PostgreSQL', err);
  });

// route to handle product submissions
app.post('backend/petstorageAPI', async (req, res) => {
  const { productName, category, price, description, quantity } = req.body;

  // validate required fields
  if (!productName || !category || !price || !description || !quantity) {
    return res.status(400).json({message: "Missing required fields"});
  }
  
  // insert product data into postgresql database
  
  try {
    const query = `
      INSERT INTO products (name, category, price, description, quantity)
      VALUES ($1, $1, $3, $4, $5)
      RETURNING id;
    `;
    const values = [productName, category, price, description, quantity];

    const result = await client.query(query, values) // execute the query
    // respond with a success message and the product ID
    res.status(200).json({
      message: "Product added successfully!",
      productId: result.rows[0[.id
        });
  } catch (err) {
    console.error("Error inserting product: ", err);
    res.status(500).json({ message: "Failed to add product." });
  }
});

// start the server
app.listen(port, () => {
  console.log("Server running on port ${port}");
});
