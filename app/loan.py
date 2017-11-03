from validators import valid
from decimal import Decimal
from utils import Utils
import decimal


class Loan(object):

    def __init__(self, id, amount, term, rate, date, payments):
        self._id = valid.integer(id)
        self._amount = valid.decimal(amount)
        self._term = valid.integer(term)
        self._rate = valid.decimal(rate)
        self._date = valid.date(date)
        self._payments = valid.array_of_payments(payments)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = valid.integer(value)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = valid.decimal(value)

    @property
    def term(self):
        return self._term

    @term.setter
    def term(self, value):
        self._term = valid.integer(value)

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = valid.decimal(value)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = valid.date(value)

    @property
    def payments(self):
        return self._payments

    @payments.setter
    def payments(self, value):
        self._payments = valid.array_of_payments(value)

    def formated_id(self):
        return Utils.format_id(self._id)

    # Calculates loan installment
    #
    # Loan payment formula:
    # r = rate / 12.
    # Installment (monthly) = [ r + r / ( (1+r) ^ term - 1) ] x amount
    def installment(self):
        r = self.rate / 12
        calc = (r + r / ((1 + r) ** self.term - 1)) * self.amount
        return calc.quantize(Decimal('0.01'), decimal.ROUND_DOWN)

    # Calculates loan balance at specified date
    def balance(self, date):
        return self.total() - self.paid(date)

    # Calculates total amount due
    def total(self):
        return self.installment() * self.term

    # Calculates paid amount at specified date
    def paid(self, date):
        paid_amount = 0

        # order payments by date asc
        self.payments.sort(key=lambda obj: obj.date)

        for payment in self.payments:
            if(payment.date > date):
                break
            if(payment.payment == 'made'):
                paid_amount = paid_amount + payment.amount

        return paid_amount
