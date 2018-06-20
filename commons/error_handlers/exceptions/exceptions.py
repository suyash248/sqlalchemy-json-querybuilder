__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from util.error_handlers.errors import Error

class BaseException(Exception):
    """
    Base class for custom error_handlers.
    Subclasses should provide `message` and `errors` properties.
    """
    message = 'Oops! Something went wrong.'
    errors = []

    def __init__(self, message=None, errors=()):
        self.errors = errors
        if message: self.message = message

    def __str__(self):
        return "Error: {}".format(self.message)

class DatabaseException(BaseException):
    message = 'Error occurred while performing database operation.'
    def __init__(self, message=None, errors=()):
        super(DatabaseException, self).__init__(message=message, errors=errors)

class SqlAlchemyException(DatabaseException):
    message = 'Error occurred while performing an operation on database.'
    def __init__(self, message=None, errors=()):
        # from thirdparty import db
        # db.session.rollback()
        message = message or self.message
        super(SqlAlchemyException, self).__init__(message=message, errors=errors)

class ExceptionBuilder(object):
    def __init__(self, exc_cls=BaseException):
        self._exc_cls = exc_cls
        self._errors = []
        self._message = ''

    def error(self, error_constant, *fields, message=None):
        self._errors.append(Error(error_constant, *fields, message=message).to_dict)
        return self

    def message(self, msg):
        self._message = msg
        return self

    def throw(self):
        raise self._exc_cls(errors=self._errors, message=self._message)


