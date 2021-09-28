# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
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
    from PyQt4.Qt import QKeySequence, QTextCursor
    from PyQt4.QtGui import *

elif qt_api == "pyqt5":
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtPrintSupport import *
    from PyQt5.QtCore import (
        QAbstractProxyModel,
        QItemSelection,
        QItemSelectionModel,
        QItemSelectionRange,
        QSortFilterProxyModel,
        QStringListModel,
    )

    QStyleOptionTabV2 = QStyleOptionTab
    QStyleOptionTabV3 = QStyleOptionTab
    QStyleOptionTabBarBaseV2 = QStyleOptionTabBarBase

else:
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtPrintSupport import *
    from PySide2.QtCore import (
        QAbstractProxyModel,
        QItemSelection,
        QItemSelectionModel,
        QItemSelectionRange,
        QSortFilterProxyModel,
    )

    QStyleOptionTabV2 = QStyleOptionTab
    QStyleOptionTabV3 = QStyleOptionTab
    QStyleOptionTabBarBaseV2 = QStyleOptionTabBarBase
