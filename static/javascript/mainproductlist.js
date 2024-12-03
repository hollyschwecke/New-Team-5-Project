/*  
Author: Claire Lueking, CSPB 3308 Fall 2024
Purpose: Create Javascript functionality for product list page to help it function with database
Usage: utilize the HTML and CSS files that are linked to the  product list page to adjust the signing in/out and database linking 
*/


//Sign Out button click function added that links to login page and clears session data
document.getElementById('signOutButton').addEventListener('click', function() {
    sessionStorage.clear();
    window.location.href = '/login';
});

// Function to display the username by getting the item from the current session and displaying it with welcome text
function displayUsername() {
    const username = sessionStorage.getItem('username');
    const usernameDisplay = document.getElementById('usernameDisplay');
    
    if (username) {
        usernameDisplay.textContent = `User: ${username}`;
    } else {
        fetch('/get_username')
        .then(response => response.json())
        .then(data => {
            // Insert the username into the #usernameDisplay div
            sessionStorage.setItem('username', data.username);
            usernameDisplay.textContent = `Welcome, ${data.username}`;
        })
        .catch(error => console.error('Error fetching username:', error));
    }
}

// Call displayUsername to initialize username display
displayUsername();

// // Fetch products from the server
// async function fetchProducts() {
//     try {
//         const response = await fetch('/api/products');
//         if (!response.ok) {
//             throw new Error('Failed to fetch products');
//         }
//         const products = await response.json();
//         displayResults(products); // Display products dynamically
//     } catch (error) {
//         console.error('Error fetching products:', error);
//         const resultsContainer = document.getElementById('resultsContainer');
//         resultsContainer.innerHTML = '<p>Error loading products. Please try again later.</p>';
//     }
// }

// // Filter and search functionality
// document.getElementById('searchButton').addEventListener('click', function() {
//     const query = document.getElementById('searchInput').value.toLowerCase();
//     const selectedFilter = document.getElementById('filterSelect').value;

//     fetch('/api/products')
//         .then(response => response.json())
//         .then(products => {
//             const filteredResults = products.filter(product => {
//                 const matchesQuery = product.name.toLowerCase().includes(query);
//                 const matchesFilter =
//                     selectedFilter === "" || 
//                     (selectedFilter === "Alphabetically" && product.name) || 
//                     (selectedFilter === "Price: Low to High" && product.price >= 0) || 
//                     (selectedFilter === "Price: High to Low" && product.price <= Infinity); 
//                 return matchesQuery && matchesFilter;
//             });

//             displayResults(filteredResults);
//         })
//         .catch(error => {
//             console.error('Error filtering products:', error);
//             const resultsContainer = document.getElementById('resultsContainer');
//             resultsContainer.innerHTML = '<p>Error applying filter.</p>';
//         });
// });

// // Display results in the results container
// function displayResults(products) {
//     const resultsContainer = document.getElementById('resultsContainer');
//     resultsContainer.innerHTML = ""; // Clear previous results

//     if (products.length === 0) {
//         resultsContainer.innerHTML = "<p>No results found.</p>";
//         return;
//     }

//     products.forEach(product => {
//         const productCard = document.createElement('div');
//         productCard.className = 'product-card';
//         productCard.innerHTML = `
//             <h3>${product.name}</h3>
//             <p>${product.description || 'No description available.'}</p>
//             <p><strong>Price:</strong> $${product.price.toFixed(2)}</p>
//         `;
//         resultsContainer.appendChild(productCard);
//     });
// }

// // Initialize the page by fetching and displaying products
// fetchProducts();
// }
