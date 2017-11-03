# Utilitary functions


class Utils(object):

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
