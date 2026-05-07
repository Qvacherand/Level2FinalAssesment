"""Fairway Finds web application - golf equipment store."""

import sqlite3
from flask import Flask, render_template, request, g, session, jsonify

app = Flask(__name__)
app.secret_key = 'fairwayfinds2025'
app.config['SESSION_TYPE'] = 'filesystem'
DATABASE = '/Users/quentin/Documents/GitHub/Level2FinalAssesment/database/fairway.db'

# Opens a connection and checks if there is already one
def get_db():
    """Opens a connection to the database and returns it."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Runs a query and returns results
def query_db(query, args=(), one=False):
    """Runs a SQL query and returns the results."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Shuts the database when the app stops
@app.teardown_appcontext
def close_connection(_exception):
    """Closes the database connection when the app stops."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Home page
@app.route('/')
def home():
    """Displays the home page with 3 featured products."""
    featured = query_db('SELECT * FROM products LIMIT 3')
    return render_template('home.html', products=featured)

# Products page with search and filter
@app.route('/products')
def products():
    """Displays all products with search and filter functionality."""
    search = request.args.get('search', '')
    selected_category = request.args.get('category', '')

    if search and selected_category:
        all_products = query_db('''
            SELECT * FROM products
            WHERE keywords LIKE ? AND category_id = ?
        ''', ['%' + search + '%', selected_category])
    elif search:
        all_products = query_db('''
            SELECT * FROM products
            WHERE keywords LIKE ?
        ''', ['%' + search + '%'])
    elif selected_category:
        all_products = query_db('''
            SELECT * FROM products
            WHERE category_id = ?
        ''', [selected_category])
    else:
        all_products = query_db('SELECT * FROM products')

    categories = query_db('SELECT * FROM categories')
    return render_template('products.html',
                           products=all_products,
                           categories=categories,
                           search=search,
                           selected_category=selected_category)

# About page
@app.route('/about')
def about():
    """Displays the about page."""
    return render_template('about.html')

# Product detail page
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Displays a single product with brand and category details."""
    product = query_db('''
        SELECT products.*, brands.name as brand_name, categories.name as category_name
        FROM products
        JOIN brands ON products.brand_id = brands.brand_id
        JOIN categories ON products.category_id = categories.category_id
        WHERE products.product_id = ?
    ''', [product_id], one=True)
    return render_template('product_detail.html', product=product)

# View cart
@app.route('/cart')
def cart():
    """Displays the cart page with all items and total price."""
    cart_items = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    return render_template('cart.html', cart=cart_items, total=total)

# Add to cart - no page refresh
@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Adds a product to the cart or increases quantity if already there."""
    product = query_db('SELECT * FROM products WHERE product_id = ?', [product_id], one=True)
    cart_items = session.get('cart', {})
    key = str(product_id)
    if key in cart_items:
        cart_items[key]['quantity'] += 1
    else:
        cart_items[key] = {
            'product_id': product_id,
            'name': product['name'],
            'price': float(product['price']),
            'quantity': 1
        }
    session['cart'] = cart_items
    session.modified = True
    return jsonify({'success': True, 'message': 'Added to cart'})

# Remove from cart - no page refresh
@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Removes a product from the cart."""
    cart_items = session.get('cart', {})
    key = str(product_id)
    if key in cart_items:
        del cart_items[key]
    session['cart'] = cart_items
    session.modified = True
    return jsonify({'success': True, 'message': 'Item removed'})

# Update quantity - no page refresh
@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    """Updates the quantity of a product in the cart."""
    data = request.get_json()
    cart_items = session.get('cart', {})
    key = str(product_id)
    if key in cart_items:
        cart_items[key]['quantity'] = data['quantity']
    session['cart'] = cart_items
    session.modified = True
    return jsonify({'success': True, 'message': 'Quantity updated'})

# Clears the cart session - used once to reset old cart data
@app.route('/cart/clear')
def clear_cart():
    """Clears all items from the cart session."""
    session.pop('cart', None)
    return 'Cart cleared! <a href="/">Go home</a>'

# Custom 404 page
@app.errorhandler(404)
def page_not_found(_e):
    """Displays a custom 404 error page."""
    return render_template('404.html'), 404

# Custom 500 error page
@app.errorhandler(500)
def internal_error(_e):
    """Displays a custom 500 error page."""
    return render_template('505.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
    