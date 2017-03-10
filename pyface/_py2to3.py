""" Helper module, providing a common API for tasks that require a different
implementation in python 2 and 3.
"""

import sys


if sys.version_info[0] < 3:
    str_types = (basestring,)
    text_type = unicode
    import __builtin__ as builtins
    xrange = xrange
else:
    str_types = (str,)
    text_type = str
    import builtins
    xrange = range
