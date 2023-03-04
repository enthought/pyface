# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
from . import qt_api

if qt_api == "pyqt5":
    from PyQt5.QtCore import *

    from PyQt5.QtCore import pyqtProperty as Property
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.Qt import QCoreApplication
    from PyQt5.Qt import Qt

    __version__ = QT_VERSION_STR
    __version_info__ = tuple(map(int, QT_VERSION_STR.split(".")))

elif qt_api == "pyqt6":
    from PyQt6.QtCore import *

    from PyQt6.QtCore import pyqtProperty as Property
    from PyQt6.QtCore import pyqtSignal as Signal
    from PyQt6.QtCore import pyqtSlot as Slot

    __version__ = QT_VERSION_STR
    __version_info__ = tuple(map(int, QT_VERSION_STR.split(".")))

elif qt_api == "pyside6":
    from PySide6.QtCore import *

    from PySide6 import __version__, __version_info__

else:
    from PySide2.QtCore import *

    from PySide2 import __version__, __version_info__
