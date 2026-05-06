import sqlite3

# Connect to the database folder and creates the file since it doesnt exist before
conn = sqlite3.connect('/Users/quentin/Documents/GitHub/Level2FinalAssesment/database/fairway.db')
cursor = conn.cursor()

# Creates Categories table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE
    )
''')

# Creates Brands table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS brands (
        brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE,
        country VARCHAR(50)
    )
''')
# Inserts brands
cursor.executemany('INSERT INTO brands (name, country) VALUES (?, ?)', [
    ('Titleist', 'USA'),
    ('Callaway', 'USA'),
    ('TaylorMade', 'USA'),
    ('Ping', 'USA'),
    ('Mizuno', 'Japan'),
    ('Cleveland', 'USA'),
    ('Generic', 'NZ'),
])

# Creates Products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10,2) NOT NULL CHECK(price > 0),
        keywords VARCHAR(255) NOT NULL,
        image VARCHAR(255),
        featured INTEGER DEFAULT 0,
        category_id INTEGER,
        brand_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(category_id),
        FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
    )
''')
# Inserts categories
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

# Inserts products
cursor.executemany('''
    INSERT INTO products (name, price, keywords, image, category_id, brand_id)
    VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('Golf Balls Dozen', 50, 'ball golf dozen accessories', 'golf_balls.jpg', 1, 1),
    ('Driver', 500, 'club driver woods 1 one 1wood', 'driver.jpg', 2, 2),
    ('3 Wood', 400, 'woods 3 three club 3wood', '3wood.jpg', 2, 3),
    ('5 Wood', 400, 'woods 5 five club 5wood', '5wood.jpg', 2, 3),
    ('7 Wood', 375, '7wood wood 7 seven club', '7wood.jpg', 2, 2),
    ('3 Iron', 250, '3iron iron club three', '3iron.jpg', 3, 5),
    ('4 Iron', 250, '4iron iron four club', '4iron.jpg', 3, 5),
    ('5 Iron', 250, '5iron iron five club', '5iron.jpg', 3, 5),
    ('6 Iron', 250, '6iron iron club six', '6iron.jpg', 3, 5),
    ('7 Iron', 250, '7iron iron club seven', '7iron.jpg', 3, 5),
    ('8 Iron', 200, 'iron club eight 8iron', '8iron.jpg', 3, 4),
    ('9 Iron', 200, 'iron 9 iron club nine', '9iron.jpg', 3, 4),
    ('Pitching Wedge', 150, 'Wedge Pitching club', 'pw.jpg', 4, 6),
    ('Sand Wedge', 150, 'Sand Wedge club', 'sw.jpg', 4, 6),
    ('Putter', 300, 'putter mallet club', 'putter.jpg', 5, 1),
    ('Tees', 10, 'tees wooden plastic accessories', 'tees.jpg', 6, 7),
    ('Golf Stand Bag', 300, 'bag stand sack carry', 'bag.jpg', 8, 2),
    ('Golf Cap', 40, 'cap hat clothing accessories', 'cap.jpg', 7, 7),
    ('Iron Set 3-SW', 1200, 'set iron wedge clubs', 'iron_set.jpg', 9, 5),
])
#closes program
conn.commit()
conn.close()