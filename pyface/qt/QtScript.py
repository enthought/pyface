from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtScript import *

elif qt_api == 'pyqt5':
    import warnings
    warnings.warn(DeprecationWarning("QtScript is not supported in PyQt5"))

elif qt_api == 'pyside2':
    import warnings
    warnings.warn(DeprecationWarning("QtScript is not supported in PyQt5"))

else:
    from PySide.QtScript import *
