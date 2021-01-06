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
    from PyQt4.QtScript import *

elif qt_api == "pyqt5":
    import warnings

    warnings.warn(DeprecationWarning("QtScript is not supported in PyQt5"))

elif qt_api == "pyside2":
    import warnings

    warnings.warn(DeprecationWarning("QtScript is not supported in PyQt5"))

else:
    from PySide.QtScript import *
