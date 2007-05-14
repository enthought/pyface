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


class View_wx(object):
    """ The View monkey patch for wx. """

    ###########################################################################
    # 'View' toolkit interface.
    ###########################################################################

    def _tk_view_create(self, parent):
        """ Create a default control. """

        # By default we create a red panel!
        panel = wx.Panel(parent, -1)
        panel.SetBackgroundColour("red")
        panel.SetSize((100, 200))

        return panel

    def _tk_view_destroy(self):
        """ Destroy the control. """

        self.control.Destroy()

        return

    def _tk_view_set_focus(self):
        """ Set the focus to the control. """

        self.control.SetFocus()

        return

#### EOF ######################################################################
