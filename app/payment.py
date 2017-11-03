from .validators import valid


class Payment(object):

    def __init__(self, id, payment, date, amount):
        self._id = valid.integer(id)
        self._payment = valid.payment_type(payment)
        self._date = valid.date(date)
        self._amount = valid.decimal(amount)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = valid.integer(value)

    @property
    def payment(self):
        return self._payment

    @payment.setter
    def payment(self, value):
        self._payment = valid.payment_type(value)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = valid.date(value)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = valid.decimal(value)
