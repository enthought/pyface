from qtpy import PYQT4, PYQT5, PYSIDE

if PYQT4:
    from PyQt4.QtWebKit import *

elif PYQT5:
    from PyQt5.QtWebKitWidgets import *
    
elif PYSIDE:
    from PySide.QtWebKit import *

else:
    raise ImportError('Unknown qt api')
