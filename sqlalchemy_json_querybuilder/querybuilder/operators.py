__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from sqlalchemy_json_querybuilder.commons.error_handlers.exceptions.exceptions import ExceptionBuilder, SqlAlchemyException
from sqlalchemy_json_querybuilder.constants.error_codes import ErrorCode

class Operator(object):
    """Represents an operator"""
    def __init__(self, model_cls, field_name, field_value):
        self.model_cls = model_cls
        self.field_name = field_name
        self.field_value = field_value

    def expr(self):
        """Evaluates criterion and returns expression to be used inside `model_cls.query.filter(*expressions)` method.
        Concrete operator classes must override this method."""
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_OPERATOR, self.field_name,
                    message="Invalid operator").throw()
    @property
    def model_field(self):
        try:
            return getattr(self.model_cls, self.field_name)
        except:
            ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_FIELD, self.field_name,
                message="Couldn't find {} under {}".format(self.field_name, self.model_cls.__name__)).throw()

class Equals(Operator):
    def expr(self):
        return self.model_field == self.field_value

class NotEquals(Operator):
    def expr(self):
        return self.model_field != self.field_value

class LessThan(Operator):
    def expr(self):
        if isinstance(self.field_value, (int, float)):
            return self.model_field < self.field_value
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
            message="field_value must be number(int, float)").throw()

class LessThanEq(Operator):
    def expr(self):
        if isinstance(self.field_value, (int, float)):
            return self.model_field <= self.field_value
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                        message="field_value must be number(int, float)").throw()

class GreaterThan(Operator):
    def expr(self):
        if isinstance(self.field_value, (int, float)):
            return self.model_field > self.field_value
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                        message="field_value must be number(int, float)").throw()

class GreaterThanEq(Operator):
    def expr(self):
        if isinstance(self.field_value, (int, float)):
            return self.model_field >= self.field_value
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                        message="field_value must be number(int, float)").throw()

class IN(Operator):
    def expr(self):
        try:
            iter(self.field_value)
        except TypeError as te:
            ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                            message="field_value must be iterable").throw()
        return self.model_field.in_(self.field_value)

class NotIn(Operator):
    def expr(self):
        try:
            iter(self.field_value)
        except TypeError as te:
            ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                            message="field_value must be iterable").throw()
        return ~self.model_field.in_(self.field_value)

class IsNull(Operator):
    def expr(self):
        return self.model_field.is_(None)

class IsNotNull(Operator):
    def expr(self):
        return self.model_field.isnot(None)

class Like(Operator):
    def expr(self):
        return self.model_field.like(self.field_value)

class ILike(Operator):
    def expr(self):
        return self.model_field.ilike(self.field_value)

class StartsWith(Like):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = self.field_value + '%'
            return super(StartsWith, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class IStartsWith(ILike):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = self.field_value + '%'
            return super(IStartsWith, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                message="field_value must be string").throw()

class EndsWith(Like):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = '%' + self.field_value
            return super(EndsWith, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class IEndsWith(ILike):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = '%' + self.field_value
            return super(IEndsWith, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class Contains(Like):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = '%' + self.field_value + '%'
            return super(Contains, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class IContains(ILike):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = '%' + self.field_value + '%'
            return super(IContains, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class Any(Operator):
    def expr(self):
        return self.model_field.any(self.field_value)

class Has(Operator):
    def expr(self):
        return self.model_field.has(self.field_value)

# Maps `operator_name` to corresponding 'operator` class.
operators_mapping = {
    'equals': Equals,
    'notequals': NotEquals,
    'lt': LessThan,
    'lte': LessThanEq,
    'gt': GreaterThan,
    'gte': GreaterThanEq,
    'like': Like,
    'ilike': ILike,
    'startswith': StartsWith,
    'istartswith': IStartsWith,
    'endswith': EndsWith,
    'iendswith': IEndsWith,
    'contains': Contains,
    'icontains': IContains,
    'in': IN,
    'notin': NotIn,
    'isnull': IsNull,
    'isnotnull': IsNotNull,
    'any': Any,
    'has': Has
}