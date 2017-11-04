import sqlite3
import os
import os.path


# loans test suit
class DatabaseManager(object):

    def create(self, name):
        # connecting to DB
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, name)
        conn = sqlite3.connect(db_path)

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

        # closing connection...
        conn.close()

    # note: will only remove tests.db
    def createTestsDb(self):
        self.create('tests.db')

    def destroyTestsDb(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'tests.db')
        os.remove(db_path)
