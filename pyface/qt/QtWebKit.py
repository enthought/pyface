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

elif qt_api == "pyqt6":
    from PyQt6.QtWidgets import *

    from PyQt6.QtWebEngineCore import (
        QWebEngineHistory as QWebHistory,
        QWebEngineHistoryItem as QWebHistoryItem,
        QWebEnginePage as QWebPage,
        QWebEngineSettings as QWebSettings,
    )
    from PyQt6.QtWebEngineWidgets import (
        QWebEngineView as QWebView,
    )

elif qt_api == "pyside6":
    from PySide6.QtWidgets import *

    from PySide6.QtWebEngineCore import (
        QWebEngineHistory as QWebHistory,
        QWebEngineSettings as QWebSettings,
        QWebEnginePage as QWebPage,
        QWebEngineHistoryItem as QWebHistoryItem,
    )
    from PySide6.QtWebEngineWidgets import (
        QWebEngineView as QWebView,
    )

else:
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
