from manager import DatabaseManager

db = DatabaseManager()
db.create('loans.db')

print('Loans DB created successfully.')
