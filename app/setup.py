import sqlite3

# connecting to DB
conn = sqlite3.connect('app/loans.db')

# defining cursor
cursor = conn.cursor()

# creating loans table
cursor.execute("""
    CREATE TABLE loans (
            loan_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            amount INTEGER NOT NULL,
            term INTEGER NOT NULL,
            rate INTEGER NOT NULL,
            dt TEXT NOT NULL
    );
""")

# creating payments table
cursor.execute("""
    CREATE TABLE payments (
            payment_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            loan_id INTEGER NOT NULL,
            type INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            dt TEXT NOT NULL,
            FOREIGN KEY(loan_id) REFERENCES loans(loan_id)
    );
""")

print('Loans DB created successfully.')

# closing connection...
conn.close()
