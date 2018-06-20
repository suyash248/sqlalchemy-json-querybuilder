__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import itertools
from constants.error_codes import DBErrorCode
from pymysql.constants import ER

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

# Dict for mapping error code to error constant(name). e.g. 5001: 'SOME_ERROR_CONST'
__err_code_const_name_mapping__ = {getattr(ER, _, -1): _ for _ in __COMMON_ERR_CONSTANT_NAMES__}

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

def handle_db_errors(dbe):
    try:
        args = dbe.orig.args
        err_code = args[0]
        error_constant_name = __err_code_const_name_mapping__.get(err_code, DBErrorCode.NON_STANDARD_ERROR)
        error_constant = getattr(DBErrorCode, error_constant_name, DBErrorCode.NON_STANDARD_ERROR)
        err_msg = args[1]
        field_name = __extract_field__(err_msg)
        return Error(error_constant, field_name, message=err_msg).to_dict
    except Exception as ex:
        return Error(DBErrorCode.NON_STANDARD_ERROR, message=str(ex)).to_dict