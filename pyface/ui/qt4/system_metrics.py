# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


from pyface.qt import QtGui, is_qt5


from traits.api import HasTraits, Int, Property, provides, Tuple


from pyface.i_system_metrics import ISystemMetrics, MSystemMetrics


@provides(ISystemMetrics)
class SystemMetrics(MSystemMetrics, HasTraits):
    """ The toolkit specific implementation of a SystemMetrics.  See the
    ISystemMetrics interface for the API documentation.
    """

    # 'ISystemMetrics' interface -------------------------------------------

    screen_width = Property(Int)

    screen_height = Property(Int)

    dialog_background_color = Property(Tuple)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_screen_width(self):
        # QDesktopWidget.screenGeometry() is deprecated and Qt docs
        # suggest using screens() instead, but screens in not available in qt4
        # see issue: enthought/pyface#721
        if is_qt5:
            return QtGui.QApplication.instance().screens()[0].availableGeometry().width()
        else:
            return QtGui.QApplication.instance().desktop().availableGeometry().width()

    def _get_screen_height(self):
        # QDesktopWidget.screenGeometry(int screen) is deprecated and Qt docs
        # suggest using screens() instead, but screens in not available in qt4
        # see issue: enthought/pyface#721
        if is_qt5:
            return (
                QtGui.QApplication.instance().screens()[0].availableGeometry().height()
            )
        else:
            return (
                QtGui.QApplication.instance().desktop().availableGeometry().height()
            )

    def _get_dialog_background_color(self):
        color = (
            QtGui.QApplication.instance()
            .palette()
            .color(QtGui.QPalette.Window)
        )

        return (color.redF(), color.greenF(), color.blueF())
