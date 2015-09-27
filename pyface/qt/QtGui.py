from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.Qt import QKeySequence, QTextCursor
    from PyQt4.QtGui import *

elif qt_api == 'pyqt5':
    from PyQt5.Qt import QKeySequence, QTextCursor
    from PyQt5.QtGui import *
    
else:
    from PySide.QtGui import *
