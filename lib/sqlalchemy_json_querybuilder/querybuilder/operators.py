__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from ..commons.error_handlers.exceptions.exceptions import ExceptionBuilder, SqlAlchemyException
from ..constants.error_codes import ErrorCode

class OperatorEvaluator(object):
    """Represents an operator"""
    def __init__(self, model_cls, field_name, field_value):
        self.model_cls = model_cls
        self.field_name = field_name
        self.field_value = field_value

    @staticmethod
    def obj(operator_name, model_cls, field_name, field_value):
        operator_name = operator_name.lower()
        try:
            op_eval_cls = __OPERATORS_MAPPING__[operator_name]
            return op_eval_cls(model_cls, field_name, field_value)
        except:
            ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_OPERATOR, operator_name,
                    message="Invalid operator: {}".format(operator_name)).throw()

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

class __Equals__(OperatorEvaluator):
    def expr(self):
        return self.model_field == self.field_value

class __NotEquals__(OperatorEvaluator):
    def expr(self):
        return self.model_field != self.field_value

class __LessThan__(OperatorEvaluator):
    def expr(self):
        return self.model_field < self.field_value

class __LessThanEq__(OperatorEvaluator):
    def expr(self):
        return self.model_field <= self.field_value

class __GreaterThan__(OperatorEvaluator):
    def expr(self):
        return self.model_field > self.field_value

class __GreaterThanEq__(OperatorEvaluator):
    def expr(self):
        return self.model_field >= self.field_value

class __IN__(OperatorEvaluator):
    def expr(self):
        try:
            iter(self.field_value)
        except TypeError as te:
            ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                            message="field_value must be iterable").throw()
        return self.model_field.in_(self.field_value)

class __NotIn__(OperatorEvaluator):
    def expr(self):
        try:
            iter(self.field_value)
        except TypeError as te:
            ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                            message="field_value must be iterable").throw()
        return ~self.model_field.in_(self.field_value)

class __IsNull__(OperatorEvaluator):
    def expr(self):
        return self.model_field.is_(None)

class __IsNotNull__(OperatorEvaluator):
    def expr(self):
        return self.model_field.isnot(None)

class __Like__(OperatorEvaluator):
    def expr(self):
        return self.model_field.like(self.field_value)

class __ILike__(OperatorEvaluator):
    def expr(self):
        return self.model_field.ilike(self.field_value)

class __StartsWith__(__Like__):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = self.field_value + '%'
            return super(__StartsWith__, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class __IStartsWith__(__ILike__):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = self.field_value + '%'
            return super(__IStartsWith__, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                message="field_value must be string").throw()

class __EndsWith__(__Like__):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = '%' + self.field_value
            return super(__EndsWith__, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class __IEndsWith__(__ILike__):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = '%' + self.field_value
            return super(__IEndsWith__, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class __Contains__(__Like__):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = '%' + self.field_value + '%'
            return super(__Contains__, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class __IContains__(__ILike__):
    def expr(self):
        if type(self.field_value) == str:
            self.field_value = '%' + self.field_value + '%'
            return super(__IContains__, self).expr()
        ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                                                    message="field_value must be string").throw()

class __Match__(OperatorEvaluator):
    def expr(self):
        return self.model_field.match(self.field_value)

class __Any__(OperatorEvaluator):
    def expr(self):
        return self.model_field.any(self.field_value)

class __Has__(OperatorEvaluator):
    def expr(self):
        return self.model_field.has(self.field_value)

# Maps `operator_name` to corresponding 'operator` class.
__OPERATORS_MAPPING__ = {
    'equals': __Equals__,
    'eq': __Equals__,
    '==': __Equals__,

    'notequals': __NotEquals__,
    'not_equals': __NotEquals__,
    'ne': __NotEquals__,
    '!=': __NotEquals__,
    '~=': __NotEquals__,

    'less_than': __LessThan__,
    'lt': __LessThan__,
    '<': __LessThan__,

    'less_than_equals': __LessThanEq__,
    'lte': __LessThanEq__,
    '<=': __LessThanEq__,

    'greater_than': __GreaterThan__,
    'gt': __GreaterThan__,
    '>': __GreaterThan__,

    'greater_than_equals': __GreaterThanEq__,
    'gte': __GreaterThanEq__,
    '>=': __GreaterThanEq__,

    'like': __Like__,
    'ilike': __ILike__,
    'startswith': __StartsWith__,
    'istartswith': __IStartsWith__,
    'endswith': __EndsWith__,
    'iendswith': __IEndsWith__,
    'contains': __Contains__,
    'icontains': __IContains__,

    'match': __Match__,

    'in': __IN__,
    'notin': __NotIn__,

    'isnull': __IsNull__,
    'isnotnull': __IsNotNull__,

    'any': __Any__,
    'has': __Has__
}