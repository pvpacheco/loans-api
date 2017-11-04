# Utilitary functions
import dateutil.parser
from decimal import Decimal


class Valid(object):

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


class Formatter(object):

    # convert id (int) to format 000-0000-0000-0000
    def format_id(value):
        fid = '{0:015d}'.format(value)
        return '{}-{}-{}-{}'.format(
            fid[0:3],
            fid[3:7],
            fid[7:11],
            fid[11:15]
        )

    # convert id 000-0000-0000-0000 to int
    def unformat_id(value):
        return int(value.replace("-", ""))
