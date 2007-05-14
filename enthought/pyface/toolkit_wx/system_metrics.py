#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------

# Major package imports.
import wx


class SystemMetrics_wx(object):
    """ The SystemMetrics monkey patch for wx. """

    ###########################################################################
    # 'SystemMetrics' toolkit interface.
    ###########################################################################

    def _tk_systemmetrics_get_screen_width(self):
        """ Returns the width of the screen in pixels. """

        return wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)

    def _tk_systemmetrics_get_screen_height(self):

        return wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

    def _tk_systemmetrics_get_dialog_background_color(self):
        """ Returns the background color of a standard dialog window as an RGB
        tuple.  RGB values range between 0.0-1.0 
        """

        wx_color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE)    
        color = wx_color.Get()
        
        return (color[0]/255., color[1]/255., color[2]/255.)

#### EOF ######################################################################
