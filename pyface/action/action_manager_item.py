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
""" Abstract base class for all action manager items. """


# Enthought library imports.
from traits.api import Bool, HasTraits, Instance, Str


class ActionManagerItem(HasTraits):
    """ Abstract base class for all action manager items.

    An action manager item represents a contribution to a shared UI resource
    such as a menu bar, menu or tool bar.

    Action manager items know how to add themselves to menu bars, menus and
    tool bars.  In a tool bar a contribution item is represented as a tool or a
    separator.  In a menu bar a contribution item is a menu, and in a menu
    a contribution item is a menu item or separator.

    """

    #: The item's unique identifier ('unique' in this case means unique within
    #: its group)
    id = Str

    #: The group the item belongs to.
    parent = Instance('pyface.action.api.Group')

    #: Is the item enabled?
    enabled = Bool(True)

    #: Is the item visible?
    visible = Bool(True)

    ###########################################################################
    # 'ActionManagerItem' interface.
    ###########################################################################

    def add_to_menu(self, parent, menu, controller):
        """ Adds the item to a menu.

        Parameters
        ----------
        parent : toolkit control
            The parent of the new menu item control.
        menu : toolkit menu
            The menu to add the action item to.
        controller : ActionController instance or None
            The controller to use.
        """
        raise NotImplementedError

    def add_to_toolbar(self, parent, tool_bar, image_cache, controller):
        """ Adds the item to a tool bar.

        Parameters
        ----------
        parent : toolkit control
            The parent of the new menu item control.
        tool_bar : toolkit toolbar
            The toolbar to add the action item to.
        image_cache : ImageCache instance
            The image cache for resized images.
        controller : ActionController instance or None
            The controller to use.
        show_labels : bool
            Should the toolbar item show a label.
        """
        raise NotImplementedError
