#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  Author: Scott Swarts <swarts@enthought.com>
#
#-----------------------------------------------------------------------------

"""A dialog that is loaded from an XRC resource file.
"""
from __future__ import absolute_import

# Standard library imports.
import os.path

# Major packages.
import wx
import wx.xrc

# Enthought library imports
from traits.api import Instance, Str
import traits.util.resource

# Local imports.
from .dialog import Dialog


##############################################################################
# class 'XrcDialog'
##############################################################################

class XrcDialog(Dialog):
    """A dialog that is loaded from an XRC resource file.
    """

    ##########################################################################
    # Traits
    ##########################################################################

    ### 'XrcDialog' interface ############################################

    # Path to the xrc file relative to the class's module
    xrc_file = Str

    # The ID of the dialog in the file
    id = Str("dialog")

    # The resource object
    resource = Instance(wx.xrc.XmlResource)

    ##########################################################################
    # 'Dialog' interface
    ##########################################################################

    def _create_control(self, parent):
        """
        Creates the dialog and loads it in from the resource file.
        """
        classpath = traits.util.resource.get_path( self )
        path = os.path.join( classpath, self.xrc_file )

        self.resource = wx.xrc.XmlResource( path )
        return self.resource.LoadDialog(parent, self.id)

    def _create_contents(self, dialog):
        """
        Calls add_handlers.  The actual content is created
        in _create_control by loading a resource file.
        """
        # Wire up the standard buttons
        # We change the ID on OK and CANCEL to the standard ids
        # so we get the default behavior
        okbutton = self.XRCCTRL("OK")
        if okbutton is not None:
            # Change the ID and set the handler
            okbutton.SetId(wx.ID_OK)
            wx.EVT_BUTTON(self.control, okbutton.GetId(), self._on_ok)
        cancelbutton = self.XRCCTRL("CANCEL")
        if cancelbutton is not None:
            # Change the ID and set the handler
            cancelbutton.SetId(wx.ID_CANCEL)
            wx.EVT_BUTTON(self.control, cancelbutton.GetId(), self._on_cancel)
        helpbutton = self.XRCCTRL("HELP")
        if helpbutton is not None:
            wx.EVT_BUTTON(self.control, helpbutton.GetId(), self._on_help)

        self._add_handlers()

    ##########################################################################
    # 'XrcDialog' interface
    ##########################################################################

    def XRCID(self, name):
        """
        Returns the numeric widget id for the given name.
        """
        return wx.xrc.XRCID(name)

    def XRCCTRL(self, name):
        """
        Returns the control with the given name.
        """
        return self.control.FindWindowById(self.XRCID(name))

    def set_validator(self, name, validator):
        """
        Sets the validator on the named control.
        """
        self.XRCCTRL(name).SetValidator(validator)

    ##########################################################################
    # 'XrcDialog' protected interface
    ##########################################################################

    def _add_handlers(self):
        """
        Override to add event handlers.
        """
        return

#### EOF ######################################################################
