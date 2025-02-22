document.addEventListener('DOMContentLoaded', function() {
    // Initialize registration page functionality
    console.log('Registration page JavaScript loaded');
    
    // Password visibility toggle function
    window.togglePasswordVisibility = function(inputId) {
        const passwordInput = document.getElementById(inputId);
        const toggleButton = passwordInput.nextElementSibling;
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleButton.innerHTML = '🔒';
        } else {
            passwordInput.type = 'password';
            toggleButton.innerHTML = '👁️';
        }
    }

    const registerForm = document.querySelector('form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            // Add registration form validation logic here
            console.log('Registration form submitted');
        });
    }
}); 