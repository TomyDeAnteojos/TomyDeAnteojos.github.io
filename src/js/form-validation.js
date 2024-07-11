function viewPsw() {
    var passwordField = document.getElementById("psw");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

document.getElementById('loginForm').addEventListener('submit', function(event) {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let errorMessage = document.getElementById('errorMessage');

    if (!username || !password) {
        errorMessage.textContent = 'Both fields are required.';
        event.preventDefault();
    }
});