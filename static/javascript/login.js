/*  
Author: Claire Lueking, CSPB 3308 Fall 2024
Purpose: Create Javascript functionality for login page to help it function with database
Usage: utilize the HTML and CSS files that are linked to the login page to adjust the signing in/out and database linking 
*/

//Create account button click function added that links to create account page and clears session data
document.getElementById('creaccntbutton').addEventListener('click', function() {
    window.location.href = '/createaccount';
});

// listens for login form submit button and prevents refreshing the page right away, instead goes to javascript
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault()

    // Get data from form (username and password)
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Send login request to the server
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    })
    // procceses the response from server and sees if it is successful
    .then(response => {
    console.log('Response Status:', response.status);  // Log the status code
    return response.json(); // Attempt to parse JSON
    })
    .then(data => {
        console.log('Data:', data); // Verify the JSON response
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
