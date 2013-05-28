#------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: Enthought, Inc.
#
#------------------------------------------------------------------------------

""" Enthought pyface package component
"""

# Standard library imports.
import sys

# Major package imports.
import wx

# Enthought library imports.
from traits.api import HasTraits, Int, Property, provides, Tuple

# Local imports.
from pyface.i_system_metrics import ISystemMetrics, MSystemMetrics


@provides(ISystemMetrics)
class SystemMetrics(MSystemMetrics, HasTraits):
    """ The toolkit specific implementation of a SystemMetrics.  See the
    ISystemMetrics interface for the API documentation.
    """


    #### 'ISystemMetrics' interface ###########################################

    screen_width = Property(Int)

    screen_height = Property(Int)

    dialog_background_color = Property(Tuple)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_screen_width(self):
        return wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)

    def _get_screen_height(self):
        return wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

    def _get_dialog_background_color(self):
        if sys.platform == 'darwin':
            # wx lies.
            color = wx.Colour(232, 232, 232)
        else:
            color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_MENUBAR).Get()

        return (color[0]/255., color[1]/255., color[2]/255.)

#### EOF ######################################################################
