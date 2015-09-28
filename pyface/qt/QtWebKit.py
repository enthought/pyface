from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtWebKit import *

elif qt_api == 'pyqt5':
    from PyQt5.QtWebKit import *
    
else:
    from PySide.QtWebKit import *
