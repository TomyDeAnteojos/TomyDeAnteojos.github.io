function viewPsw() {
    var passwordField = document.getElementById("psw");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

function validateForm(event) {
    event.preventDefault(); // Evita el envío del formulario por defecto

    var userName = document.getElementById("userName").value;
    var password = document.getElementById("psw").value;

    if (userName === "" || password === "") {
        // Almacenar el mensaje de error en sessionStorage
        sessionStorage.setItem("errorMessage", "Por favor, ingrese todos los datos.");
        // Recargar la página para mostrar el mensaje
        location.reload();
    } else {
        // Limpiar el mensaje de error en sessionStorage
        sessionStorage.removeItem("errorMessage");
        // Si todos los campos están completos, enviar el formulario
        document.getElementById("loginForm").submit();
    }
}

// Añade un event listener al formulario para la validación
document.getElementById("loginForm").addEventListener("submit", validateForm);

// Mostrar el mensaje de error si existe en sessionStorage
document.addEventListener("DOMContentLoaded", function() {
    var alertMessage = sessionStorage.getItem("errorMessage");
    if (alertMessage) {
        var alertDiv = document.getElementById("msj-alert");
        alertDiv.textContent = alertMessage;
        alertDiv.style.color = "red";
    }
});
