import dateutil.parser
from decimal import Decimal


class valid(object):

    def integer(value):
        if isinstance(value, int) or str(value).isdigit():
            value = int(value)

            if value > 0:
                return int(value)

        raise TypeError('`{}` not a valid positive integer'.format(value))

    def decimal(value):
        try:
            value = Decimal(str(value))
            if value > 0:
                return value
            else:
                raise TypeError(
                    '`{}` not a valid positive decimal'.format(value)
                )
        except ValueError:
            raise TypeError('`{}` not a valid positive'.format(value))

    def date(value):
        try:
            return dateutil.parser.parse(value)
        except ValueError:
            raise TypeError('`{}` not a valid date'.format(value))

    def payment_type(value):
        if value in ('made', 'missed'):
            return value
        else:
            raise TypeError('`{}` not a valid payment type'.format(value))

    def array_of_payments(value):
        return value
