import os.path
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_restful import HTTPException
from sqlalchemy import create_engine

from .loan import Loan
from .payment import Payment
from .validators import valid
from .utils import Utils


# custom api validation errors
class InvalidDecimalError(HTTPException):
    code = 400


class InvalidIntegerError(HTTPException):
    code = 400


class InvalidDateError(HTTPException):
    code = 400


class LoanNotFoundError(HTTPException):
    code = 400


class NotAllowedError(HTTPException):
    code = 400


# custom error messages
errors = {
    'InvalidDecimalError': {
        'message': "Invalid positive decimal format.",
    },
    'InvalidIntegerError': {
        'message': "Invalid positive integer format.",
    },
    'InvalidDateError': {
        'message': "Invalid date format. Must be an ISO 8601 string.",
    },
    'LoanNotFoundError': {
        'message': "Loan not found.",
    },
    'NotAllowedError': {
        'message': (
            "The method is not allowed for the requested URL. "
            "Please follow the instructions at "
            "https://documenter.getpostman.com/view/3076044/loans-api/77h6P84"
        )
    },
}


# custom positive decimal validation
def valid_decimal(value):
    try:
        return valid.decimal(value)
    except Exception:
        raise InvalidDecimalError


# custom positive integer validation
def valid_integer(value):
    try:
        return valid.integer(value)
    except Exception:
        raise InvalidIntegerError


# custom positive decimal validation
def valid_date(value):
    try:
        return valid.date(value)
    except Exception:
        raise InvalidDateError


# setup db connection and API initialization
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "loans.db")
db_connect = create_engine('sqlite:///' + db_path)

app = Flask(__name__)
api = Api(app, errors=errors)


class LoansApi(Resource):

    def get(self):
        raise NotAllowedError

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('amount', type=str, required=True, location='json')
        parser.add_argument('term', type=int, required=True, location='json')
        parser.add_argument('rate', type=str, required=True, location='json')
        parser.add_argument('date', type=str, required=True, location='json')

        args = parser.parse_args(strict=True)

        args.amount = valid_decimal(args.amount)
        args.term = valid_integer(args.term)
        args.rate = valid_decimal(args.rate)
        valid_date(args.date)

        # connect to database
        conn = db_connect.connect()
        query = conn.execute('''
                INSERT INTO loans(amount, term, rate, dt)
                VALUES(?, ?, ?, ?)''', (
                    int(args.amount*100),
                    int(args.term),
                    int(args.rate*100),
                    args.date
                )
            )

        query = conn.execute('SELECT LAST_INSERT_ROWID()')
        loan_id = query.cursor.fetchall()[0][0]
        loan = Loan(
                loan_id,
                args.amount,
                args.term,
                args.rate,
                args.date,
                []
            )

        conn.close()

        return {
                "loan_id": loan.formated_id(),
                "installment": str(loan.installment())
            }


class PaymentsApi(Resource):

    def post(self, loan_id):

        # parsing arguments
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
                'payment',
                type=str,
                required=True,
                location='json',
                choices=('made', 'missed')
            )
        parser.add_argument('amount', type=str, required=True, location='json')
        parser.add_argument('date', type=str, required=True, location='json')

        args = parser.parse_args(strict=True)

        args.amount = valid_decimal(args.amount)
        valid_date(args.date)

        # connect to database
        conn = db_connect.connect()
        conn.execute('PRAGMA foreign_keys = ON')
        query = conn.execute('''
                INSERT INTO payments(loan_id, type, amount, dt)
                VALUES(?, ?, ?, ?)''', (
                    Utils.unformat_id(loan_id),
                    1 if (args.payment == 'made') else 2,
                    int(args.amount*100),
                    args.date
                )
            )

        query = conn.execute('SELECT LAST_INSERT_ROWID()')
        payment_id = query.cursor.fetchall()[0][0]
        payment = Payment(
                payment_id,
                args.payment,
                args.date,
                args.amount
            )

        conn.close()

        return {
                "payment": payment.payment,
                "date": args.date,
                "amount": '{0:.2f}'.format(payment.amount)
            }


class BalanceApi(Resource):

    def post(self, loan_id):

        # parsing arguments
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('date', type=str, required=True, location='json')

        args = parser.parse_args(strict=True)

        args.date = valid_date(args.date)

        # connect to database
        conn = db_connect.connect()

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
                '''.format(Utils.unformat_id(loan_id)))

        # return all loans
        query_payments = conn.execute('''
                    SELECT
                        payment_id,
                        type,
                        dt,
                        amount
                    FROM payments
                    WHERE loan_id = {}
                '''.format(Utils.unformat_id(loan_id)))

        loan_data = query_loan.cursor.fetchall()
        loan_payments_data = query_payments.cursor.fetchall()
        loan_payments_list = []

        conn.close()

        # raising error if loan was not found
        if (len(loan_data) < 1):
            raise LoanNotFoundError
            return

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
                    data[2],
                    data[3]/100
                ))

        loan.payments = loan_payments_list

        # returns json result
        return {"balance": '{0:.2f}'.format(loan.balance(args.date))}


# Route 1
# POST /loans
# Summary: creates a loan application. Loans are automatically accepted.
api.add_resource(LoansApi, '/loans')

# Route 2
# POST /loans/<:id>/payments
# Summary: creates a record of a payment made or missed.
api.add_resource(PaymentsApi, '/loans/<loan_id>/payments')

# Route 3
# POST /loans/<:id>/balance
# Summary: get the volume of outstanding debt
# (i.e., debt yet to be paid) at some point in time.
api.add_resource(BalanceApi, '/loans/<loan_id>/balance')


if __name__ == '__main__':
    app.run()
