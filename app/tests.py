import unittest
import dateutil.parser
from decimal import Decimal

from .loans.loan import Loan
from .loans.payment import Payment
from .loans.manager import LoansManager
from .db.manager import DatabaseManager

# mock loan data
loan_data = {
    'id': 1,
    'amount': Decimal('1000'),
    'term': 12,
    'rate': Decimal('0.05'),
    'date': '2017-08-05 02:18Z'
}


# loans test suit
class TestLoan(unittest.TestCase):

    # mock loan
    def setUp(self):
        self.loan = Loan(
            loan_data['id'],
            loan_data['amount'],
            loan_data['term'],
            loan_data['rate'],
            loan_data['date'],
            [
                Payment(1, 'made', '85.60', '2017-09-05 02:18Z'),
                Payment(2, 'made', '85.60', '2017-10-05 02:18Z'),
                Payment(3, 'missed', '85.60', '2017-11-05 02:18Z'),
                Payment(4, 'made', '85.60', '2017-12-05 02:18Z')
            ]
        )

    # assert correct installment amount
    def test_installment(self):
        self.assertEqual(self.loan.installment(), Decimal('85.60'))

    # assert correct balance amount
    def test_balance(self):
        self.assertEqual(
            self.loan.balance(dateutil.parser.parse('2017-08-05 02:18Z')),
            Decimal('1027.20')
        )
        self.assertEqual(
            self.loan.balance(dateutil.parser.parse('2017-09-05 02:18Z')),
            Decimal('941.60')
        )
        self.assertEqual(
            self.loan.balance(dateutil.parser.parse('2017-10-05 02:18Z')),
            Decimal('856')
        )
        self.assertEqual(
            self.loan.balance(dateutil.parser.parse('2017-11-05 02:18Z')),
            Decimal('856')
        )
        self.assertEqual(
            self.loan.balance(dateutil.parser.parse('2017-12-05 02:18Z')),
            Decimal('770.40')
        )
        self.assertEqual(
            self.loan.balance(dateutil.parser.parse('2018-01-05 02:18Z')),
            Decimal('770.40')
        )


# loans manager test suit
class TestLoanManager(unittest.TestCase):

    def setUp(self):
        # creating tests.db
        self.db_name = '../db/tests.db'
        database_manager = DatabaseManager()
        database_manager.createTestsDb()

    def tearDown(self):
        # destroying tests.db
        database_manager = DatabaseManager()
        database_manager.destroyTestsDb()

    # assert correct loan creation
    def test_createLoan(self):
        loan_manager = LoansManager()
        loan_manager.db_name = self.db_name
        loan = loan_manager.createLoan(
            loan_data['amount'],
            loan_data['term'],
            loan_data['rate'],
            loan_data['date']
        )

        self.assertIsInstance(loan, Loan)
        self.assertEqual(loan.amount, loan_data['amount'])

    # assert correct loan loading
    def test_loadLoan(self):
        loan_manager = LoansManager()
        loan_manager.db_name = self.db_name
        loan = loan_manager.createLoan(
            loan_data['amount'],
            loan_data['term'],
            loan_data['rate'],
            loan_data['date']
        )
        loan2 = loan_manager.loadById(loan.id)

        self.assertEqual(loan2.id, 1)
        self.assertEqual(loan2.amount, loan_data['amount'])
        self.assertEqual(loan2.term, loan_data['term'])
        self.assertEqual(loan2.rate, loan_data['rate'])
        self.assertEqual(loan2.date, dateutil.parser.parse(loan_data['date']))

    # assert correct loan payment recording
    def test_recordPayment(self):
        loan_manager = LoansManager()
        loan_manager.db_name = self.db_name
        loan = loan_manager.createLoan(
            loan_data['amount'],
            loan_data['term'],
            loan_data['rate'],
            loan_data['date']
        )

        payment_id = loan_manager.recordPayment(
            loan.id,
            'made',
            Decimal('85.60'),
            '2017-09-05 02:18Z'
        )
        self.assertEqual(payment_id, 1)


if __name__ == '__main__':
    unittest.main()
