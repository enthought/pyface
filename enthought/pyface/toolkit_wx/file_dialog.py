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


class FileDialog_wx(object):
    """ The FileDialog monkey patch for wx. """

    ###########################################################################
    # 'FileDialog' toolkit interface.
    ###########################################################################

    def _tk_filedialog_create(self, parent, directory, filename):
        """ Create the toolkit specific control that represents the dialog. """

        if self.action == 'open':
            style = wx.OPEN | wx.HIDE_READONLY

        else:
            style = wx.SAVE | wx.OVERWRITE_PROMPT

        # Create the actual dialog.
        return wx.FileDialog(
            parent,
            self.title,
            defaultDir  = directory,
            defaultFile = filename,
            style       = style,
            wildcard    = self.wildcard
        )

    def _tk_filedialog_get_path(self):
        """ Return the selected pathname. """

        return str(self.control.GetPath())

#### EOF ######################################################################
