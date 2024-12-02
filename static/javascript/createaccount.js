/*  
Author: Claire Lueking, CSPB 3308 Fall 2024
Purpose: Create Javascript functionality for the create account page to help it function with database
Usage: utilize the HTML and CSS files that are linked to the create account page to adjust the creating an account and database linking 
*/

// listens for create account form submit button and prevents refreshing the page right away, instead goes to javascript
document.getElementById("createForm").addEventListener("submit", function(event) {
    // event.preventDefault();

    // Get data from form (email, username, and password)
    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Send add data request to the server
    fetch('/createaccount', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, username, password })
    })
    // procceses the response from server and sees if it is successful
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Creating an account was successful!");
        } else {
            alert("Not able to create an account with the information provided.");
        }
    })
    // if any errors, logs them to the console (debugging use)
    .catch(error => {
        console.error('Error:', error);
    });
});
