from . import qt_api

if qt_api == 'pyqt':
    from PyQt4.QtCore import *

    from PyQt4.QtCore import pyqtProperty as Property
    from PyQt4.QtCore import pyqtSignal as Signal
    from PyQt4.QtCore import pyqtSlot as Slot
    from PyQt4.Qt import QCoreApplication
    from PyQt4.Qt import Qt

    # forward compatability with Qt5
    from PyQt4.QtGui import QItemSelection, QItemSelectionModel

    __version__ = QT_VERSION_STR
    __version_info__ = tuple(map(int, QT_VERSION_STR.split('.')))

elif qt_api == 'pyqt5':
    from PyQt5.QtCore import *

    from PyQt5.QtCore import pyqtProperty as Property
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.Qt import QCoreApplication
    from PyQt5.Qt import Qt

    __version__ = QT_VERSION_STR
    __version_info__ = tuple(map(int, QT_VERSION_STR.split('.')))

else:
    try:
        from PySide import __version__, __version_info__
    except ImportError:
        pass
    from PySide.QtCore import *

    # forward compatibility with Qt5
    from PySide.QtGui import QItemSelection, QItemSelectionModel
