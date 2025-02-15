const apiUrl = 'http://127.0.0.1:5000'; // Ensure this matches your Flask API URL

// Create Account
document.getElementById('account-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const first_name = document.getElementById('first_name').value;
    const last_name = document.getElementById('last_name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const c_password = document.getElementById('password_con').value;
    const phone_num = document.getElementById('phone_num').value;
    const seller_account = document.getElementById('seller_account').checked;
if (password==c_password){
    fetch(`${apiUrl}/accounts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email ,password, phone_num, seller_account, first_name ,last_name, })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('account-message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error creating account:', error);
    });}else{
        document.getElementById('account-message').innerText = "Passwords do not match. Please try again.";
    }
});

// Fetch Accounts
document.getElementById('fetch-accounts')?.addEventListener('click', function() {
    fetch(`${apiUrl}/accounts`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const accountsList = document.getElementById('accounts-list');
        accountsList.innerHTML = ''; // Clear previous data
        data.forEach(account => {
            accountsList.innerHTML += `<ul class="account-info">
    <li><span class="bold-heading">Name:</span> ${account.last_name + " " + account.first_name}</li>
    <li><span class="bold-heading">Email:</span> ${account.email}</li>
    <li><span class="bold-heading">Phone:</span> ${account.phone_num}</li>
    <li><span class="bold-heading">Password:</span> ${account.password}</li>
    <li><span class="bold-heading">Seller Account:</span> ${account.seller_account ? 'Yes' : 'No'}</li>
</ul>`;
        });
    })
    .catch(error => {
        console.error('Error fetching accounts:', error);
        const accountsList = document.getElementById('accounts-list');
        accountsList.innerHTML = `<p class="account-info">Error fetching accounts: ${error.message}</p>`;
    });
});

// Create Product
document.getElementById('product-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const product_name = document.getElementById('product_name').value;
    const description = document.getElementById('description').value;
    const price = document.getElementById('price').value;
    const stock_quantity = document.getElementById('stock_quantity').value;
    const category_id = document.getElementById('category_id').value;
    const seller_id = document.getElementById('seller_id').value;

    fetch(`${apiUrl}/products`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_name, description, price, stock_quantity, category_id, seller_id })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('product-message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error creating product:', error);
    });
});

// Fetch Products
document.getElementById('fetch-products')?.addEventListener('click', function() {
    fetch(`${apiUrl}/products`)
    .then(response => response.json())
    .then(data => {
        const productsList = document.getElementById('products-list');
        productsList.innerHTML = ''; // Clear previous data
        data.forEach(product => {
            productsList.innerHTML += `<p>Product Name: ${product.product_name}, Price: $${product.price}</p>`;
        });
    })
    .catch(error => {
        console.error('Error fetching products:', error);
    });
});

// Create Order
document.getElementById('order-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const order_email = document.getElementById('order_email').value;
    const address = document.getElementById('address').value;
    const order_phone_num = document.getElementById('order_phone_num').value;
    const total_price = document.getElementById('total_price').value;

    fetch(`${apiUrl}/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: order_email, address, phone_num: order_phone_num, total_price })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('order-message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error creating order:', error);
    });
});

// Fetch Orders
document.getElementById('fetch-orders')?.addEventListener('click', function() {
    fetch(`${apiUrl}/orders`)
    .then(response => response.json())
    .then(data => {
        const ordersList = document.getElementById('orders-list');
        ordersList.innerHTML = ''; // Clear previous data
        data.forEach(order => {
            ordersList.innerHTML += `<p>Order ID: ${order.order_id}, Total Price: $${order.total_price}</p>`;
        });
    })
    .catch(error => {
        console.error('Error fetching orders:', error);
    });
});

// Create Seller
document.getElementById('seller-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const seller_name = document.getElementById('seller_name').value;
    const seller_email = document.getElementById('seller_email').value;

    fetch(`${apiUrl}/sellers`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ seller_name, email: seller_email })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('seller-message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error creating seller:', error);
    });
});

// Fetch Sellers
document.getElementById('fetch-sellers')?.addEventListener('click', function() {
    fetch(`${apiUrl}/sellers`)
    .then(response => response.json())
    .then(data => {
        const sellersList = document.getElementById('sellers-list');
        sellersList.innerHTML = ''; // Clear previous data
        data.forEach(seller => {
            sellersList.innerHTML += `<p>Seller Name: ${seller.seller_name}, Email: ${seller.email}</p>`;
        });
    })
    .catch(error => {
        console.error('Error fetching sellers:', error);
    });
});

// Create Category
document.getElementById('category-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const category_name = document.getElementById('category_name').value;
    const category_image = document.getElementById('category_image').value;

    fetch(`${apiUrl}/categories`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ category_name, category_image })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('category-message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error creating category:', error);
    });
});

// Fetch Categories
document.getElementById('fetch-categories')?.addEventListener('click', function() {
    fetch(`${apiUrl}/categories`)
    .then(response => response.json())
    .then(data => {
        const categoriesList = document.getElementById('categories-list');
        categoriesList.innerHTML = ''; // Clear previous data
        data.forEach(category => {
            categoriesList.innerHTML += `<p>Category Name: ${category.category_name}</p>`;
        });
    })
    .catch(error => {
        console.error('Error fetching categories:', error);
    });
});

// Create Image
document.getElementById('image-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const product_id = document.getElementById('image_product_id').value;
    const image_url = document.getElementById('image_url').value;

    fetch(`${apiUrl}/images`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id, image_url })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('image-message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error creating image:', error);
    });
});

// Fetch Images
document.getElementById('fetch-images')?.addEventListener('click', function() {
    fetch(`${apiUrl}/images`)
    .then(response => response.json())
    .then(data => {
        const imagesList = document.getElementById('images-list');
        imagesList.innerHTML = ''; // Clear previous data
        data.forEach(image => {
            imagesList.innerHTML += `<p>Image ID: ${image.image_id}, URL: ${image.image_url}</p>`;
        });
    })
    .catch(error => {
        console.error('Error fetching images:', error);
    });
});

// Create Cart
document.getElementById('cart-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('cart_email').value;

    fetch(`${apiUrl}/cart`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error creating cart:', error);
    });
});

// Fetch Carts
document.getElementById('fetch-carts')?.addEventListener('click', function() {
    fetch(`${apiUrl}/cart`)
    .then(response => response.json())
    .then(data => {
        const cartsList = document.getElementById('carts-list');
        cartsList.innerHTML = ''; // Clear previous data
        data.forEach(cart => {
            cartsList.innerHTML += `<p>Cart ID: ${cart.cart_id}, Email: ${cart.email}</p>`;
        });
    })
    .catch(error => {
        console.error('Error fetching carts:', error);
    });
});

// Create Cart Product
document.getElementById('cart-product-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const product_id = document.getElementById('cart_product_id').value;
    const cart_id = document.getElementById('cart_id').value;
    const order_id = document.getElementById('order_id').value;

    fetch(`${apiUrl}/cart-products`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id, cart_id, order_id })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-product-message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error creating cart product:', error);
    });
});

// Fetch Cart Products
document.getElementById('fetch-cart-products')?.addEventListener('click', function() {
    fetch(`${apiUrl}/cart-products`)
    .then(response => response.json())
    .then(data => {
        const cartProductsList = document.getElementById('cart-products-list');
        cartProductsList.innerHTML = ''; // Clear previous data
        data.forEach(cartProduct => {
            cartProductsList.innerHTML += `<p>Cart Product ID: ${cartProduct.id}, Product ID: ${cartProduct.product_id}</p>`;
        });
    })
    .catch(error => {
        console.error('Error fetching cart products:', error);
    });
});