# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" The wx specific implementation of a menu manager.
"""


import wx


from traits.api import Str, Bool, provides


from pyface.action.action_manager import ActionManager
from pyface.action.action_manager_item import ActionManagerItem
from pyface.action.group import Group
from pyface.action.i_menu_manager import IMenuManager


@provides(IMenuManager)
class MenuManager(ActionManager, ActionManagerItem):
    """ A menu manager realizes itself in a menu control.

    This could be a sub-menu or a context (popup) menu.
    """

    # 'MenuManager' interface ---------------------------------------------#

    # The menu manager's name (if the manager is a sub-menu, this is what its
    # label will be).
    name = Str()

    # Does the menu require a separator before the menu item name?
    separator = Bool(True)

    # ------------------------------------------------------------------------
    # 'MenuManager' interface.
    # ------------------------------------------------------------------------

    def create_menu(self, parent, controller=None):
        """ Creates a menu representation of the manager. """

        # If a controller is required it can either be set as a trait on the
        # menu manager (the trait is part of the 'ActionManager' API), or
        # passed in here (if one is passed in here it takes precedence over the
        # trait).
        if controller is None:
            controller = self.controller

        return _Menu(self, parent, controller)

    # ------------------------------------------------------------------------
    # 'ActionManagerItem' interface.
    # ------------------------------------------------------------------------

    def add_to_menu(self, parent, menu, controller):
        """ Adds the item to a menu. """

        sub = self.create_menu(parent, controller)
        id = sub.GetId()

        # fixme: Nasty hack to allow enabling/disabling of menus.
        sub._id = id
        sub._menu = menu

        menu.Append(id, self.name, sub)

    def add_to_toolbar(self, parent, tool_bar, image_cache, controller):
        """ Adds the item to a tool bar. """

        raise ValueError("Cannot add a menu manager to a toolbar.")


class _Menu(wx.Menu):
    """ The toolkit-specific menu control. """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, manager, parent, controller):
        """ Creates a new tree. """

        # Base class constructor.
        wx.Menu.__init__(self)

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
        self._manager.observe(self.refresh, "changed")
        self._manager.observe(self._on_enabled_changed, "enabled")

        return

    def dispose(self):
        self._manager.observe(self.refresh, "changed", remove=True)
        self._manager.observe(self._on_enabled_changed, "enabled", remove=True)
        # Removes event listeners from downstream menu items
        self.clear()

    # ------------------------------------------------------------------------
    # '_Menu' interface.
    # ------------------------------------------------------------------------

    def clear(self):
        """ Clears the items from the menu. """

        for item in self.GetMenuItems():
            if item.GetSubMenu() is not None:
                item.GetSubMenu().clear()
            self.Delete(item.GetId())

        for item in self.menu_items:
            item.dispose()

        self.menu_items = []

    def is_empty(self):
        """ Is the menu empty? """

        return self.GetMenuItemCount() == 0

    def refresh(self, event=None):
        """ Ensures that the menu reflects the state of the manager. """

        self.clear()

        manager = self._manager
        parent = self._parent

        previous_non_empty_group = None
        for group in manager.groups:
            previous_non_empty_group = self._add_group(
                parent, group, previous_non_empty_group
            )

    def show(self, x=None, y=None):
        """ Show the menu at the specified location. """

        if x is None or y is None:
            self._parent.PopupMenu(self)
        else:
            self._parent.PopupMenu(self, x, y)

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _on_enabled_changed(self, event):
        """ Dynamic trait change handler. """

        # fixme: Nasty hack to allow enabling/disabling of menus.
        #
        # We cannot currently (AFAIK) disable menus on the menu bar. Hence
        # we don't give them an '_id'...

        if hasattr(self, "_id"):
            self._menu.Enable(self._id, event.new)

    def _add_group(self, parent, group, previous_non_empty_group=None):
        """ Adds a group to a menu. """

        if len(group.items) > 0:
            # Is a separator required?
            if previous_non_empty_group is not None and group.separator:
                self.AppendSeparator()

            # Create actions and sub-menus for each contribution item in
            # the group.
            for item in group.items:
                if isinstance(item, Group):
                    if len(item.items) > 0:
                        self._add_group(parent, item, previous_non_empty_group)

                        if (
                            previous_non_empty_group is not None
                            and previous_non_empty_group.separator
                            and item.separator
                        ):
                            self.AppendSeparator()

                        previous_non_empty_group = item

                else:
                    if isinstance(item, MenuManager):
                        if item.separator:
                            self.AppendSeparator()
                        previous_non_empty_group = item
                    item.add_to_menu(parent, self, self._controller)

            previous_non_empty_group = group

        return previous_non_empty_group
