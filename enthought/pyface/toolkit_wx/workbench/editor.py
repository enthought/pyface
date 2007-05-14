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


class Editor_wx(object):
    """ The Editor monkey patch for wx. """

    ###########################################################################
    # 'Editor' toolkit interface.
    ###########################################################################

    def _tk_editor_create(self, parent):
        """ Create a default control. """

        # By default we create a yellow panel!
        panel = wx.Panel(parent, -1)
        panel.SetBackgroundColour("yellow")
        panel.SetSize((100, 200))

        return panel

    def _tk_editor_destroy(self):
        """ Destroy the control. """

        self.control.Destroy()

        return

    def _tk_editor_set_focus(self):
        """ Set the focus to the control. """

        self.control.SetFocus()

        return

#### EOF ######################################################################
