# (C) Copyright 2005-2025 Enthought, Inc., Austin, TX
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
    # Forwards compatibility imports
    from PyQt5.QtSvg import *

elif qt_api == "pyqt6":
    from PyQt6.QtSvgWidgets import *

elif qt_api == "pyside6":
    from PySide6.QtSvgWidgets import *

else:
    # Forwards compatibility imports
    from PySide2.QtSvg import *
