__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import importlib
import types
from collections import OrderedDict
from constants.error_codes import ErrorCode
from util.callable import Callable

def load_class(fully_qualified_class_name):
    """
    Dynamically loads/imports a class by it's fully qualified name.

    Note - It returns class **type**, NOT the instance of class.

    Usage -
            `my_class = load_class('my_package.my_module.MyClass')`

            `my_class_obj = my_class()`

    """
    class_data = fully_qualified_class_name.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    return getattr(module, class_str)

def get_fully_qualified_classname(cls=None, obj=None):
    """
    Returns `fully-qualified-name` of the class represented by **cls** or **obj**

    :param cls:
    :param obj:
    :return:
    """
    if obj:
        module = obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return obj.__class__.__name__
        return module + '.' + obj.__class__.__name__
    elif cls:
        module = cls.__module__
        if module is None or module == str.__class__.__module__:
            return cls.__name__
        return module + '.' + cls.__name__

def _deserialize_one_(model_obj, *args, fields=(), deserializer=None, **kwargs):
    """
    Deserialize a model instance/object to `OrderedDict` containing `fields` as keys.

    :param model_obj: Model instance that needs to be deserialized.
    :param fields: Model object *fields'* names, which will be part of deserialized `OrderedDict`. If *fields* are not
                    specified then all the fields(as returned by `record.to_dict()` method) will be part of
                    deserialized `OrderedDict`.
    :param deserializer: Can be any one of following -

            1. **Function** - A function which will accept model object as an arg and returns a dict.
            2. **String** - name of the function defined under model class and returns a dict.
            3. **Callable** - Wraps function along with args & kwargs. Defined under services.commons.callable.

    :return: Deserialized dict.
    """
    if model_obj is None:
        return None
    try:
        model_dict = None
        deserializer = deserializer or 'to_dict'
        if type(deserializer) == str:
            model_dict = getattr(model_obj, deserializer, 'to_dict')(*args, **kwargs)
        elif isinstance(deserializer, (Callable,)):
            model_dict = deserializer(obj=model_obj)
        elif isinstance(deserializer, (types.FunctionType,)):
            model_dict = deserializer(model_obj, *args, **kwargs)
        else:
            model_dict = model_obj.to_dict(*args, **kwargs)
        all_fields_dict = model_dict
        return OrderedDict((f, all_fields_dict[f]) for f in fields) if len(fields) > 0 else OrderedDict(all_fields_dict)
    except KeyError as ke:
        # TODO - ErrorHandler
        pass
        # ExceptionBuilder().error(ErrorCode.INVALID_FIELD, 'unknown', message=str(ke)).throw()

def deserialize(data, fields=(), deserializer=None, *args, **kwargs):
    """
    Deserialize model instance or list of model instance(s) to `OrderedDict` or list of `OrderedDict` containing
    `fields` as keys.

    :param data: model object or collection(list, set, tuple) of model objects.
    :param fields: Model object *fields*, which will be part of deserialized `OrderedDict`. If *fields* are not
                    specified then all the fields(as returned by `record.to_dict()` method) will be part of
                    deserialized `OrderedDict`.
    :param deserializer: Can be any one of following -

            1. **Function** - A function which will accept model object as an arg and returns a dict.
            2. **String** - name of the function defined under model class and returns a dict.
            3. **Callable** - Wraps function along with args & kwargs. Defined under services.commons.callable.

    :return: Deserialized object or
    """
    try:
        if isinstance(data, (list, set, tuple)):
            return list(map(lambda _: _deserialize_one_(_, *args, fields=fields, deserializer=deserializer, **kwargs), data))
        else:
            return _deserialize_one_(data, fields=fields, *args, **kwargs)
    except AttributeError as ae:
        pass
        # TODO - ErrorHandler
        # ExceptionBuilder().error(ErrorCode.INVALID_DATA_TYPE, 'unknown', message=str(ae)).throw()

def xdeserialize(records, fields=(), deserializer=None, *args, **kwargs):
    """
    To deserialize model instance or list of model instance(s) to deserialized `OrderedDict(s)` and yield them one-by-one.

    :param records: model object or collection(list, set, tuple) of model objects.
    :param fields: Model object *fields*, which will be part of deserialized `OrderedDict`. If *fields* are not
                    specified then all the fields(as returned by `record.to_dict()` method) will be part of
                    deserialized `OrderedDict`.
    :param deserializer: Can be any one of following -

            1. **Function** - A function which will accept model object as an arg and returns a dict.
            2. **String** - name of the function defined under model class and returns a dict.
            3. **Callable** - Wraps function along with args & kwargs. Defined under services.commons.callable.

    :return: Generator, which yield deserialized version of model object in the form of `OrderedDict`
    """
    if not isinstance(records, (list, tuple)):
        records = [records]
    try:
        for rec in records:
            yield _deserialize_one_(rec, *args, fields=fields, deserializer=deserializer, **kwargs)
    except AttributeError as ae:
        pass
        # TODO - ErrorHandler
        # ExceptionBuilder().error(ErrorCode.INVALID_DATA_TYPE, 'unknown', message=str(ae)).throw()