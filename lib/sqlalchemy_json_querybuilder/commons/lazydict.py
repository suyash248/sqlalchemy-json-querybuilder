__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from collections import Mapping
from ..commons.callable import Callable

class LazyDict(Mapping):
    """
    Lazy dictionary, value will be initialized once corresponding key is accessed. e.g.

    ld = LazyDict({
        'k': expensive_to_construct_func
    })

    **expensive_to_construct_func** function will be executed only if `k` is accessed(ld.get('k') or ld['k'])
    """
    def __init__(self, *args, **kw):
        self._raw_dict = dict(*args, **kw)

    def __getitem__(self, key):
        val = self._raw_dict.__getitem__(key)
        if isinstance(val, (Callable,)):
            return val()
        else:
            pass
        return self._raw_dict.__getitem__(key)

    def __iter__(self):
        return iter(self._raw_dict)

    def __len__(self):
        return len(self._raw_dict)