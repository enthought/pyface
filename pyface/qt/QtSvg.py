from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtSvg import *

elif qt_api == 'pyqt5':
    from PyQt5.QtSvg import *

else:
    from PySide.QtSvg import *
