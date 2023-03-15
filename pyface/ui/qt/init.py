# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
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

from pyface.qt import QtGui
from pyface.base_toolkit import Toolkit
from .gui import GUI

# It's possible that it has already been initialised.
_app = QtGui.QApplication.instance()

if _app is None:
    try:
        # pyface.qt.QtWebKit tries QtWebEngineWidgets first, but
        # if QtWebEngineWidgets is present, it must be imported prior to
        # creating a QCoreApplication instance, otherwise importing
        # QtWebEngineWidgets later would fail (see enthought/pyface#581).
        # Import it here first before creating the instance.
        from pyface.qt import QtWebKit  # noqa: F401
    except ImportError:
        # This error will be raised in the context where
        # QtWebKit/QtWebEngine widgets are required.
        pass
    _app = QtGui.QApplication(sys.argv)


# create the toolkit object
toolkit_object = Toolkit("pyface", "qt", "pyface.ui.qt")


# ensure that Traits has a UI handler appropriate for the toolkit.
if ui_handler is None:
    # Tell the traits notification handlers to use this UI handler
    set_ui_handler(GUI.invoke_later)
