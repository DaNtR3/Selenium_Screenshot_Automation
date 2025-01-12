document.addEventListener('DOMContentLoaded', function() {
    fetchCart();

    // Function to update button states based on cart items
    function updateButtonStates(cart) {
        cart.security_systems.forEach(item => {
            const selectButton = document.getElementById(`select-security_systems-${item.id}`);
            const removeButton = document.getElementById(`remove-security_systems-${item.id}`);
            if (selectButton && removeButton) {
                selectButton.disabled = true;
                removeButton.disabled = false;
            }
        });

        cart.endpoints.forEach(item => {
            const selectButton = document.getElementById(`select-endpoints-${item.id}`);
            const removeButton = document.getElementById(`remove-endpoints-${item.id}`);
            if (selectButton && removeButton) {
                selectButton.disabled = true;
                removeButton.disabled = false;
            }
        });
    }
    

    // Function to show a toast notification and conditionally reload the page
    function showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
        }, 100); // Delay to allow CSS transition

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
                // Reload the page only if the current page is cart.html
                if (window.location.pathname === '/views/cart') {
                    location.reload();
                }
            }, 300); // Delay to allow CSS transition
        }, 3000); // Display duration
    }

    // Fetch the cart items from the server
        function fetchCart() {
            fetch('/views/get_cart')
            .then(response => {
                console.log(response);  // Log the response to see its status and details
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(cart => {
                console.log(cart);  // Log the cart data
                updateButtonStates(cart);
            })
            .catch(error => {
                console.error('Error fetching cart data:', error);
            });
    }

     // Function to add an item to the cart
     function addToCart(key, category, name, displayname, connectionkey, connectionname) {
        console.log('Adding to cart:', name);

        // Check if the item is already in the cart
        fetch('/views/get_cart')
        
            .then(response => response.json())
            .then(cart => {
                let isInCart = false;
                if (category === 'security_systems') {
                    isInCart = cart.security_systems.some(item => item.id === key);
                } else if (category === 'endpoints') {
                    isInCart = cart.endpoints.some(item => item.id === key);
                }

                if (isInCart) {
                    showToast('Item is already in the cart', 'error');
                } else {
                    // Disable the select button and enable the remove button for the item
                    const selectButton = document.getElementById(`select-${category}-${key}`);
                    const removeButton = document.getElementById(`remove-${category}-${key}`);
                    
                    if (selectButton && removeButton) {
                        selectButton.disabled = true;  // Disables the select button
                        removeButton.disabled = false;  // Enables the remove button
                    } else {
                        console.error('Buttons not found for item:', name);
                    }

                    const payload = { key: key, category: category, name: name, displayname: displayname, connectionkey: connectionkey, connectionname: connectionname };
                    console.log(JSON.stringify(payload));
                    // Send AJAX request to add item to cart
                    fetch('/views/add_to_cart', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(payload)
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.message);
                        showToast(data.message, 'success');
                    })
                    .catch(error => {
                        console.error('Error adding item to cart:', error);
                        showToast('Error adding item to cart', 'error');
                    });
                }
            })
            .catch(error => {
                console.error('Error checking cart items:', error);
            });
    }

    // Function to remove an item from the cart
    function removeFromCart(key, category, name) {
        console.log('Removing from cart:', name);

        // Check if the item is in the cart
        fetch('/views/get_cart')
            .then(response => response.json())
            .then(cart => {
                let isInCart = false;
                if (category === 'security_systems') {
                    isInCart = cart.security_systems.some(item => item.id === key);
                } else if (category === 'endpoints') {
                    isInCart = cart.endpoints.some(item => item.id === key);
                }

                if (!isInCart) {
                    showToast('Item not found in the cart', 'error');
                } else {
                    // Enable the select button and disable the remove button for the item
                    const selectButton = document.getElementById(`select-${category}-${key}`);
                    const removeButton = document.getElementById(`remove-${category}-${key}`);
                    
                    if (selectButton && removeButton) {
                        selectButton.disabled = false;  // Enables the select button
                        removeButton.disabled = true;  // Disables the remove button
                    } else {
                        console.error('Buttons not found for item:', name);
                    }

                    const payload = { key: key, name: name, category: category };
                    console.log(JSON.stringify(payload));
                    // Send AJAX request to remove item from cart
                    fetch('/views/remove_from_cart', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(payload)
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.message);
                        showToast(data.message, 'success');
                    })
                    .catch(error => {
                        console.error('Error removing item from cart:', error);
                        showToast('Error removing item from cart', 'error');
                    });
                }
            })
            .catch(error => {
                console.error('Error checking cart items:', error);
            });
    }

    
    // Function to submit the cart data
    function submitCart() {
        const submitButton = document.getElementById('submit-request');
        submitButton.disabled = true; // Disable the submit button

        fetch('/views/get_cart')
            .then(response => response.json())
            .then(cart => {
                const payload = {
                    security_systems: cart.security_systems,
                    endpoints: cart.endpoints
                };
                console.log('Submitting cart:', payload);
                // Send AJAX request to submit the cart
                fetch('/views/submit_cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                    showToast(data.message, 'success');
                })
                .catch(error => {
                    console.error('Error submitting cart:', error);
                    showToast('Error submitting cart', 'error');
                })
                .finally(() => {
                    setTimeout(() => {
                    submitButton.disabled = false; // Re-enable the submit button
                    }, 3500);
                });
            })
            .catch(error => {
                console.error('Error fetching cart items:', error);
                submitButton.disabled = false; // Re-enable the submit button in case of error
            });
    }

    // Function to clear the cart
    function clearCart() {
        const clearButton = document.getElementById('clear-cart');
        clearButton.disabled = true; // Disable the clear button

        fetch('/views/clear_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            showToast(data.message, 'success');
        })
        .catch(error => {
            console.error('Error clearing cart:', error);
            showToast('Error clearing cart', 'error');
        })
        .finally(() => {
            setTimeout(() => {
                clearButton.disabled = false; // Re-enable the clear button after a delay
            }, 3500); 
        });
    }


    // Add event listener to the submit button
    const submitButton = document.getElementById('submit-request');
    if (submitButton) {
        submitButton.addEventListener('click', submitCart);
    }

    // Add event listener to the clear button
    const clearButton = document.getElementById('clear-cart');
    if (clearButton) {
        clearButton.addEventListener('click', clearCart);
    }


    // Expose functions to the global scope
    window.addToCart = addToCart;
    window.removeFromCart = removeFromCart;

});