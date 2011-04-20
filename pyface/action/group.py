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


# Enthought library imports.
from traits.api import Any, Bool, HasTraits, Instance, List, Property
from traits.api import Str
from traits.trait_base import user_name_for

# Local imports.
from action import Action
from action_item import ActionItem
from action_manager_item import ActionManagerItem


class Group(HasTraits):
    """ A group of action manager items.

    By default, a group declares itself as requiring a separator when it is
    visualized, but this can be changed by setting its 'separator' trait to
    False.

    """

    #### 'Group' interface ####

    # Is the group enabled?
    enabled = Bool(True)

    # Is the group visible?
    visible = Bool(True)

    # The group's unique identifier (only needs to be unique within the action
    # manager that the group belongs to).
    id = Str

    # All of the items in the group.
    items = Property

    # The action manager that the group belongs to.
    parent = Any#Instance('pyface.action.ActionManager')

    # Does this group require a separator when it is visualized?
    separator = Bool(True)

    #### Private interface ####

    # All of the items in the group.
    _items = List#(ActionManagerItem)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *items,  **traits):
        """ Creates a new menu manager. """

        # Base class constructor.
        super(Group, self).__init__(**traits)

        # Add any specified items.
        for item in items:
            self.append(item)

        return

    ###########################################################################
    # 'Group' interface.
    ###########################################################################

    #### Trait Properties #####################################################

    def _get_items(self):
        """ Returns the items in the group. """

        return self._items[:]

    #### Trait change handlers ################################################

    def _enabled_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        for item in self.items:
            item.enabled = new

        return

    #### Methods ##############################################################

    def append(self, item):
        """ Appends an item to the group.

        See the documentation for 'insert'.

        """

        return self.insert(len(self._items), item)

    def clear(self):
        """ Remove all items from the group. """

        self._items = []

        return

    def destroy(self):
        """ Called when the manager is no longer required.

        By default this method simply calls 'destroy' on all items in the
        group.

        """

        for item in self.items:
            item.destroy()

        return

    def insert(self, index, item):
        """ Inserts an item into the group at the specified index.

        1) An 'ActionManagerItem' instance.

            In which case the item is simply inserted into the group.

        2) An 'Action' instance.

            In which case an 'ActionItem' instance is created with the action
            and then inserted into the group.

        3) A Python callable (ie.'callable(item)' returns True).

            In which case an 'Action' is created that calls the callable when
            it is performed, and the action is then wrapped as in 2).

        """

        if isinstance(item, Action):
            item = ActionItem(action=item)

        elif callable(item):
            text = user_name_for(item.func_name)
            item = ActionItem(action=Action(text=text, on_perform=item))

        item.parent = self
        self._items.insert(index, item)

        return item

    def remove(self, item):
        """ Removes an item from the group. """

        self._items.remove(item)
        item.parent = None

        return

    def insert_before(self, before, item):
        """ Inserts an item into the group before the specified item.

        See the documentation for 'insert'.

        """

        index = self._items.index(before)

        self.insert(index, item)

        return (index, item)

    def insert_after(self, after, item):
        """ Inserts an item into the group after the specified item.

        See the documentation for 'insert'.

        """

        index = self._items.index(after)

        self.insert(index + 1, item)

        return (index, item)

    def find(self, id):
        """ Returns the item with the specified Id.

        Returns None if no such item exists.

        """

        for item in self._items:
            if item.id == id:
                break

        else:
            item = None

        return item


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

#### EOF ######################################################################
