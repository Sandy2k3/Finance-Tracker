document.addEventListener('DOMContentLoaded', function() {
    // Get canvas contexts
    const incomeCtx = document.getElementById('incomeChart').getContext('2d');
    const expensesCtx = document.getElementById('expensesChart').getContext('2d');
    const netBalanceCtx = document.getElementById('netBalanceChart').getContext('2d');
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    
    // Initialize charts as null
    let incomeChart = null;
    let expensesChart = null;
    let netBalanceChart = null;
    let pieChart = null;
    
    // Get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Fetch options with CSRF token
    const fetchOptions = {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    };

    // Colors for the charts
    const chartColors = {
        income: 'rgb(75, 192, 192)',
        expenses: 'rgb(255, 99, 132)',
        net: 'rgb(54, 162, 235)',
        pieColors: [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#7BC8A4', '#7377BF'
        ]
    };

    // Common chart options
    const commonChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            tooltip: {
                enabled: true,
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += new Intl.NumberFormat('en-US', {
                                style: 'currency',
                                currency: 'USD'
                            }).format(context.parsed.y);
                        }
                        return label;
                    }
                }
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                },
                ticks: {
                    callback: function(value) {
                        return new Intl.NumberFormat('en-US', {
                            style: 'currency',
                            currency: 'USD'
                        }).format(value);
                    },
                    font: {
                        size: 10
                    }
                }
            },
            x: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                },
                ticks: {
                    font: {
                        size: 10
                    }
                }
            }
        },
        layout: {
            padding: {
                left: 10,
                right: 10,
                top: 5,
                bottom: 5
            }
        }
    };

    // Initialize the charts with data
    function initializeCharts(data) {
        console.log('Initializing charts with data:', data);
        
        // Destroy existing charts if they exist
        if (incomeChart) incomeChart.destroy();
        if (expensesChart) expensesChart.destroy();
        if (netBalanceChart) netBalanceChart.destroy();
        
        // Create Income Chart
        incomeChart = new Chart(incomeCtx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Income',
                    data: data.income,
                    borderColor: chartColors.income,
                    backgroundColor: chartColors.income + '20',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                ...commonChartOptions,
                onClick: (event, elements) => handleChartClick(event, elements, 'Income', data.labels)
            }
        });
        
        // Create Expenses Chart
        expensesChart = new Chart(expensesCtx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Expenses',
                    data: data.expenses,
                    borderColor: chartColors.expenses,
                    backgroundColor: chartColors.expenses + '20',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                ...commonChartOptions,
                onClick: (event, elements) => handleChartClick(event, elements, 'Expenses', data.labels)
            }
        });
        
        // Create Net Balance Chart
        netBalanceChart = new Chart(netBalanceCtx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Net Balance',
                    data: data.net,
                    borderColor: chartColors.net,
                    backgroundColor: chartColors.net + '20',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: commonChartOptions
        });
    }

    // Initialize the pie chart with empty data
    function initializePieChart() {
        console.log('Initializing pie chart');
        
        if (pieChart) {
            pieChart.destroy();
        }

        pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: chartColors.pieColors,
                    borderWidth: 1,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Category Breakdown',
                        font: {
                            size: 14
                        },
                        padding: {
                            top: 0,
                            bottom: 10
                        }
                    },
                    legend: {
                        display: true,
                        position: 'right',
                        labels: {
                            boxWidth: 12,
                            padding: 10,
                            font: {
                                size: 10
                            }
                        }
                    },
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${new Intl.NumberFormat('en-US', {
                                    style: 'currency',
                                    currency: 'USD'
                                }).format(value)} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Handle click on chart
    function handleChartClick(event, elements, categoryType, labels) {
        if (!elements || elements.length === 0) {
            console.log('No chart element clicked');
            return;
        }
        
        const element = elements[0];
        const monthIndex = element.index;
        
        // Ensure we have valid data
        if (monthIndex === undefined || !labels || !labels[monthIndex]) {
            console.log('Invalid click data:', { monthIndex, labels });
            return;
        }
        
        const monthName = labels[monthIndex];
        
        console.log('\n=== Chart Click Event ===');
        console.log('Month Index:', monthIndex);
        console.log('Month Name:', monthName);
        console.log('Category Type:', categoryType);
        
        // Update pie chart title immediately to show loading state
        if (pieChart) {
            pieChart.options.plugins.title.text = `Loading ${monthName} ${categoryType} Breakdown...`;
            pieChart.update();
        }
        
        // Construct the API URL
        const apiUrl = `/finance/api/monthly-breakdown/?month=${encodeURIComponent(monthName)}&type=${encodeURIComponent(categoryType)}`;
        console.log('Fetching data from:', apiUrl);
        
        // Fetch and update the pie chart data
        fetch(apiUrl, fetchOptions)
            .then(response => {
                console.log('Response received:', response);
                if (response.redirected) {
                    window.location.href = response.url;
                    throw new Error('Session expired. Please log in again.');
                }
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Failed to fetch breakdown data');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('\nReceived breakdown data:', data);
                
                if (!data.labels || !data.values || data.labels.length === 0) {
                    console.log('No breakdown data available');
                    pieChart.data.labels = [];
                    pieChart.data.datasets[0].data = [];
                    pieChart.options.plugins.title.text = `No ${categoryType} data for ${monthName}`;
                } else {
                    console.log('Updating pie chart with:', data);
                    pieChart.data.labels = data.labels;
                    pieChart.data.datasets[0].data = data.values;
                    pieChart.options.plugins.title.text = `${monthName} ${categoryType} Breakdown`;
                    
                    while (pieChart.data.datasets[0].backgroundColor.length < data.labels.length) {
                        pieChart.data.datasets[0].backgroundColor = pieChart.data.datasets[0].backgroundColor.concat(chartColors.pieColors);
                    }
                }
                
                pieChart.update();
            })
            .catch(error => {
                console.error('\nError in handleChartClick:', error);
                alert('Error loading breakdown data: ' + error.message);
                
                pieChart.data.labels = [];
                pieChart.data.datasets[0].data = [];
                pieChart.options.plugins.title.text = 'Error loading data';
                pieChart.update();
            });
    }

    // Fetch initial data and create charts
    console.log('Fetching initial monthly data...');
    fetch('/finance/api/monthly-data/', fetchOptions)
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
                throw new Error('Session expired. Please log in again.');
            }
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to fetch monthly data');
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Received monthly data:', data);
            initializeCharts(data);
            initializePieChart();
        })
        .catch(error => {
            console.error('Error fetching monthly data:', error);
            alert('Error loading chart data: ' + error.message);
        });
}); 