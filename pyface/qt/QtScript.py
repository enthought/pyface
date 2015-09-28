from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtScript import *

elif qt_api == 'pyqt5':
    from PyQt5.QtScript import *
    
else:
    from PySide.QtScript import *
