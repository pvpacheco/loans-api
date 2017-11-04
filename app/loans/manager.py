import os.path
from sqlalchemy import create_engine

from .loan import Loan
from .payment import Payment


# main loan managing functions
class LoansManager(object):

    def __init__(self):

        self.db_name = '../db/loans.db'

    def init(self):

        # setup db connection
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, self.db_name)
        self.db_connect = create_engine('sqlite:///' + db_path)

    def createLoan(self, amount, term, rate, date):

        # connect to database
        self.init()
        conn = self.db_connect.connect()

        # creating loan
        query = conn.execute('''
                INSERT INTO loans(amount, term, rate, dt)
                VALUES(?, ?, ?, ?)''', (
                    int(amount*100),
                    int(term),
                    int(rate*100),
                    date
                )
            )

        query = conn.execute('SELECT LAST_INSERT_ROWID()')
        loan_id = query.cursor.fetchall()[0][0]
        conn.close()

        return self.loadById(loan_id)

    def recordPayment(self, loan_id, payment, amount, date):

        # connect to database
        self.init()
        conn = self.db_connect.connect()

        # recording payment
        conn.execute('PRAGMA foreign_keys = ON')
        query = conn.execute('''
                INSERT INTO payments(loan_id, type, amount, dt)
                VALUES(?, ?, ?, ?)''', (
                    loan_id,
                    1 if (payment == 'made') else 2,
                    int(amount*100),
                    date
                )
            )

        query = conn.execute('SELECT LAST_INSERT_ROWID()')
        payment_id = query.cursor.fetchall()[0][0]
        conn.close()

        return payment_id

    def loadById(self, loan_id):

        # connect to database
        self.init()
        conn = self.db_connect.connect()

        # return loan
        query_loan = conn.execute('''
            SELECT
                loan_id,
                amount,
                term,
                rate,
                dt
            FROM loans
            WHERE loan_id = {}
        '''.format(loan_id))

        # return all loans
        query_payments = conn.execute('''
            SELECT
                payment_id,
                type,
                amount,
                dt
            FROM payments
            WHERE loan_id = {}
        '''.format(loan_id))

        loan_data = query_loan.cursor.fetchall()
        loan_payments_data = query_payments.cursor.fetchall()
        loan_payments_list = []

        conn.close()

        # raising error if loan was not found
        if (len(loan_data) < 1):
            return None

        # loading classes
        loan = Loan(
            loan_data[0][0],
            loan_data[0][1]/100,
            loan_data[0][2],
            loan_data[0][3]/100,
            loan_data[0][4],
            []
        )

        for data in loan_payments_data:
            loan_payments_list.append(Payment(
                data[0],
                'made' if (data[1] == 1) else 'missed',
                data[2]/100,
                data[3]
            ))

        loan.payments = loan_payments_list

        return loan
