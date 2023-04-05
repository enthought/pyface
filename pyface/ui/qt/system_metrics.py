# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
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

from traits.api import HasTraits, Int, List, Property, provides, Tuple

from pyface.i_system_metrics import ISystemMetrics, MSystemMetrics
from pyface.qt import QtGui


@provides(ISystemMetrics)
class SystemMetrics(MSystemMetrics, HasTraits):
    """ The toolkit specific implementation of a SystemMetrics.  See the
    ISystemMetrics interface for the API documentation.
    """

    # 'ISystemMetrics' interface -------------------------------------------

    #: The width of the main screen in pixels.
    screen_width = Property(Int)

    #: The height of the main screen in pixels.
    screen_height = Property(Int)

    #: The height and width of each screen in pixels
    screen_sizes = Property(List(Tuple(Int, Int)))

    #: Background color of a standard dialog window as a tuple of RGB values
    #: between 0.0 and 1.0.
    dialog_background_color = Property(Tuple)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_screen_width(self):
        screens = self.screen_sizes
        if len(screens) == 0:
            return 0
        else:
            return screens[0][0]

    def _get_screen_height(self):
        screens = self.screen_sizes
        if len(screens) == 0:
            return 0
        else:
            return screens[0][1]

    def _get_screen_sizes(self):
        screens = QtGui.QApplication.instance().screens()
        return [
            (
                screen.availableGeometry().width(),
                screen.availableGeometry().height(),
            )
            for screen in screens
        ]

    def _get_dialog_background_color(self):
        color = (
            QtGui.QApplication.instance()
            .palette()
            .color(QtGui.QPalette.ColorRole.Window)
        )

        return (color.redF(), color.greenF(), color.blueF())
