__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import itertools
from sqlalchemy_json_querybuilder.constants.error_codes import DBErrorCode

class Error(object):
    """
    Every time error needs to thrown, instance of this class must be used to represent an error.
    """
    def __init__(self, error_constant, *fields, message=None):
        self.error_constant = error_constant or DBErrorCode.NON_STANDARD_ERROR
        self.fields = tuple(fields)
        self.message = message

    @property
    def to_dict(self):
        self.fields = tuple(itertools.chain(*map(lambda field: field.split('|'), self.fields)))
        err_dict = dict(error_constant = self.error_constant)
        if self.fields: err_dict['fields'] = self.fields
        if self.message: err_dict['message'] = self.message
        return err_dict


# Collection of error constants(only name) defined in ErrorCodes.py.
__COMMON_ERR_CONSTANT_NAMES__ = filter(lambda _: not _.startswith('_'), dir(DBErrorCode))


def __extract_field__(err_msg):
    try:
        stop_words_with_quote = {"doesn't", "don't", "won't", "can't", "shouldn't", "isn't", "aren't", "wouldn't"}

        # Remove `stop_words_with_quote` from err_msg
        for _ in stop_words_with_quote: err_msg = err_msg.replace(_, '')

        field_name = "Unknown"; sep = "'"
        while "'" in err_msg:
            field_name, sep, err_msg = err_msg.partition(sep)
        return field_name.strip()
    except Exception as ex:
        print(ex)
        return "Unknown"