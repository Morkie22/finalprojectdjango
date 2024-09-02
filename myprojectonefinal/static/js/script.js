$(document).ready(function () {
    const products = [
        { id: 1, name: 'Arepa', price: 10.00, img: 'img/product1.jpeg', description: 'Description for product 1' },
        { id: 2, name: 'Pandebono', price: 15.00, img: 'img/product2.jpeg', description: 'Description for product 2' },
        { id: 3, name: 'Empanada', price: 20.00, img: 'img/product3.jpeg', description: 'Description for product 3' }
    ];

    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let currentUser = null;

    // Function to render products on the main page
    function renderProducts(productsToShow) {
        const productContainer = $('#products');
        productContainer.empty();
        productsToShow.forEach(product => {
            const productHtml = `
                <div class="col-md-4">
                    <div class="card mb-4">
                        <img src="${product.img}" class="card-img-top" alt="${product.name}">
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <p class="card-text">$${product.price.toFixed(2)}</p>
                            <button class="btn btn-primary add-to-cart" data-id="${product.id}">Add to Cart</button>
                            <a href="product.html?id=${product.id}" class="btn btn-secondary view-details" data-id="${product.id}">View Details</a>
                        </div>
                    </div>
                </div>
            `;
            productContainer.append(productHtml);
        });
    }

    // Function to render the items in the cart
    function renderCart() {
        const cartContainer = $('#cart-items');
        cartContainer.empty();
        if (cart.length > 0) {
            cart.forEach(item => {
                const cartItemHtml = `
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <img src="${item.img}" class="img-thumbnail mr-3" alt="${item.name}" style="width: 50px;">
                        ${item.name} - $${item.price.toFixed(2)}
                        <button class="btn btn-danger btn-sm remove-from-cart" data-id="${item.id}">Remove</button>
                    </li>
                `;
                cartContainer.append(cartItemHtml);
            });
            const checkoutButtonHtml = `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <button class="btn btn-success btn-lg btn-block" id="checkout-button">Checkout</button>
                </li>
            `;
            cartContainer.append(checkoutButtonHtml);
            $('#cart-count').text(cart.length);
        } else {
            $('#cart-count').text(0);
        }
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    // Add a product to the cart
    function addToCart(id) {
        const product = products.find(p => p.id === id);
        if (product) {
            cart.push(product);
            renderCart();
        }
    }

    // Remove a product from the cart
    function removeFromCart(id) {
        cart = cart.filter(item => item.id !== id);
        renderCart();
    }

    // Search products by name
    function searchProducts(query) {
        const filteredProducts = products.filter(product => product.name.toLowerCase().includes(query.toLowerCase()));
        renderProducts(filteredProducts);
    }

    // Navigate to the product details page
    function navigateToProductDetails(id) {
        history.pushState({ page: 'product', id: id }, '', `product.html?id=${id}`);
        renderProductDetails(id);
    }

    // Render product details on the product page
    function renderProductDetails(id) {
        const product = products.find(p => p.id === id);

        if (product) {
            const productDetailsHtml = `
                <div class="row">
                    <div class="col-md-6">
                        <img src="${product.img}" class="img-fluid" alt="${product.name}">
                    </div>
                    <div class="col-md-6">
                        <h3>${product.name}</h3>
                        <p>$${product.price.toFixed(2)}</p>
                        <p>${product.description}</p>
                        <button class="btn btn-primary add-to-cart" data-id="${product.id}">Add to Cart</button>
                    </div>
                </div>
            `;
            $('#product-details').html(productDetailsHtml);
        }
    }

    // Simulate checkout process
    function checkout() {
        alert('Checkout successful!');
        cart = [];
        renderCart();
    }

    // Event Handlers
    $(document).on('click', '.add-to-cart', function () {
        const id = $(this).data('id');
        addToCart(id);
    });

    $(document).on('click', '.remove-from-cart', function () {
        const id = $(this).data('id');
        removeFromCart(id);
    });

    $(document).on('click', '.view-details', function (event) {
        event.preventDefault();
        const id = $(this).data('id');
        navigateToProductDetails(id);
    });

    $(document).on('click', '#checkout-button', function () {
        checkout();
    });

    $('#search').on('input', function () {
        const query = $(this).val();
        searchProducts(query);
    });

    $('#cart-icon').on('click', function () {
        window.location.href = 'cart.html';
    });

    // Handle back navigation
    window.onpopstate = function (event) {
        if (event.state && event.state.page === 'product') {
            renderProductDetails(event.state.id);
        } else {
            renderProducts(products);
        }
    };

    // Initial Rendering based on the page
    if ($('#products').length) {
        renderProducts(products);
    }

    if ($('#product-details').length) {
        const urlParams = new URLSearchParams(window.location.search);
        const productId = parseInt(urlParams.get('id'));
        renderProductDetails(productId);
    }

    if ($('#cart-page').length) {
        renderCart();
    }

    // Simulate user sign-up and login processes
    if ($('#signup-form').length) {
        $('#signup-form').on('submit', function (event) {
            event.preventDefault();
            alert('User signed up successfully!');
            window.location.href = 'login.html';
        });
    }

    if ($('#login-form').length) {
        $('#login-form').on('submit', function (event) {
            event.preventDefault();
            currentUser = { username: $('#username-email').val() };
            alert('User logged in successfully!');
            window.location.href = 'index.html';
        });
    }
});

