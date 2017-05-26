from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtOpenGL import *
#- Use elif instead of a new if, otherwise will throw error --> PyQt4 will never be used  
elif qt_api == 'pyqt5':
    from PyQt5.QtOpenGL import *

else:
    from PySide.QtOpenGL import *
