"""
Tee Time Golf Store Database Setup
File: setup_db.py
Author: Quentin Vacherand
Date: May 2026
Purpose: Creates the database tables and inserts all product category and brand data
"""
# imports
import sqlite3

# connects to database
conn = sqlite3.connect('/Users/quentin/Documents/GitHub/Level2FinalAssesment/database/fairway.db')
cursor = conn.cursor()

# categories table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE
    )
''')

# brands table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS brands (
        brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE,
        country VARCHAR(50)
    )
''')

# products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10,2) NOT NULL CHECK(price > 0),
        keywords VARCHAR(255) NOT NULL,
        image VARCHAR(255),
        description VARCHAR(255) DEFAULT NULL,
        category_id INTEGER,
        brand_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(category_id),
        FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
    )
''')

# adds categories
cursor.executemany('INSERT INTO categories (name) VALUES (?)', [
    ('Golf Balls',),
    ('Woods',),
    ('Irons',),
    ('Wedges',),
    ('Putters',),
    ('Accessories',),
    ('Clothing',),
    ('Bags',),
    ('Sets',)
])

# adds brands
cursor.executemany('INSERT INTO brands (name, country) VALUES (?, ?)', [
    ('Titleist', 'USA'),
    ('Callaway', 'USA'),
    ('TaylorMade', 'USA'),
    ('Ping', 'USA'),
    ('Mizuno', 'Japan'),
    ('Cleveland', 'USA'),
    ('Generic', 'NZ'),
])

# adds products
cursor.executemany('''
    INSERT INTO products (name, price, keywords, image, category_id, brand_id)
    VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('Golf Balls Dozen', 50, 'ball golf dozen accessories', 'golf_balls.jpg', 1, 1),
    ('Driver', 500, 'club driver woods 1 one 1wood', 'wood.jpg', 2, 2),
    ('3 Wood', 400, 'woods 3 three club 3wood', 'wood.jpg', 2, 3),
    ('5 Wood', 400, 'woods 5 five club 5wood', 'wood.jpg', 2, 3),
    ('7 Wood', 375, '7wood wood 7 seven club', 'wood.jpg', 2, 2),
    ('3 Iron', 250, '3iron iron club three', 'iron.jpg', 3, 5),
    ('4 Iron', 250, '4iron iron four club', 'iron.jpg', 3, 5),
    ('5 Iron', 250, '5iron iron five club', 'iron.jpg', 3, 5),
    ('6 Iron', 250, '6iron iron club six', 'iron.jpg', 3, 5),
    ('7 Iron', 250, '7iron iron club seven', 'iron.jpg', 3, 5),
    ('8 Iron', 200, 'iron club eight 8iron', 'iron.jpg', 3, 4),
    ('9 Iron', 200, 'iron 9 iron club nine', 'iron.jpg', 3, 4),
    ('Pitching Wedge', 150, 'Wedge Pitching club', 'wedge.jpg', 4, 6),
    ('Sand Wedge', 150, 'Sand Wedge club', 'wedge.jpg', 4, 6),
    ('Putter', 300, 'putter mallet club', 'putter.jpg', 5, 1),
    ('Tees', 10, 'tees wooden plastic accessories', 'tees.jpg', 6, 7),
    ('Golf Stand Bag', 300, 'bag stand sack carry', 'bag.jpg', 8, 2),
    ('Golf Cap', 40, 'cap hat clothing accessories', 'cap.jpg', 7, 7),
    ('Iron Set 3-SW', 1200, 'set iron wedge clubs', 'iron.jpg', 9, 5),
])

# saves and closes
conn.commit()
conn.close()
print("Database created successfully!")