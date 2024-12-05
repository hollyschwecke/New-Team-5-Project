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

// Function that retrieves username from DB, stores username in session, and updates the display
function loginUser() {
    const username = "JaneDoe"; 
    sessionStorage.setItem('username', username);
    displayUsername();
}

// Function to display the username by getting the item from the current session and displaying it with welcome text
function displayUsername() {
    const username = sessionStorage.getItem('username');
    const usernameDisplay = document.getElementById('usernameDisplay');
    
    if (username) {
        usernameDisplay.textContent = `User: ${username}`;
    } else {
        fetch('/login')
        .then(response => response.json())
        .then(data => {
            document.getElementById('usernameDisplay').textContent = `Welcome, ${data.username}`;
        })
        .catch(error => console.error('Error fetching username:', error));
}
}

document.getElementById('searchButton').addEventListener('click', function () {
    const searchInput = document.getElementById('searchInput').value.trim();
    const filterSelect = document.getElementById('filterSelect').value;

    // Send a POST request to the /search route
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            search: searchInput,
            category: filterSelect,
        }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            displayResults(data.results);
        })
        .catch((error) => {
            console.error('Error fetching search results:', error);
        });
});

function displayResults(results) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = ''; // Clear previous results
    window.location.href = '/search/results'; //redirect to search results page
    //no results found case
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No results found.</p>';
        return;
    }
    // for each result do this
    results.forEach((result) => {
        const resultDiv = document.createElement('div');
        resultDiv.classList.add('result-item');
        resultDiv.innerHTML = `
            <h3>${result.name}</h3>
            <p>${result.description}</p>
            <p>Price: $${result.price}</p>
            <p>Stock: ${result.stock_quantity}</p>
        `;
        resultsContainer.appendChild(resultDiv);
    });
}