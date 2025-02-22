document.addEventListener('DOMContentLoaded', function() {
    // Initialize home page functionality
    console.log('Home page JavaScript loaded');
    
    // Toggle dropdown visibility
    window.toggleDropdown = function() {
        const dropdown = document.getElementById('dropdown-menu');
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    }

    // Close the dropdown if clicked outside
    window.onclick = function(event) {
        if (!event.target.matches('.user-menu img')) {
            const dropdown = document.getElementById('dropdown-menu');
            if (dropdown && dropdown.style.display === 'block') {
                dropdown.style.display = 'none';
            }
        }
    }
}); 