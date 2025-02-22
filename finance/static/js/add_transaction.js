document.addEventListener('DOMContentLoaded', function() {
    // Initialize add transaction page functionality
    console.log('Add transaction page JavaScript loaded');
    
    const categorySelect = document.getElementById('id_category');
    const subcategoryContainer = document.getElementById('subcategory-container');
    
    function updateSubcategoryField() {
        const category = categorySelect.value;
        
        // Clear current content
        subcategoryContainer.innerHTML = '';
        
        if (category === 'Custom') {
            // Show text input for custom subcategory
            subcategoryContainer.innerHTML = `
                <div class="form-group">
                    <label for="id_subcat">Custom Subcategory:</label>
                    <input type="text" 
                           id="id_subcat" 
                           name="subcat" 
                           class="form-control custom-input" 
                           placeholder="Enter custom subcategory"
                           required>
                </div>`;
        } else if (category) {
            // Show dropdown for predefined categories
            subcategoryContainer.innerHTML = `
                <div class="form-group">
                    <label for="id_subcat">Subcategory:</label>
                    <select id="id_subcat" name="subcat" required>
                        <option value="">Select Subcategory</option>
                    </select>
                </div>`;
            
            // Fetch and populate subcategories
            fetch(`/finance/api/get_subcategories/?category=${category}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch subcategories');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Received subcategories:', data);
                    const subcatSelect = document.getElementById('id_subcat');
                    data.forEach(item => {
                        const option = document.createElement('option');
                        option.value = item.id;
                        option.textContent = item.subcat_name;
                        subcatSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error fetching subcategories:', error);
                    subcategoryContainer.innerHTML = `
                        <div class="error-message">
                            Error loading subcategories. Please try again.
                        </div>`;
                });
        }
    }
    
    if (categorySelect) {
        categorySelect.addEventListener('change', updateSubcategoryField);
        
        // Initial load
        if (categorySelect.value) {
            updateSubcategoryField();
        }
    }

    const transactionForm = document.querySelector('form');
    if (transactionForm) {
        transactionForm.addEventListener('submit', function(e) {
            // Add transaction form handling logic here
            console.log('Transaction form submitted');
        });
    }
}); 