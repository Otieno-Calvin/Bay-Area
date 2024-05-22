import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('delivery.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store delivery information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        id_no TEXT NOT NULL,
        package_type TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        transaction_code TEXT NOT NULL,
        delivery_from TEXT NOT NULL,
        delivery_to TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
