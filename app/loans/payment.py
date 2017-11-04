from ..utils import Valid


class Payment(object):

    def __init__(self, id, payment, amount, date):
        self._id = Valid.integer(id)
        self._payment = Valid.payment_type(payment)
        self._date = Valid.date(date)
        self._amount = Valid.decimal(amount)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = Valid.integer(value)

    @property
    def payment(self):
        return self._payment

    @payment.setter
    def payment(self, value):
        self._payment = Valid.payment_type(value)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = Valid.date(value)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = Valid.decimal(value)
