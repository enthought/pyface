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
""" A group of action manager items. """

from functools import partial

# Enthought library imports.
from traits.api import Any, Bool, HasTraits, Instance, List, Property
from traits.api import Str
from traits.trait_base import user_name_for

# Local imports.
from pyface.action.action import Action
from pyface.action.action_item import ActionItem
from pyface.action.action_manager_item import ActionManagerItem


class Group(HasTraits):
    """ A group of action manager items.

    By default, a group declares itself as requiring a separator when it is
    visualized, but this can be changed by setting its 'separator' trait to
    False.

    """

    #### 'Group' interface ####

    #: Is the group enabled?
    enabled = Bool(True)

    #: Is the group visible?
    visible = Bool(True)

    #: The group's unique identifier (only needs to be unique within the action
    #: manager that the group belongs to).
    id = Str

    #: All of the items in the group.
    items = Property

    #: The action manager that the group belongs to.
    parent = Any  #Instance('pyface.action.ActionManager')

    #: Does this group require a separator when it is visualized?
    separator = Bool(True)

    #### Private interface ####

    #: All of the items in the group.
    _items = List  #(ActionManagerItem)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *items, **traits):
        """ Creates a new menu manager.

        Parameters
        ----------
        items : collection of ActionManagerItems
            Items to add to the group.
        """
        # Base class constructor.
        super(Group, self).__init__(**traits)

        # Add any specified items.
        for item in items:
            self.append(item)

    ###########################################################################
    # 'Group' interface.
    ###########################################################################

    #### Trait Properties #####################################################

    def _get_items(self):
        return self._items[:]

    #### Trait change handlers ################################################

    def _enabled_changed(self, trait_name, old, new):
        for item in self.items:
            item.enabled = new

    #### Methods ##############################################################

    def append(self, item):
        """ Appends an item to the group.

        Parameters
        ----------
        item : ActionManagerItem, Action or callable
            The item to append.

        Returns
        -------
        item : ActionManagerItem
            The actually inserted item.

        Notes
        -----
        If the item is an ActionManagerItem instance it is simply appended.
        If the item is an Action instance, an ActionItem is created for the
        action, and that is appended.  If the item is a callable, then an
        Action is created for the callable, and then that is handled as above.
        """
        return self.insert(len(self._items), item)

    def clear(self):
        """ Remove all items from the group. """
        self._items = []

    def destroy(self):
        """ Called when the manager is no longer required.

        By default this method simply calls 'destroy' on all items in the
        group.
        """
        for item in self.items:
            item.destroy()

    def insert(self, index, item):
        """ Inserts an item into the group at the specified index.

        Parameters
        ----------
        index : int
            The position to insert the item.
        item : ActionManagerItem, Action or callable
            The item to insert.

        Returns
        -------
        item : ActionManagerItem
            The actually inserted item.

        Notes
        -----

        If the item is an ActionManagerItem instance it is simply inserted.
        If the item is an Action instance, an ActionItem is created for the
        action, and that is inserted.  If the item is a callable, then an
        Action is created for the callable, and then that is handled as above.
        """
        if isinstance(item, Action):
            item = ActionItem(action=item)
        elif callable(item):
            name = user_name_for(item.__name__)
            item = ActionItem(action=Action(name=name, on_perform=item))

        item.parent = self
        self._items.insert(index, item)

        return item

    def remove(self, item):
        """ Removes an item from the group.

        Parameters
        ----------
        item : ActionManagerItem
            The item to remove.
        """
        self._items.remove(item)
        item.parent = None

    def insert_before(self, before, item):
        """ Inserts an item into the group before the specified item.

        Parameters
        ----------
        before : ActionManagerItem
            The item to insert before.
        item : ActionManagerItem, Action or callable
            The item to insert.

        Returns
        -------
        index, item : int, ActionManagerItem
            The position inserted, and the item actually inserted.

        Notes
        -----

        If the item is an ActionManagerItem instance it is simply inserted.
        If the item is an Action instance, an ActionItem is created for the
        action, and that is inserted.  If the item is a callable, then an
        Action is created for the callable, and then that is handled as above.
        """
        index = self._items.index(before)
        self.insert(index, item)
        return (index, item)

    def insert_after(self, after, item):
        """ Inserts an item into the group after the specified item.

        Parameters
        ----------
        before : ActionManagerItem
            The item to insert after.
        item : ActionManagerItem, Action or callable
            The item to insert.

        Returns
        -------
        index, item : int, ActionManagerItem
            The position inserted, and the item actually inserted.

        Notes
        -----

        If the item is an ActionManagerItem instance it is simply inserted.
        If the item is an Action instance, an ActionItem is created for the
        action, and that is inserted.  If the item is a callable, then an
        Action is created for the callable, and then that is handled as above.
        """
        index = self._items.index(after)
        self.insert(index + 1, item)
        return (index, item)

    def find(self, id):
        """ Find the item with the specified id.

        Parameters
        ----------
        id : str
            The id of the item

        Returns
        -------
        item : ActionManagerItem
            The item with the specified Id, or None if no such item exists.
        """
        for item in self._items:
            if item.id == id:
                return item
        else:
            return None

    @classmethod
    def factory(cls, *args, **kwargs):
        """ Create a factory for a group with the given arguments.

        This is particularly useful for passing context to Tasks schema
        additions.
        """
        return partial(cls, *args, **kwargs)


class Separator(Group):
    """ A convenience class.

    This is only used in 'cheap and cheerful' applications that create menus
    like::

        file_menu = MenuManager(
            CopyAction(),
            Separator(),
            ExitAction()
        )

    Hopefully, 'Separator' is more readable than 'Group'...
    """
    pass
