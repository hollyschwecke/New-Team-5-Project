/*  
Author: Claire Lueking, CSPB 3308 Fall 2024
Purpose: Create Javascript functionality for product list page to help it function with database
Usage: utilize the HTML and CSS files that are linked to the  product list page to adjust the signing in/out and database linking 
*/

//potential back button: is it needed?
//document.getElementById('backButton').addEventListener('click', function() {
    // window.history.back();
// });

//Sign Out button click function added that links to login page and clears session data
document.getElementById('signOutButton').addEventListener('click', function() {
    sessionStorage.clear();
    window.location.href = './login.html';
});

//function that retrieves username from DB, stores username in session and updates the display
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
        fetch('/get_username')
        .then(response => response.json())
        .then(data => {
            // Insert the username into the #usernameDisplay div
            document.getElementById('usernameDisplay').textContent = `Welcome, ${data.username}`;
        })
        .catch(error => console.error('Error fetching username:', error));
    }
}

// Call function to simulate logging in (DEMO PURPOSES ONLY)
// loginUser();
// displayUsername();


//Search bar filtering
const data = [
    { name: "Item 1", category: "Category 1" },
    { name: "Item 2", category: "Category 2" },
    { name: "Item 3", category: "Category 3" },
    { name: "Item 4", category: "Category 4" },
    { name: "Item 5", category: "Category 5" },
];

const filterImage = document.getElementById('filterImage');
const dropdown = document.getElementById('dropdown');

filterImage.addEventListener('click', function() {
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none'; // Toggle dropdown
});

dropdown.addEventListener('click', function(event) {
    const selectedValue = event.target.getAttribute('data-value');
    if (selectedValue) {
        document.getElementById('filterSelect').value = selectedValue; // Update the dropdown value
        dropdown.style.display = 'none'; // Hide dropdown after selection
    }
});

document.getElementById('searchButton').addEventListener('click', function() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const selectedFilter = document.getElementById('filterSelect').value;

    const filteredResults = data.filter(item => {
        const matchesQuery = item.name.toLowerCase().includes(query);
        const matchesFilter = selectedFilter === "" || item.category === selectedFilter;
        return matchesQuery && matchesFilter;
    });

    displayResults(filteredResults);
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
