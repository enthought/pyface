from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtMultimediaWidgets import *

elif qt_api == 'pyqt5':
    from PyQt5.QtMultimediaWidgets import *

elif qt_api == 'pyside2':
    from PySide2.QtMultimediaWidgets import *

else:
    from PySide.QtMultimediaWidgets import *
