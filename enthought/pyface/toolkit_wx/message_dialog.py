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


SEVERITY_TO_STYLE_MAP = {
    'information' : wx.ICON_INFORMATION,
    'warning'     : wx.ICON_WARNING,
    'error'       : wx.ICON_ERROR
}


class MessageDialog_wx(object):
    """ The MessageDialog monkey patch for wx. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """Create the toolkit-specific control that represents the window. """

        icon_style = SEVERITY_TO_STYLE_MAP[self.severity]

        dialog = wx.MessageDialog(
            parent, self.message, self.title,
            wx.OK | icon_style | wx.STAY_ON_TOP
        )

        return dialog

#### EOF ######################################################################
