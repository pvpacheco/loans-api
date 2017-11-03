import unittest
import dateutil.parser
from decimal import Decimal
from loan import Loan
from payment import Payment


class TestLoan(unittest.TestCase):

    # mock loan
    def setUp(self):
        self.loan = Loan(
            1,
            1000,
            12,
            0.05,
            "2017-08-05 02:18Z",
            [
                Payment(1, 'made', "2017-09-05 02:18Z", '85.60'),
                Payment(2, 'made', "2017-10-05 02:18Z", '85.60'),
                Payment(3, 'missed', "2017-11-05 02:18Z", '85.60'),
                Payment(4, 'made', "2017-12-05 02:18Z", '85.60')
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


if __name__ == '__main__':
    unittest.main()
