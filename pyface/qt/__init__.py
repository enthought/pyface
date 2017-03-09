#------------------------------------------------------------------------------
# Copyright (c) 2010, Enthought Inc
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.

#
# Author: Enthought Inc
# Description: Qt API selector. Can be used to switch between pyQt and PySide
#------------------------------------------------------------------------------

import os

from qtpy import API

def prepare_pyqt4():
    # Set PySide compatible APIs.
    import sip
    sip.setapi('QDate', 2)
    sip.setapi('QDateTime', 2)
    sip.setapi('QString', 2)
    sip.setapi('QTextStream', 2)
    sip.setapi('QTime', 2)
    sip.setapi('QUrl', 2)
    sip.setapi('QVariant', 2)

qt_api = API
if qt_api == 'pyqt4':
    qt_api = 'pyqt'

if qt_api is None:
    try:
        import PySide
        qt_api = 'pyside'
    except ImportError:
        try:
            prepare_pyqt4()
            import PyQt4
            qt_api = 'pyqt'
        except ImportError:
            raise ImportError('Cannot import PySide or PyQt4')

elif qt_api == 'pyqt':
    prepare_pyqt4()

elif qt_api == 'pyqt5':
    pass

elif qt_api == 'pyside':
    pass

else:
    raise RuntimeError("Invalid Qt API %r, valid values are: 'pyqt', 'pyqt5', or 'pyside'"
                       % qt_api)
