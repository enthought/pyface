# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import sys

from traits.trait_notifiers import set_ui_handler, ui_handler

from pyface.qt import QtCore, QtGui, qt_api
from pyface.base_toolkit import Toolkit
from .gui import GUI

if qt_api == "pyqt":
    # Check the version numbers are late enough.
    if QtCore.QT_VERSION < 0x040200:
        raise RuntimeError(
            "Need Qt v4.2 or higher, but got v%s" % QtCore.QT_VERSION_STR
        )

    if QtCore.PYQT_VERSION < 0x040100:
        raise RuntimeError(
            "Need PyQt v4.1 or higher, but got v%s" % QtCore.PYQT_VERSION_STR
        )

# It's possible that it has already been initialised.
_app = QtGui.QApplication.instance()

if _app is None:
    _app = QtGui.QApplication(sys.argv)


# create the toolkit object
toolkit_object = Toolkit("pyface", "qt4", "pyface.ui.qt4")


# ensure that Traits has a UI handler appropriate for the toolkit.
if ui_handler is None:
    # Tell the traits notification handlers to use this UI handler
    set_ui_handler(GUI.invoke_later)
