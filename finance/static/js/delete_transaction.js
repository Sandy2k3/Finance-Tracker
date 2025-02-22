document.addEventListener('DOMContentLoaded', function() {
    // Initialize delete transaction page functionality
    console.log('Delete transaction page JavaScript loaded');
    
    const deleteForm = document.querySelector('form');
    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            // Add deletion confirmation logic here
            if (!confirm('Are you sure you want to delete this transaction?')) {
                e.preventDefault();
            }
        });
    }
}); 