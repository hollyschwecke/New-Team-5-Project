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

// Search bar functionality linked to the database
document.getElementById('searchButton').addEventListener('click', function() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const selectedFilter = document.getElementById('filterSelect').value;

    fetch(`/search?query=${encodeURIComponent(query)}&filter=${encodeURIComponent(selectedFilter)}`)
        .then(response => response.json())
        .then(data => {
            displayResults(data);  // Display the products retrieved from the database
        })
        .catch(error => console.error('Error fetching products:', error));
});

function displayResults(results) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = ""; // Clear previous results

    if (results.length === 0) {
        resultsContainer.innerHTML = "<p>No results found.</p>";
        return;
    }

    results.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.textContent = item.name + " (" + item.category + ")";
        resultsContainer.appendChild(itemDiv);
    });
}
}