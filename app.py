#Imports like flask and sqlite
from flask import Flask, render_template, request, g
import sqlite3
from flask import Flask, render_template, request, g, session, redirect, jsonify

#identifying variable database and assinging value
app = Flask(__name__)
app.secret_key = 'fairwayfinds2025'
DATABASE = '/Users/quentin/Documents/GitHub/Level2FinalAssesment/database/fairway.db'



#Opens a connection and checks if there is allready one
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


#runs a querey and returns results
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# shuts the database when the app stops
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Home page linking
@app.route('/')
def home():
    featured = query_db('SELECT * FROM products LIMIT 3')
    return render_template('home.html', products=featured)


# Products page with search and filter
@app.route('/products')
def products():
    all_products = query_db('SELECT * FROM products')
    return render_template('products.html', products=all_products)
    
    # About page
@app.route('/about')
def about():
    return render_template('about.html')

    # Build query based on search and filter
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

# Product detail page linking
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = query_db('''
        SELECT products.*, brands.name as brand_name, categories.name as category_name
        FROM products
        JOIN brands ON products.brand_id = brands.brand_id
        JOIN categories ON products.category_id = categories.category_id
        WHERE products.product_id = ?
    ''', [product_id], one=True)
    return render_template('product_detail.html', product=product)


# Custom 404 page that handles errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Custom 505 error page
@app.errorhandler(500)
def internal_error(e):
    return render_template('505.html'), 500


if __name__ == '__main__':
    app.run(debug=True)





# View cart
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

# Add to cart - no page refresh
@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = query_db('SELECT * FROM products WHERE product_id = ?', [product_id], one=True)
    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            session.modified = True
            return jsonify({'success': True, 'message': 'Quantity updated'})
    cart.append({
        'product_id': product_id,
        'name': product['name'],
        'price': product['price'],
        'quantity': 1
    })
    session['cart'] = cart
    return jsonify({'success': True, 'message': 'Item added to cart'})

# Remove from cart - no page refresh
@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['product_id'] != product_id]
    return jsonify({'success': True, 'message': 'Item removed'})

# Update quantity - no page refresh
@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    data = request.get_json()
    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] = data['quantity']
            session.modified = True
    return jsonify({'success': True, 'message': 'Quantity updated'})