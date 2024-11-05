// listens for login form submit button and prevents refreshing the page right away, instead goes to javascript
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

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
    // proceses the response from server and sees if it is successful
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Login successful!");
        } else {
            alert("Invalid credentials.");
        }
    })
    // if any errors, logs them to the console (debugging use)
    .catch(error => {
        console.error('Error:', error);
    });
});