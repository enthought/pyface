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
    from PyQt5.QtOpenGL import *
    from PyQt5.QtWidgets import QOpenGLWidget

elif qt_api == "pyqt6":
    from PyQt6.QtOpenGL import *
    from PyQt6.QtOpenGLWidgets import *

elif qt_api == "pyside6":
    from PySide6.QtOpenGL import *
    from PySide6.QtOpenGLWidgets import *

else:
    from PySide2.QtOpenGL import *
    from PySide2.QtWidgets import QOpenGLWidget
