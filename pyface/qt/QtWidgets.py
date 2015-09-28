from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtGui import *

elif qt_api == 'pyqt5':
    from PyQt5.QtWidgets import *

else:
    from PySide.QtGui import *
