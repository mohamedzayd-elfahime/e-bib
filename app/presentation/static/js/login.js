// Get the login form element
const form = document.getElementById("login-form");

// Intercept form submission
form.addEventListener("submit", function (event) {
    // Prevent default browser form submission
    event.preventDefault();

    // Read CSRF token injected in HTML by backend
    const csrfToken = document.getElementById("csrf_token").value;

    // Send POST request to backend
    fetch(form.action, {
        method: "POST",
        headers: {
            // CSRF proof: only a real rendered page can send this
            "X-CSRF-Token": csrfToken
        },
        // Send email + password as form data
        body: new FormData(form)
    })
    .then(response => {
        // Backend answers with 302 -> redirect to /home
        if (response.redirected) {
            window.location.href = response.url;
        } 
        // Authentication failed
        else if (!response.ok) {
            alert("Invalid email or password");
        }
    })
    .catch(() => {
        alert("Network error");
    });
});
