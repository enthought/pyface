# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
from . import qt_api

if qt_api == "pyqt":
    from PyQt4.QtWebKit import *

elif qt_api == "pyqt5":
    from PyQt5.QtWidgets import *

    try:
        from PyQt5.QtWebEngine import *
        from PyQt5.QtWebEngineWidgets import (
            QWebEngineHistory as QWebHistory,
            QWebEngineHistoryItem as QWebHistoryItem,
            QWebEnginePage as QWebPage,
            QWebEngineView as QWebView,
            QWebEngineSettings as QWebSettings,
        )
    except ImportError:
        from PyQt5.QtWebKit import *
        from PyQt5.QtWebKitWidgets import *

elif qt_api == "pyside2":
    from PySide2.QtWidgets import *

    # WebKit is currently in flux in PySide2
    try:
        from PySide2.QtWebEngineWidgets import (
            # QWebEngineHistory as QWebHistory,
            QWebEngineHistoryItem as QWebHistoryItem,
            QWebEnginePage as QWebPage,
            QWebEngineView as QWebView,
            QWebEngineSettings as QWebSettings,
        )
    except ImportError:
        from PySide2.QtWebKit import *
        from PySide2.QtWebKitWidgets import *

else:
    from PySide.QtWebKit import *
