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


class DirectoryDialog_wx(object):
    """ The DirectoryDialog monkey patch for wx. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create the toolkit specific control that represents the dialog. """

        # The default style.
        style = wx.OPEN | wx.HIDE_READONLY
        
        # Create the wx style depending on which buttons are required etc.
        if self.new_directory:
            style = style | wx.DD_NEW_DIR_BUTTON

        if self.message:
            message = self.message
        else:
            message = "Choose a directory"

        # Create the actual dialog.
        dialog = wx.DirDialog(
            parent,
            message     = message,
            defaultPath = self.default_path,
            style       = style
        )
        
        return dialog

    ###########################################################################
    # 'DirectoryDialog' toolkit interface.
    ###########################################################################

    def _tk_directorydialog_get_path(self):
        """ Return the selected pathname. """

        return self.control.GetPath()

#### EOF ######################################################################
