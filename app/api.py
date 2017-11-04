from flask_restful import Resource, reqparse
from flask_restful import HTTPException

from .loans.manager import LoansManager
from .utils import Valid, Formatter


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
ApiErrors = {
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
        return Valid.decimal(value)
    except Exception:
        raise InvalidDecimalError


# custom positive integer validation
def valid_integer(value):
    try:
        return Valid.integer(value)
    except Exception:
        raise InvalidIntegerError


# custom positive decimal validation
def valid_date(value):
    try:
        return Valid.date(value)
    except Exception:
        raise InvalidDateError


class LoansApi(Resource):

    def get(self):
        raise NotAllowedError

    def post(self):

        # parsing arguments
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

        # loading manager and creating new loan
        loans_manager = LoansManager()
        loan = loans_manager.createLoan(
            args.amount,
            args.term,
            args.rate,
            args.date
        )

        # returns json result
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

        # loading loan
        loans_manager = LoansManager()
        loan = loans_manager.loadById(Formatter.unformat_id(loan_id))

        if (loan is None):
            raise LoanNotFoundError
            return

        # registering payment
        loans_manager = LoansManager()
        payment_id = loans_manager.recordPayment(
            Formatter.unformat_id(loan_id),
            args.payment,
            args.amount,
            args.date
        )

        if (payment_id < 1):
            raise LoanNotFoundError
            return
        else:
            return {
                "payment": args.payment,
                "date": args.date,
                "amount": '{0:.2f}'.format(args.amount)
            }


class BalanceApi(Resource):

    def post(self, loan_id):

        # parsing arguments
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('date', type=str, required=True, location='json')
        args = parser.parse_args(strict=True)
        args.date = valid_date(args.date)

        # loading loan
        loans_manager = LoansManager()
        loan = loans_manager.loadById(Formatter.unformat_id(loan_id))

        # returns json result
        return {"balance": '{0:.2f}'.format(loan.balance(args.date))}
