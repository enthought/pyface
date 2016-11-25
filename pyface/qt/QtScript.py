from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtScript import *
    
elif qt_api == 'pyqt5':
    #from PyQt5.QtScript import *
    raise ImportError("QtScript not supported with qt_api='pyqt5'")
    
else:
    from PySide.QtScript import *
