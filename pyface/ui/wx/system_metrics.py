# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""


import sys

import wx

from traits.api import HasTraits, Int, List, Property, provides, Tuple

from pyface.i_system_metrics import ISystemMetrics, MSystemMetrics


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
        return wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)

    def _get_screen_height(self):
        return wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

    def _get_screen_sizes(self):
        return [(self.screen_width, self.screen_height)]

    def _get_dialog_background_color(self):
        if sys.platform == "darwin":
            # wx lies.
            color = wx.Colour(232, 232, 232)
        else:
            color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR).Get()

        return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
