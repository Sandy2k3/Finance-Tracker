document.addEventListener('DOMContentLoaded', function() {
    // Initialize transaction list page functionality
    console.log('Transaction list page JavaScript loaded');
    
    // Add delete confirmation handler
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this transaction?')) {
                e.preventDefault();
            }
        });
    });

    // Add transaction list filtering and sorting functionality here
    const transactionList = document.querySelector('.transaction-list');
    if (transactionList) {
        // Initialize list handlers
        console.log('Transaction list initialized');
    }
}); 