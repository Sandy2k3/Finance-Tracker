document.addEventListener('DOMContentLoaded', function() {
    // Initialize login page functionality
    console.log('Login page JavaScript loaded');
    
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

    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Add form validation logic here
            console.log('Form submitted');
        });
    }
}); 