# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import importlib
import os
import sys

QtAPIs = [
    ("pyside2", "PySide2"),
    ("pyside6", "PySide6"),
    ("pyqt5", "PyQt5"),
    ("pyqt6", "PyQt6"),
]
api_names, modules = zip(*QtAPIs)


qt_api = None

# have we already imported a Qt API?
for api_name, module in QtAPIs:
    if module in sys.modules:
        qt_api = api_name
        break
else:
    # does our environment give us a preferred API?
    qt_api = os.environ.get("QT_API")

# if we have no preference, is a Qt API available? Or fail with ImportError.
if qt_api is None:
    for api_name, module in QtAPIs:
        try:
            importlib.import_module(module)
            importlib.import_module(".QtCore", module)
            qt_api = api_name
            break
        except ImportError:
            continue
    else:
        raise ImportError("Cannot import any of " + ", ".join(modules))

# otherwise check QT_API value is valid
elif qt_api not in api_names:
    msg = (
        "Invalid Qt API %r, valid values are: "
        + ', '.join(api_names)
    ) % qt_api
    raise RuntimeError(msg)

# useful constants
is_qt4 = False
is_qt5 = qt_api in {"pyqt5", "pyside2"}
is_qt6 = qt_api in {"pyqt6", "pyside6"}
is_pyqt = qt_api in {"pyqt", "pyqt5", "pyqt6"}
is_pyside = qt_api in {"pyside", "pyside2", "pyside6"}
