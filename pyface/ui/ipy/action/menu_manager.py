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
""" The 'null' backend specific implementation of a menu manager.
"""


# Enthought library imports.
from traits.api import Unicode

# Local imports.
from pyface.action.action_manager import ActionManager
from pyface.action.action_manager_item import ActionManagerItem
from pyface.action.group import Group


class MenuManager(ActionManager, ActionManagerItem):
    """ A menu manager realizes itself in a menu control.

    This could be a sub-menu or a context (popup) menu.
    """

    #### 'MenuManager' interface ##############################################

    # The menu manager's name (if the manager is a sub-menu, this is what its
    # label will be).
    name = Unicode

    ###########################################################################
    # 'MenuManager' interface.
    ###########################################################################

    def create_menu(self, parent, controller=None):
        """ Creates a menu representation of the manager. """

        # If a controller is required it can either be set as a trait on the
        # menu manager (the trait is part of the 'ActionManager' API), or
        # passed in here (if one is passed in here it takes precedence over the
        # trait).
        if controller is None:
            controller = self.controller

        return None

    ###########################################################################
    # 'ActionManagerItem' interface.
    ###########################################################################

    def add_to_menu(self, parent, menu, controller):
        """ Adds the item to a menu. """
        return

    def add_to_toolbar(self, parent, tool_bar, image_cache, controller):
        """ Adds the item to a tool bar. """

        raise ValueError("Cannot add a menu manager to a toolbar.")



#### EOF ######################################################################
