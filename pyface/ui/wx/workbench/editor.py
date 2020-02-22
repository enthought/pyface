# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------

""" Enthought pyface package component
"""

# Local imports.
from pyface.workbench.i_editor import MEditor


class Editor(MEditor):
    """ The toolkit specific implementation of an Editor.

    See the IEditor interface for the API documentation.

    """

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the part. """

        import wx

        # By default we create a yellow panel!
        control = wx.Panel(parent, -1)
        control.SetBackgroundColour("yellow")
        control.SetSize((100, 200))

        return control

    def destroy_control(self):
        """ Destroy the toolkit-specific control that represents the part. """

        if self.control is not None:
            self.control.Destroy()
            self.control = None

        return

    def set_focus(self):
        """ Set the focus to the appropriate control in the part. """

        if self.control is not None:
            self.control.SetFocus()

        return


#### EOF ######################################################################
