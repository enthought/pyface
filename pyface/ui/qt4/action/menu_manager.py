#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

#
# Author: Riverbank Computing Limited
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" The PyQt specific implementation of a menu manager. """


# Major package imports.
from pyface.qt import QtCore, QtGui

# Enthought library imports.
from traits.api import Instance, Unicode

# Local imports.
from pyface.action.action_manager import ActionManager
from pyface.action.action_manager_item import ActionManagerItem
from pyface.action.action_item import _Tool, Action
from pyface.action.group import Group


class MenuManager(ActionManager, ActionManagerItem):
    """ A menu manager realizes itself in a menu control.

    This could be a sub-menu or a context (popup) menu.
    """

    #### 'MenuManager' interface ##############################################

    # The menu manager's name (if the manager is a sub-menu, this is what its
    # label will be).
    name = Unicode

    # The default action for tool button when shown in a toolbar (Qt only)
    action = Instance(Action)

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

        return _Menu(self, parent, controller)

    ###########################################################################
    # 'ActionManagerItem' interface.
    ###########################################################################

    def add_to_menu(self, parent, menu, controller):
        """ Adds the item to a menu. """

        submenu = self.create_menu(parent, controller)
        submenu.menuAction().setText(self.name)
        menu.addMenu(submenu)

    def add_to_toolbar(self, parent, tool_bar, image_cache, controller,
                       show_labels=True):
        """ Adds the item to a tool bar. """
        menu = self.create_menu(parent, controller)
        if self.action:
            tool_action = _Tool(
                parent, tool_bar, image_cache, self, controller, show_labels).control
            tool_action.setMenu(menu)
        else:
            tool_action = menu.menuAction()
            tool_bar.addAction(tool_action)

        tool_action.setText(self.name)
        tool_button = tool_bar.widgetForAction(tool_action)
        tool_button.setPopupMode(tool_button.MenuButtonPopup if self.action
                                 else tool_button.InstantPopup)


class _Menu(QtGui.QMenu):
    """ The toolkit-specific menu control. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, manager, parent, controller):
        """ Creates a new tree. """

        # Base class constructor.
        QtGui.QMenu.__init__(self, parent)

        # The parent of the menu.
        self._parent = parent

        # The manager that the menu is a view of.
        self._manager = manager

        # The controller.
        self._controller = controller

        # List of menu items
        self.menu_items = []

        # Create the menu structure.
        self.refresh()

        # Listen to the manager being updated.
        self._manager.on_trait_change(self.refresh, 'changed')
        self._manager.on_trait_change(self._on_enabled_changed, 'enabled')
        self._manager.on_trait_change(self._on_visible_changed, 'visible')
        self._manager.on_trait_change(self._on_name_changed, 'name')
        self.setEnabled(self._manager.enabled)
        self.menuAction().setVisible(self._manager.visible)

        return

    ###########################################################################
    # '_Menu' interface.
    ###########################################################################

    def clear(self):
        """ Clears the items from the menu. """

        for item in self.menu_items:
            item.dispose()
            
        self.menu_items = []

        super(_Menu, self).clear()

    def is_empty(self):
        """ Is the menu empty? """

        return self.isEmpty()

    def refresh(self):
        """ Ensures that the menu reflects the state of the manager. """

        self.clear()

        manager = self._manager
        parent  = self._parent

        previous_non_empty_group = None
        for group in manager.groups:
            previous_non_empty_group = self._add_group(parent, group,
                    previous_non_empty_group)

        self.setEnabled(manager.enabled)

    def show(self, x=None, y=None):
        """ Show the menu at the specified location. """

        if x is None or y is None:
            point = QtGui.QCursor.pos()
        else:
            point = QtCore.QPoint(x, y)
        self.popup(point)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _on_enabled_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        self.setEnabled(new)

    def _on_visible_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        self.menuAction().setVisible(new)

        return

    def _on_name_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        self.menuAction().setText(new)

        return

    def _add_group(self, parent, group, previous_non_empty_group=None):
        """ Adds a group to a menu. """

        if len(group.items) > 0:
            # Is a separator required?
            if previous_non_empty_group is not None and group.separator:
                self.addSeparator()

            # Create actions and sub-menus for each contribution item in
            # the group.
            for item in group.items:
                if isinstance(item, Group):
                    if len(item.items) > 0:
                        self._add_group(parent, item, previous_non_empty_group)

                        if previous_non_empty_group is not None \
                           and previous_non_empty_group.separator \
                           and item.separator:
                            self.addSeparator()

                        previous_non_empty_group = item

                else:
                    item.add_to_menu(parent, self, self._controller)

            previous_non_empty_group = group

        return previous_non_empty_group

#### EOF ######################################################################
