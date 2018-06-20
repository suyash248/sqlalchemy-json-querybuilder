"""
Function or class can be wrapped using **Callable** and can be called later(lazily) on. e.g.
    **Definition** -
        1. ca_func1 = Callable(callable='func_name', args=('arg1',), kwargs=dict(k1='v1'))
        2. ca_func2 = Callable(callable=func, args=('arg1',), kwargs=dict(k1='v1'))
        3. ca_cls1 = Callable(callable='SomeClass', args=('arg1',), kwargs=dict(k1='v1'))
        4. ca_cls2 = Callable(callable=SomeClass, args=('arg1',), kwargs=dict(k1='v1'))

    **Invocation** -
        1. ca_func1(obj=obj_of_func_class)        # **obj_of_func_class** is an object of class to which **func_name** belongs.
        2. ca_func1(module_name='some.module')    # **some.module** is a module in which **func_name** resides.
        3. ca_func2()
        4. ca_cls1(module_name='some.module')     # **some.module** is a module in which **SomeClass** resides.
        5. ca_cls2()

    Note: **args** & **kwargs** can also be provided at the time of invocation. e.g.:
            > `ca(module_name='some.module', args=(1, 'delhi`), kwargs={'country': 'India'})`

            > `ca(obj=obj_of_func_class, args=(1, 'delhi`), kwargs={'country': 'India'})`

"""

__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import importlib
from collections import namedtuple
from itertools import chain

Callable = namedtuple('Callable', 'callable module_name obj args kwargs')
Callable.__new__.__defaults__ = (None, None, None, (), {})

def _call_(self, module_name=None, obj=None, args=(), kwargs={}):
    args = chain(args, self.args)
    kwargs = {**kwargs, **self.kwargs}
    if type(self.callable) == str:
        module_name = module_name or self.module_name
        obj = obj or self.obj
        if module_name:
            module = importlib.import_module(module_name)
            # module.callable(*args, **kwargs)
            return getattr(module, self.callable)(*args, **kwargs)
        elif obj:
            # obj.callable(*args, **kwargs)
            return getattr(obj, self.callable)(*args, **kwargs)
    else:
        # callable(*args, **kwargs)
        return self.callable(*args, **kwargs)

Callable.__call__ = _call_
