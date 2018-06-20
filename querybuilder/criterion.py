__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from error_handlers.exceptions import SqlAlchemyException, ExceptionBuilder
from constants.error_codes import ErrorCode

class Criterion(object):
    """
    An instance of this class will represent one query criterion of many provided while filtering.
    query criterion is in following format::

        {
            "field_name": "first_name",
            "field_value": "abhi",
            "operator": "startswith"
        }

    Once `query criterion` is converted to an instance of this class, then `query_criterion` will be evaluated later.
    """
    def __init__(self, model_cls, field_name, field_value, operator_name):
        """
        Instantiate `Criterion` class and creates and instance of `Operator` by looking up operator class
        by `operator_name` under the `operators_mapping`.

        :param model_cls: Model class (NOT the instance)
        :param field_name: name of the field defined under `model_cls`
        :param field_value: value to be checked against the `field_name`
        :param operator_name: ``'notequals', 'lt', 'lte', 'gt', 'gte', 'like', 'ilike', 'startswith', 'istartswith',
                        'endswith', 'iendswith', 'contains', 'icontains', 'in', 'notin', 'isnull', 'isnotnull'``
        """
        try:
            from querybuilder.operators import operators_mapping
            operator_cls = operators_mapping[operator_name]
            self.operator = operator_cls(model_cls, field_name, field_value)
        except KeyError as ke:
            ExceptionBuilder(SqlAlchemyException).error(ErrorCode.INVALID_OPERATOR, operator_name).message(
                "Invalid operator {}".format(operator_name)
            ).throw()

    def eval(self):
        """Evaluates underlying criterion and returns SQLAlchemy expression, this expression will be used
            later inside ``model_cls.query.filter(*expressions)`` method.
        """
        return self.operator.expr()
