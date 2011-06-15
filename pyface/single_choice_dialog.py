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
""" A dialog that allows the user to chose a single item from a list. """
from __future__ import absolute_import

# Major package imports.
import wx

# Enthought library imports.
from traits.api import List, Str, Any

# Local imports.
from .dialog import Dialog


class SingleChoiceDialog(Dialog):
    """ A dialog that allows the user to chose a single item from a list.

    choices is the list of things to choose from.   If name_attribute is
    set then we assume it is a list of objects getattr(obj, name_attribute)
    gives us the string to put in the dialog.  Otherwise we just call str()
    on the choices to get the strings.
    """

    choices = List(Any)
    choice = Any
    name_attribute = Str
    caption = Str

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def close(self):
        """ Closes the window. """

        # Get the chosen object.
        if self.control is not None:
            self.choice = self.choices[self.control.GetSelection()]

        # Let the window close as normal.
        super(SingleChoiceDialog, self).close()

        return

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the window. """

        dialog = wx.SingleChoiceDialog(
            parent,
            self.title,
            self.caption,
            self._get_string_choices(),
            self.STYLE
        )

        return dialog

    def _create_contents(self, parent):
        """ Creates the window contents. """

        # In this case, wx does it all for us in 'wx.SingleChoiceDialog'
        pass

    ###########################################################################
    # 'Private' interface.
    ###########################################################################

    def _get_string_choices(self):
        """ Returns the list of strings to display in the dialog. """

        if len(self.name_attribute) > 0:
            # We asssume choices is a list of objects with this attribute
            choices = [
                getattr(obj, self.name_attribute) for obj in self.choices
            ]

        else:
            # We just convert to strings
            choices = [str(obj) for obj in self.choices]

        return choices

#### EOF ######################################################################
