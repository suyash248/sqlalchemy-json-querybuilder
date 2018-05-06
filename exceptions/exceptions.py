__author__ = "Suyash Soni"
__email__ = "suyash.soni@srijan.net"
__copyright__ = "Copyright 2018, Diversey"

from exceptions.ErrorCodes import ErrorCode

class Error(object):
    """
    Every time error needs to thrown, instance of this class must be used to represent an error.
    """
    def __init__(self, error_constant, *fields, message=None):
        self.error_constant = error_constant or ErrorCode.NON_STANDARD_ERROR
        self.fields = tuple(fields)
        self.message = message

    @property
    def to_dict(self):
        err_dict = dict(error_constant = self.error_constant)
        if self.fields: err_dict['fields'] = self.fields
        if self.message: err_dict['message'] = self.message
        return err_dict

class BaseException(Exception):
    """
    Base class for custom exceptions.
    Subclasses should provide `status_code`, `message` and `errors` properties.
    """
    status_code = 500
    message = 'A server error occurred.'
    errors = []

    def __init__(self, message=None, status_code=500, errors=()):
        self.status_code = status_code
        self.errors = errors
        if message: self.message = message

    def __str__(self):
        return "Error({}): {}".format(self.status_code, self.message)

class DatabaseException(BaseException):
    message = 'Error occurred while performing DB operation.'
    def __init__(self, message=None, status_code=400, errors=()):
        message = message or self.message
        super(DatabaseException, self).__init__(message=message, status_code=status_code, errors=errors)

class SqlAlchemyException(DatabaseException):
    message = 'Error occurred while performing an operation on RDBMS.'
    def __init__(self, message=None, status_code=400, errors=()):
        # Rollback transaction
        # db.session.rollback()
        message = message or self.message
        super(SqlAlchemyException, self).__init__(message=message, status_code=status_code, errors=errors)

class ExceptionBuilder(object):
    def __init__(self, exc_cls=BaseException):
        self._exc_cls = exc_cls
        self._errors = []
        self._message = ''
        self._code = None

    def error(self, error_constant, *fields, message=None):
        self._errors.append(Error(error_constant, *fields, message=message).to_dict)
        return self

    def message(self, msg):
        self._message = msg
        return self

    def status_code(self, code):
        self._code = code
        return self

    def throw(self):
        if self._code:
            raise self._exc_cls(errors=self._errors, message=self._message, status_code=self._code)
        else:
            raise self._exc_cls(errors=self._errors, message=self._message)