import sqlite3
from flask import Flask, request, jsonify
import pyodbc
import json
import random
from flask import Flask
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# SQL Server connection string
server = r'DESKTOP-U0B648S\VICTUS'
database = 'victus_store'
username = 'sa'
password = '123'

# Create a connection string
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

# Create a cursor object
cursor = cnxn.cursor()
def dictify_row(row):
    """Convert a pyodbc row to a dictionary."""
    columns = [column[0] for column in cursor.description]  # Get column names
    return dict(zip(columns, row))

# API endpoint to create a new account
@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.json
    email = data['email']
    password = data['password']
    phone_num = data['phone_num']
    seller_account = data['seller_account']

    query = "INSERT INTO Accounts (email, password, phone_num, seller_account) VALUES (?, ?, ?, ?)"
    cursor.execute(query, email, password, phone_num, seller_account)
    cnxn.commit()

    return jsonify({'message': 'Account created successfully'}), 201

# API endpoint to get all accounts
@app.route('/accounts', methods=['GET'])
def get_accounts():
    query = "SELECT * FROM Accounts"
    cursor.execute(query)
    rows = cursor.fetchall()

    accounts = []
    for row in rows:
        account = {
            'email': row[0],
            'password': row[1],
            'phone_num': row[2],
            'seller_account': row[3]
        }
        accounts.append(account)

    return jsonify(accounts), 200

# API endpoint to get an account by email
@app.route('/accounts/<email>', methods=['GET'])
def get_account(email):
    query = "SELECT * FROM Accounts WHERE email = ?"
    cursor.execute(query, email)
    row = cursor.fetchone()

    if row:
        account = {
            'email': row[0],
            'password': row[1],
            'phone_num': row[2],
            'seller_account': row[3]
        }
        return jsonify(account), 200
    else:
        return jsonify({'message': 'Account not found'}), 404

# API endpoint to update an account
@app.route('/accounts/<email>', methods=['PUT'])
def update_account(email):
    data = request.json
    password = data['password']
    phone_num = data['phone_num']
    seller_account = data['seller_account']

    query = "UPDATE Accounts SET password = ?, phone_num = ?, seller_account = ? WHERE email = ?"
    cursor.execute(query, password, phone_num, seller_account, email)
    cnxn.commit()

    return jsonify({'message': 'Account updated successfully'}), 200

# API endpoint to delete an account
@app.route('/accounts/<email>', methods=['DELETE'])
def delete_account(email):
    query = "DELETE FROM Accounts WHERE email = ?"
    cursor.execute(query, email)
    cnxn.commit()

    return jsonify({'message': 'Account deleted successfully'}), 200

# API endpoint to create a new seller
@app.route('/sellers', methods=['POST'])
def create_seller():
    data = request.json
    seller_name = data['seller_name']
    email = data['email']

    # Check if the email already exists
    email_query = "SELECT * FROM Sellers WHERE email = ?"
    cursor.execute(email_query, (email,))
    existing_email = cursor.fetchone()

    if existing_email:
        return jsonify({'message': 'This email is already associated with a seller.'}), 400

    # Check if the seller name already exists
    name_query = "SELECT * FROM Sellers WHERE seller_name = ?"
    cursor.execute(name_query, (seller_name,))
    existing_name = cursor.fetchone()

    if existing_name:
        return jsonify({'message': 'This seller name is already used.'}), 400

    # If both checks pass, insert the new seller
    query = "INSERT INTO Sellers (seller_name, email) VALUES (?, ?)"
    cursor.execute(query, seller_name, email)
    cnxn.commit()

    return jsonify({'message': 'Seller created successfully'}), 201

# API endpoint to get all sellers
@app.route('/sellers', methods=['GET'])
def get_sellers():
    query = "SELECT * FROM Sellers"
    cursor.execute(query)
    rows = cursor.fetchall()

    sellers = []
    for row in rows:
        seller = {
            'seller_id': row[0],
            'seller_name': row[1],
            'email': row[2]
        }
        sellers.append(seller)

    return jsonify(sellers), 200

# API endpoint to get a seller by id
@app.route('/sellers/<seller_id>', methods=['GET'])
def get_seller(seller_id):
    query = "SELECT * FROM Sellers WHERE seller_id = ?"
    cursor.execute(query, seller_id)
    row = cursor.fetchone()

    if row:
        seller = {
            'seller_id': row[0],
            'seller_name': row[1],
            'email': row[2]
        }
        return jsonify(seller), 200
    else:
        return jsonify({'message': 'Seller not found'}), 404

# API endpoint to update a seller
@app.route('/sellers/<seller_id>', methods=['PUT'])
def update_seller(seller_id):
    data = request.json
    seller_name = data['seller_name']
    email = data 
    query = "UPDATE Sellers SET seller_name = ?, email = ? WHERE seller_id = ?"
    cursor.execute(query, seller_name, email, seller_id)
    cnxn.commit()

    return jsonify({'message': 'Seller updated successfully'}), 200

# API endpoint to delete a seller
@app.route('/sellers/<seller_id>', methods=['DELETE'])
def delete_seller(seller_id):
    query = "DELETE FROM Sellers WHERE seller_id = ?"
    cursor.execute(query, seller_id)
    cnxn.commit()

    return jsonify({'message': 'Seller deleted successfully'}), 200
@app.route('/check_account/<string:email>/<string:password>', methods=['GET'])
def check_account(email, password):
    # Step 1: Check if email exists
    email_query = "SELECT password, seller_account FROM Accounts WHERE email = ?"
    cursor.execute(email_query, (email,))
    row = cursor.fetchone()

    if row:
        stored_password = row[0]  # Get the stored password
        is_seller = row[1]  # Get the seller account flag (0 or 1)

        # Step 2: Check if the provided password matches the stored one
        if stored_password == password:
            return jsonify({'password': True, 'exists': True, 'is_seller': bool(is_seller)}), 200
        else:
            return jsonify({'password': False, 'exists': True}), 401
    else:
        return jsonify({'exists': False}), 404

    
# API endpoint to create a new category
@app.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    category_name = data['category_name']
    category_image = data['category_image']

    query = "INSERT INTO Categories (category_name, category_image) VALUES (?, ?)"
    cursor.execute(query, category_name, category_image)
    cnxn.commit()

    return jsonify({'message': 'Category created successfully'}), 201

# API endpoint to get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    query = "SELECT * FROM Categories"
    cursor.execute(query)
    rows = cursor.fetchall()

    categories = []
    for row in rows:
        category = {
            'category_id': row[0],
            'category_name': row[1],
            'category_image': row[2]
        }
        categories.append(category)

    return jsonify(categories), 200

# API endpoint to get a category by id
@app.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    query = "SELECT * FROM Categories WHERE category_id = ?"
    cursor.execute(query, category_id)
    row = cursor.fetchone()

    if row:
        category = {
            'category_id': row[0],
            'category_name': row[1],
            'category_image': row[2]
        }
        return jsonify(category), 200
    else:
        return jsonify({'message': 'Category not found'}), 404
# API endpoint to get all products of a specific category
@app.route('/categories/<category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    query = """
       SELECT p.product_id, p.product_name, p.description, p.price, p.stock_quantity, p.category_id, p.seller_id, i.image_url
    FROM Products p
    LEFT JOIN Images i ON p.product_id = i.product_id
    WHERE category_id = ?
    """
    cursor.execute(query, category_id)
    rows = cursor.fetchall()

    products = []
    for row in rows:
        product = {
          
            'product_id': row[0],
            'product_name': row[1],
            'description': row[2],
            'price': row[3],
            'stock_quantity': row[4],
            'category_id': row[5],
            'seller_id': row[6],
            'image_url': row[7]  # This is the image URL
        
        }
        products.append(product)

    return jsonify(products), 200
# API endpoint to update a category
@app.route('/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json
    category_name = data['category_name']
    category_image = data['category_image']

    query = "UPDATE Categories SET category_name = ?, category_image = ? WHERE category_id = ?"
    cursor.execute(query, category_name, category_image, category_id)
    cnxn.commit()

    return jsonify({'message': 'Category updated successfully'}), 200

# API endpoint to delete a category
@app.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    query = "DELETE FROM Categories WHERE category_id = ?"
    cursor.execute(query, category_id)
    cnxn.commit()

    return jsonify({'message': 'Category deleted successfully'}), 200

# API endpoint to create a new product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product_name = data['product_name']
    description = data['description']
    price = data['price']
    stock_quantity = data['stock_quantity']
    category_id = data['category_id']
    seller_id = data['seller_id']

    query = "INSERT INTO Products (product_name, description, price, stock_quantity, category_id, seller_id) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, product_name, description, price, stock_quantity, category_id, seller_id)
    cnxn.commit()

    return jsonify({'message': 'Product created successfully'}), 201

# API endpoint to get all products
@app.route('/products', methods=['GET'])
def get_products():
    query = """
    SELECT p.product_id, p.product_name, p.description, p.price, p.stock_quantity, p.category_id, p.seller_id, i.image_url
    FROM Products p
    LEFT JOIN Images i ON p.product_id = i.product_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    products = []
    for row in rows:
        product = {
            'product_id': row[0],
            'product_name': row[1],
            'description': row[2],
            'price': row[3],
            'stock_quantity': row[4],
            'category_id': row[5],
            'seller_id': row[6],
            'image_url': row[7]  # This is the image URL
        }
        products.append(product)

    return jsonify(products), 200

# API endpoint to get a product by id
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    query = "SELECT * FROM Products WHERE product_id = ?"
    cursor.execute(query, product_id)
    row = cursor.fetchone()

    if row:
        product = {
            'product_id': row[0],
            'product_name': row[1],
            'description': row[2],
            'price': row[3],
            'stock_quantity': row[4],
            'category_id': row[5],
            'seller_id': row[6]
        }
        return jsonify(product), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

# API endpoint to update a product
@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product_name = data['product_name']
    description = data['description']
    price = data['price']
    stock_quantity = data['stock_quantity']
    category_id = data['category_id']
    seller_id = data['seller_id']

    query = "UPDATE Products SET product_name = ?, description = ?, price = ?, stock_quantity = ?, category_id = ?, seller_id = ? WHERE product_id = ?"
    cursor.execute(query, product_name, description, price, stock_quantity, category_id, seller_id, product_id)
    cnxn.commit()

    return jsonify({'message': 'Product updated successfully'}), 200
# API endpoint to delete a product
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    query = "DELETE FROM Products WHERE product_id = ?"
    cursor.execute(query, product_id)
    cnxn.commit()

    return jsonify({'message': 'Product deleted successfully'}), 200

 # API endpoint to create a new image
@app.route('/images', methods=['POST'])
def create_image():
    data = request.json
    product_id = data['product_id']
    image_url = data['image_url']

    query = "INSERT INTO Images (product_id, image_url) VALUES (?, ?)"
    cursor.execute(query, product_id, image_url)
    cnxn.commit()

    return jsonify({'message': 'Image created successfully'}), 201

# API endpoint to get all images
@app.route('/images', methods=['GET'])
def get_images():
    query = "SELECT * FROM Images"
    cursor.execute(query)
    rows = cursor.fetchall()

    images = []
    for row in rows:
        image = {
            'image_id': row[0],
            'product_id': row[1],
            'image_url': row[2]
        }
        images.append(image)

    return jsonify(images), 200

# API endpoint to get an image by id
@app.route('/images/<image_id>', methods=['GET'])
def get_image(image_id):
    query = "SELECT * FROM Images WHERE image_id = ?"
    cursor.execute(query, image_id)
    row = cursor.fetchone()

    if row:
        image = {
            'image_id': row[0],
            'product_id': row[1],
            'image_url': row[2]
        }
        return jsonify(image), 200
    else:
        return jsonify({'message': 'Image not found'}), 404

# API endpoint to update an image
@app.route('/images/<image_id>', methods=['PUT'])
def update_image(image_id):
    data = request.json
    product_id = data['product_id']
    image_url = data['image_url']

    query = "UPDATE Images SET product_id = ?, image_url = ? WHERE image_id = ?"
    cursor.execute(query, product_id, image_url, image_id)
    cnxn.commit()

    return jsonify({'message': 'Image updated successfully'}), 200

# API endpoint to delete an image
@app.route('/images/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    query = "DELETE FROM Images WHERE image_id = ?"
    cursor.execute(query, image_id)
    cnxn.commit()

    return jsonify({'message': 'Image deleted successfully'}), 200

# API endpoint to create a new cart
@app.route('/cart', methods=['POST'])
def create_cart():
    data = request.json
    email = data['email']

    query = "INSERT INTO Cart (email) VALUES (?)"
    cursor.execute(query, email)
    cnxn.commit()

    return jsonify({'message': 'Cart created successfully'}), 201

# API endpoint to get all carts
@app.route('/cart', methods=['GET'])
def get_carts():
    query = "SELECT * FROM Cart"
    cursor.execute(query)
    rows = cursor.fetchall()

    carts = []
    for row in rows:
        cart = {
            'cart_id': row[0],
            'email': row[1]
        }
        carts.append(cart)

    return jsonify(carts), 200

# API endpoint to get a cart by id
@app.route('/cart/<cart_id>', methods=['GET'])
def get_cart(cart_id):
    query = "SELECT * FROM Cart WHERE cart_id = ?"
    cursor.execute(query, cart_id)
    row = cursor.fetchone()

    if row:
        cart = {
            'cart_id': row[0],
            'email': row[1]
        }
        return jsonify(cart), 200
    else:
        return jsonify({'message': 'Cart not found'}), 404


# API endpoint to update a cart
@app.route('/cart/<cart_id>', methods=['PUT'])
def update_cart(cart_id):
    data = request.json
    email = data['email']

    query = "UPDATE Cart SET email = ? WHERE cart_id = ?"
    cursor.execute(query, email, cart_id)
    cnxn.commit()

    return jsonify({'message': 'Cart updated successfully'}), 200

# API endpoint to delete a cart
@app.route('/cart/<cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    query = "DELETE FROM Cart WHERE cart_id = ?"
    cursor.execute(query, cart_id)
    cnxn.commit()

    return jsonify({'message': 'Cart deleted successfully'}), 200

# API endpoint to create a new order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    email = data['email']
    address = data['address']
    phone_num = data['phone_num']
    total_price = data['total_price']

    query = "INSERT INTO Orders (email, address, phone_num, total_price) VALUES (?, ?, ?, ?)"
    cursor.execute(query, email, address, phone_num, total_price)
    cnxn.commit()

    return jsonify({'message': 'Order created successfully'}), 201

# API endpoint to get all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    query = "SELECT * FROM Orders"
    cursor.execute(query)
    rows = cursor.fetchall()

    orders = []
    for row in rows:
        order = {
            'order_id': row[0],
            'email': row[1],
            'address': row[2],
            'phone_num': row[3],
            'total_price': row[4]
        }
        orders.append(order)

    return jsonify(orders), 200

# API endpoint to get an order by id
@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    query = "SELECT * FROM Orders WHERE order_id = ?"
    cursor.execute(query, order_id)
    row = cursor.fetchone()

    if row:
        order = {
            'order_id': row[0],
            'email': row[1],
            'address': row[2],
            'phone_num': row[3],
            'total_price': row[4]
        }
        return jsonify(order), 200
    else:
        return jsonify({'message': 'Order not found'}), 404

# API endpoint to update an order
@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    email = data['email']
    address = data['address']
    phone_num = data['phone_num']
    total_price = data['total_price']

    query = "UPDATE Orders SET email = ?, address = ?, phone_num = ?, total_price = ? WHERE order_id = ?"
    cursor.execute(query, email, address, phone_num, total_price, order_id)
    cnxn.commit()

    return jsonify({'message': 'Order updated successfully'}), 200

# API endpoint to delete an order
@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    query = "DELETE FROM Orders WHERE order_id = ?"
    cursor.execute(query, order_id)
    cnxn.commit()

    return jsonify({'message': 'Order deleted successfully'}), 200 # API endpoint to create a new cart product
@app.route('/cart-products', methods=['POST'])
def create_cart_product():
    data = request.json
    product_id = data['product_id']
    cart_id = data['cart_id']
    order_id = data['order_id']

    query = "INSERT INTO Cart_Products (product_id, cart_id, order_id) VALUES (?, ?, ?)"
    cursor.execute(query, product_id, cart_id, order_id)
    cnxn.commit()

    return jsonify({'message': 'Cart product created successfully'}), 201

# API endpoint to get all cart products
@app.route('/cart-products', methods=['GET'])
def get_cart_products():
    query = "SELECT * FROM Cart_Products"
    cursor.execute(query)
    rows = cursor.fetchall()

    cart_products = []
    for row in rows:
        cart_product = {
            'id': row[0],
            'product_id': row[1],
            'cart_id': row[2],
            'order_id': row[3]
        }
        cart_products.append(cart_product)

    return jsonify(cart_products), 200

# API endpoint to get a cart product by id
@app.route('/cart-products/<id>', methods=['GET'])
def get_cart_product(id):
    query = "SELECT * FROM Cart_Products WHERE id = ?"
    cursor.execute(query, id)
    row = cursor.fetchone()

    if row:
        cart_product = {
            'id': row[0],
            'product_id': row[1],
            'cart_id': row[2],
            'order_id': row[3]
        }
        return jsonify(cart_product), 200
    else:
        return jsonify({'message': 'Cart product not found'}), 404
    
@app.route('/cart/account/<string:email>', methods=['GET'])
def get_cart_for_account(email):
    query = """
    SELECT 
        c.cart_id,
        c.email,
        cp.id AS cart_product_id,
        cp.product_id,
        p.product_name,
        p.price,
        cp.order_id
    FROM 
        Cart c
    LEFT JOIN 
        Cart_Products cp ON c.cart_id = cp.cart_id
    LEFT JOIN 
        Products p ON cp.product_id = p.product_id
    WHERE 
        c.email = ?
    """
    cursor.execute(query, email)
    rows = cursor.fetchall()

    if rows:
        cart_details = []
        for row in rows:
            cart_item = {
                'cart_id': row.cart_id,
                'email': row.email,
                'cart_product_id': row.cart_product_id,
                'product_id': row.product_id,
                'product_name': row.product_name,
                'price': row.price,
                'order_id': row.order_id
            }
            cart_details.append(cart_item)
        return jsonify(cart_details), 200
    else:
        return jsonify({'message': 'Cart not found for this account'}), 404

# API endpoint to update a cart product
@app.route('/cart-products/<id>', methods=['PUT'])
def update_cart_product(id):
    data = request.json
    product_id = data['product_id']
    cart_id = data['cart_id']
    order_id = data['order_id']

    query = "UPDATE Cart_Products SET product_id = ?, cart_id = ?, order_id = ? WHERE id = ?"
    cursor.execute(query, product_id, cart_id, order_id, id)
    cnxn.commit()

    return jsonify({'message': 'Cart product updated successfully'}), 200

# API endpoint to delete a cart product
@app.route('/cart-products/<id>', methods=['DELETE'])
def delete_cart_product(id):
    query = "DELETE FROM Cart_Products WHERE id = ?"
    cursor.execute(query, id)
    cnxn.commit()

    return jsonify({'message': 'Cart product deleted successfully'}), 200 # API endpoint to create a new cart product with product details
@app.route('/cart-products-with-details', methods=['POST'])
def create_cart_product_with_details():
    data = request.json
    product_id = data['product_id']
    cart_id = data['cart_id']
    order_id = data['order_id']
    product_name = data['product_name']
    price = data['price']
    quantity = data['quantity']

    query = "INSERT INTO Cart_Products (product_id, cart_id, order_id, product_name, price, quantity) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, product_id, cart_id, order_id, product_name, price, quantity)
    cnxn.commit()

    return jsonify({'message': 'Cart product created successfully'}), 201

# API endpoint to get all cart products with details
@app.route('/cart-products-with-details', methods=['GET'])
def get_cart_products_with_details():
    query = "SELECT * FROM Cart_Products"
    cursor.execute(query)
    rows = cursor.fetchall()

    cart_products = []
    for row in rows:
        cart_product = {
            'id': row[0],
            'product_id': row[1],
            'cart_id': row[2],
            'order_id': row[3],
            'product_name': row[4],
            'price': row[5],
            'quantity': row[6]
        }
        cart_products.append(cart_product)

    return jsonify(cart_products), 200

# API endpoint to get a cart product with details by id
@app.route('/cart-products-with-details/<id>', methods=['GET'])
def get_cart_product_with_details(id):
    query = "SELECT * FROM Cart_Products WHERE id = ?"
    cursor.execute(query, id)
    row = cursor.fetchone()

    if row:
        cart_product = {
            'id': row[0],
            'product_id': row[1],
            'cart_id': row[2],
            'order_id': row[3],
            'product_name': row[4],
            'price': row[5],
            'quantity': row[6]
        }
        return jsonify(cart_product), 200
    else:
        return jsonify({'message': 'Cart product not found'}), 404

# API endpoint to update a cart product with details
@app.route('/cart-products-with-details/<id>', methods=['PUT'])
def update_cart_product_with_details(id):
    data = request.json
    product_id = data['product_id']
    cart_id = data['cart_id']
    order_id = data['order_id']
    product_name = data['product_name']
    price = data['price']
    quantity = data['quantity']

    query = "UPDATE Cart_Products SET product_id = ?, cart_id = ?, order_id = ?, product_name = ?, price = ?, quantity = ? WHERE id = ?"
    cursor.execute(query, product_id, cart_id, order_id, product_name, price, quantity, id)
    cnxn.commit()

    return jsonify({'message': 'Cart product updated successfully'}), 200

# API endpoint to delete a cart product with details
@app.route('/cart-products-with-details/<id>', methods=['DELETE'])
def delete_cart_product_with_details(id):
    query = "DELETE FROM Cart_Products WHERE id = ?"
    cursor.execute(query, id)
    cnxn.commit()

    return jsonify({'message': 'Cart product deleted successfully'}), 
import logging

logging.basicConfig(level=logging.DEBUG)
@app.route('/carts/<int:cart_id>/products', methods=['POST'])
def add_product_to_cart(cart_id):
    data = request.json
    logging.debug(f"Received request data: {data}")

    product_id = data.get('product_id')
    logging.debug(f"Extracted product_id: {product_id}")

    if not product_id or not isinstance(product_id, int):
        logging.error("Invalid or missing product_id")
        return jsonify({'error': 'Invalid or missing required field: product_id'}), 400

    try:
        cart_query = "SELECT cart_id FROM Cart WHERE cart_id = ?"
        cursor.execute(cart_query, (cart_id,))
        cart = cursor.fetchone()
        if not cart:
            logging.error("Cart not found")
            return jsonify({'error': 'Cart not found'}), 404

        product_query = "SELECT product_id FROM Products WHERE product_id = ?"
        cursor.execute(product_query, (product_id,))
        product = cursor.fetchone()
        if not product:
            logging.error("Product not found")
            return jsonify({'error': 'Product not found'}), 404

        existing_product_query = """
        SELECT quantity FROM Cart_Products WHERE cart_id = ? AND product_id = ?
        """
        cursor.execute(existing_product_query, (cart_id, product_id))
        existing_product = cursor.fetchone()

        if existing_product:
            update_query = """
            UPDATE Cart_Products SET quantity = quantity + 1 WHERE cart_id = ? AND product_id = ?
            """
            cursor.execute(update_query, (cart_id, product_id))
        else:
            insert_query = """
            INSERT INTO Cart_Products (cart_id, product_id, quantity) VALUES (?, ?, 1)
            """
            cursor.execute(insert_query, (cart_id, product_id))
        
        cnxn.commit()

        updated_cart_query = """
        SELECT 
            cp.cart_id,
            cp.product_id,
            p.product_name,
            p.price,
            SUM(cp.quantity) AS total_quantity,
            MAX(i.image_url) AS image_url
        FROM Cart_Products cp
        JOIN Products p ON cp.product_id = p.product_id
        LEFT JOIN Images i ON p.product_id = i.product_id
        WHERE cp.cart_id = ?
        GROUP BY cp.cart_id, cp.product_id, p.product_name, p.price
        """
        cursor.execute(updated_cart_query, (cart_id,))
        updated_cart = cursor.fetchall()

        cart_items = [
            {
                "cart_id": item[0],
                "product_id": item[1],
                "product_name": item[2],
                "price": float(item[3]),
                "quantity": item[4],
                "image_url": item[5] if item[5] else "https://via.placeholder.com/150"
            } for item in updated_cart
        ]

        return jsonify({'message': 'Product added to cart successfully', 'cart': cart_items}), 201

    except Exception as e:
        cnxn.rollback()
        logging.error(f"Error in add_product_to_cart: {str(e)}")
        return jsonify({'error': f'Failed to add product to cart: {str(e)}'}), 500

@app.route('/cart-products', methods=['DELETE'])
def remove_product_from_cart():
    data = request.json
    product_id = data['product_id']
    cart_id = data['cart_id']

    query = "DELETE FROM Cart_Products WHERE product_id = ? AND cart_id = ?"
    cursor.execute(query, product_id, cart_id)
    cnxn.commit()

    return jsonify({'message': 'Product removed from cart successfully'}), 200


# API endpoint to get all products in a cart
@app.route('/cart-products/<cart_id>', methods=['GET'])
def get_products_in_cart(cart_id):
    query = "SELECT * FROM Cart_Products WHERE cart_id = ?"
    cursor.execute(query, cart_id)
    rows = cursor.fetchall()

    products = []
    for row in rows:
        product = {
            'product_id': row[1],
            'cart_id': row[2]
        }
        products.append(product)

    return jsonify(products), 200

@app.route('/carts/get-or-create', methods=['POST'])
def get_or_create_cart():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Missing required field: email'}), 400

    try:
        # Check if the user already has a cart
        cart_query = "SELECT cart_id FROM Cart WHERE email = ?"
        cursor.execute(cart_query, (email,))
        cart = cursor.fetchone()

        if cart:
            # Convert the row to a dictionary
            cart_dict = dictify_row(cart)
            return jsonify({'cart_id': cart_dict['cart_id']}), 200

        # Create a new cart for the user
        insert_query = "INSERT INTO Cart (email) VALUES (?)"
        cursor.execute(insert_query, (email,))
        cnxn.commit()

        # Fetch the newly created cart ID
        cursor.execute(cart_query, (email,))
        new_cart = cursor.fetchone()

        # Convert the row to a dictionary
        new_cart_dict = dictify_row(new_cart)
        return jsonify({'cart_id': new_cart_dict['cart_id']}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

import random

# API endpoint to get 10 random products
@app.route('/products/random', methods=['GET'])
def get_random_products():
    try:
        # First, get the total number of products
        cursor.execute("SELECT COUNT(*) FROM Products")
        total_products = cursor.fetchone()[0]

        if total_products == 0:
            return jsonify({'message': 'No products available'}), 404

        # Determine how many products to fetch
        num_products_to_fetch = min(10, total_products)

        # Generate random indices
        random_indices = random.sample(range(total_products), num_products_to_fetch)

        # Fetch the products at the random indices
        products = []
        for index in random_indices:
            query = f"SELECT * FROM Products ORDER BY product_id OFFSET {index} ROWS FETCH NEXT 1 ROWS ONLY"
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                product = {
                    'product_id': row[0],
                    'product_name': row[1],
                    'description': row[2],
                    'price': row[3],
                    'stock_quantity': row[4],
                    'category_id': row[5],
                    'seller_id': row[6]
                }
                products.append(product)

        return jsonify(products), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/carts/account/<email>', methods=['GET'])
def get_carts_by_email(email):
    try:
        # Fetch the cart data for the given email
        cart_query = """
        SELECT 
            cp.cart_id,
            cp.product_id,
            p.product_name,
            p.price,
            cp.quantity,
            i.image_url
        FROM Cart_Products cp
        JOIN Products p ON cp.product_id = p.product_id
        LEFT JOIN Images i ON p.product_id = i.product_id
        WHERE cp.cart_id = (
            SELECT cart_id FROM Cart WHERE email = ?
        )
        """
        cursor.execute(cart_query, (email,))
        cart_items = cursor.fetchall()
        logging.debug(f"Fetched cart items: {cart_items}")

        # Format the cart data
        cart_list = []
        for item in cart_items:
            cart_list.append({
                "cart_id": item[0],
                "product_id": item[1],
                "product_name": item[2],
                "price": float(item[3]),  # Convert to float if necessary
                "quantity": item[4],
                "image_url": item[5] if item[5] else "https://via.placeholder.com/150"  # Default image if none exists
            })

        # Return the cart data
        return jsonify({
            'cart': cart_list
        }), 200

    except Exception as e:
        logging.error(f"Error in get_carts_by_email: {str(e)}")
        return jsonify({'error': f'Failed to fetch carts: {str(e)}'}), 500
@app.route('/cart-products', methods=['PUT'])
def update_product_quantity():
    data = request.json
    cart_id = data.get('cart_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Validate required fields
    if not cart_id or not product_id or not quantity:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Update the quantity in the database
        update_query = """
        UPDATE Cart_Products
        SET quantity = ?
        WHERE cart_id = ? AND product_id = ?
        """
        cursor.execute(update_query, (quantity, cart_id, product_id))
        cnxn.commit()

        return jsonify({'message': 'Product quantity updated successfully'}), 200
    except Exception as e:
        cnxn.rollback()
        return jsonify({'error': f'Failed to update product quantity: {str(e)}'}), 500
@app.route('/products/<int:product_id>/check-availability', methods=['GET'])
def check_product_availability(product_id):
    print(f"Checking availability for product {product_id}")
    try:
        query = "SELECT stock_quantity FROM Products WHERE product_id = ?"
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Product not found'}), 404

        available_quantity = result[0]
        print(f"Available quantity: {available_quantity}")
        return jsonify({'available_quantity': available_quantity}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Failed to check product availability: {str(e)}'}), 500

from flask import Flask, jsonify

@app.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return jsonify(routes), 200
if __name__ == '__main__':
    app.run(debug=True)
