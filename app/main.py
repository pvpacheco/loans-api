from flask import Flask
from flask_restful import Api
from .api import ApiErrors, LoansApi, PaymentsApi, BalanceApi

# Loading API and creating routes
app = Flask(__name__)
api = Api(app, errors=ApiErrors)

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
