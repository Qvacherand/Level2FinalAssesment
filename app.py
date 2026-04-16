#Imports such as flask and sqlite
from flask import Flask, render_template, request, g
import sqlite3

#identifying variable database and assinging value
app = Flask(__name__)
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
    search = request.args.get('search', '')
    selected_category = request.args.get('category', '')
    
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
    product = query_db('SELECT * FROM products WHERE product_id = ?', [product_id], one=True)
    return render_template('product_detail.html', product=product)


# Custom 404 page that handles errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
