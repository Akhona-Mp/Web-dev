import sqlite3

# Connect to database (will create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create bikes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS bikes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    year INTEGER NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL
);
''')

# Insert sample bikes
cursor.execute('''
INSERT INTO bikes (name, brand, year, category, price, description, image)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    'Yamaha R6',
    'Yamaha',
    2022,
    'Sport',
    180000,
    'A high-performance sportbike built for speed and agility.',
    'yamaha_r6.jpg'
))

cursor.execute('''
INSERT INTO bikes (name, brand, year, category, price, description, image)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    'KTM Duke 390',
    'KTM',
    2021,
    'Naked',
    95000,
    'A powerful entry-level naked bike with a punchy engine.',
    'ktm_duke_390.jpg'
))

# Save and close
conn.commit()
conn.close()

print("Database setup complete.")
