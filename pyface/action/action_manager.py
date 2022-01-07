# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Abstract base class for all action managers. """


from traits.api import (
    Bool, Constant, Event, HasTraits, Instance, List, observe, Property, Str
)

from pyface.action.action_controller import ActionController
from pyface.action.group import Group


class ActionManager(HasTraits):
    """ Abstract base class for all action managers.

    An action manager contains a list of groups, with each group containing a
    list of items.

    There are currently three concrete sub-classes:

    1) 'MenuBarManager'
    2) 'MenuManager'
    3) 'ToolBarManager'

    """

    # 'ActionManager' interface --------------------------------------------

    #: The Id of the default group.
    DEFAULT_GROUP = Constant("additions")

    #: The action controller (if any) used to control how actions are performed.
    controller = Instance(ActionController)

    #: Is the action manager enabled?
    enabled = Bool(True)

    #: All of the contribution groups in the manager.
    groups = Property(List(Group))

    #: The manager's unique identifier (if it has one).
    id = Str()

    #: Is the action manager visible?
    visible = Bool(True)

    # Events ----

    #: fixme: We probably need more granular events than this!
    changed = Event()

    # Private interface ----------------------------------------------------

    #: All of the contribution groups in the manager.
    _groups = List(Group)

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, *args, **traits):
        """ Creates a new action manager.

        Parameters
        ----------
        args : collection of strings, Group instances, or ActionManagerItem instances
            Positional arguments are interpreted as Items or Groups managed
            by the action manager.

        Notes
        -----

        If a Group is passed as a positional agrument then it is added to the
        manager and any subsequent Items arguments are appended to the Group
        until another Group is encountered.

        If a string is passed, a Group is created with id set to the string.
        """
        # Base class constructor.
        super().__init__(**traits)

        # The last group in every manager is the group with Id 'additions'.
        #
        # fixme: The side-effect of this is to ensure that the 'additions'
        # group has been created.  Is the 'additions' group even a good idea?
        group = self._get_default_group()

        # Add all items to the manager.
        for arg in args:
            # We allow a group to be defined by simply specifying a string (its
            # Id).
            if isinstance(arg, str):
                # Create a group with the specified Id.
                arg = Group(id=arg)

            # If the item is a group then add it just before the default group
            # (ie. we always keep the default group as the last group in the
            # manager).
            if isinstance(arg, Group):
                self.insert(-1, arg)
                group = arg

            # Otherwise, the item is an action manager item so add it to the
            # current group.
            else:
                group.append(arg)

    # ------------------------------------------------------------------------
    # 'ActionManager' interface.
    # ------------------------------------------------------------------------

    # Trait properties -----------------------------------------------------

    def _get_groups(self):
        return self._groups[:]

    # Trait change handlers ------------------------------------------------

    @observe('enabled')
    def _enabled_updated(self, event):
        for group in self._groups:
            group.enabled = event.new

    @observe('visible')
    def _visible_updated(self, event):
        for group in self._groups:
            group.visible = event.new

    # Methods -------------------------------------------------------------#

    def append(self, item):
        """ Append an item to the manager.

        Parameters
        ----------
        item : string, Group instance or ActionManagerItem instance
            The item to append.

        Notes
        -----

        If the item is a group, the Group is appended to the manager's list
        of groups.  It the item is a string, then a group is created with
        the string as the ``id`` and the new group is appended to the list
        of groups.  If the item is an ActionManagerItem then the item is
        appended to the manager's default group.
        """
        item = self._prepare_item(item)
        if isinstance(item, Group):
            group = self._groups

        else:
            group = self._get_default_group()

        group.append(item)
        return group

    def destroy(self):
        """ Called when the manager is no longer required.

        By default this method simply calls 'destroy' on all of the manager's
        groups.
        """
        for group in self.groups:
            group.destroy()

    def insert(self, index, item):
        """ Insert an item into the manager at the specified index.

        Parameters
        ----------
        index : int
            The position at which to insert the object
        item : string, Group instance or ActionManagerItem instance
            The item to insert.

        Notes
        -----

        If the item is a group, the Group is inserted into the manager's list
        of groups.  It the item is a string, then a group is created with
        the string as the ``id`` and the new group is inserted into the list
        of groups.  If the item is an ActionManagerItem then the item is
        inserted into the manager's defualt group.
        """
        item = self._prepare_item(item)

        if isinstance(item, Group):
            group = self._groups

        else:
            group = self._get_default_group()

        group.insert(index, item)
        return group

    def find_group(self, id):
        """ Find a group with a specified Id.

        Parameters
        ----------
        id : str
            The id of the group to find.

        Returns
        -------
        group : Group instance
            The group which matches the id, or None if no such group exists.
        """
        for group in self._groups:
            if group.id == id:
                return group
        else:
            return None

    def find_item(self, path):
        """ Find an item using a path.

        Parameters
        ----------
        path : str
            A '/' separated list of contribution Ids.

        Returns
        -------
        item : ActionManagerItem or None
            Returns the matching ActionManagerItem, or None if any component
            of the path is not found.
        """
        components = path.split("/")

        # If there is only one component, then the path is just an Id so look
        # it up in this manager.
        if len(components) > 0:
            item = self._find_item(components[0])
            if len(components) > 1 and item is not None:
                item = item.find_item("/".join(components[1:]))
        else:
            item = None

        return item

    def walk(self, fn):
        """ Walk the manager applying a function at every item.

        The components are walked in pre-order.

        Parameters
        ----------
        fn : callable
            A callable to apply to the tree of groups and items, starting with
            the manager.
        """
        fn(self)

        for group in self._groups:
            self.walk_group(group, fn)

    def walk_group(self, group, fn):
        """ Walk a group applying a function at every item.

        The components are walked in pre-order.

        Parameters
        ----------
        fn : callable
            A callable to apply to the tree of groups and items.
        """
        fn(group)

        for item in group.items:
            if isinstance(item, Group):
                self.walk_group(item, fn)
            else:
                self.walk_item(item, fn)

    def walk_item(self, item, fn):
        """ Walk an item (may be a sub-menu manager remember!).

        The components are walked in pre-order.

        Parameters
        ----------
        fn : callable
            A callable to apply to the tree of items and subgroups.
        """
        if hasattr(item, "groups"):
            item.walk(fn)
        else:
            fn(item)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_default_group(self):
        """ Returns the manager's default group.

        This will create this group if it doesn't already exist.

        Returns
        -------
        group : Group instance
            The manager's default group.
        """
        group = self.find_group(self.DEFAULT_GROUP)
        if group is None:
            group = self._prepare_item(self.DEFAULT_GROUP)
            self._groups.append(group)

        return group

    def _prepare_item(self, item):
        """ Prepare an item to be added to this ActionManager.

        Parameters
        ----------
        item : string, Group instance or ActionManagerItem instance
            The item to be added to this ActionManager

        Returns
        -------
        item : Group or ActionManagerItem
            Modified item
        """
        # 1) The item is a 'Group' instance.
        if isinstance(item, Group):
            item.parent = self

        # 2) The item is a string.
        elif isinstance(item, str):
            # Create a group with that Id.
            item = Group(id=item)
            item.parent = self

        return item

    def _find_item(self, id):
        """ Find an item with a spcified Id.

        Parameters
        ----------
        id : str
            The id of the item to be found.

        Returns
        -------
        item : ActionManagerItem or None
            Returns the item with the specified Id, or None if no such item
            exists.
        """
        for group in self.groups:
            item = group.find(id)
            if item is not None:
                return item
        else:
            return None

    # ------------------------------------------------------------------------
    # Debugging interface.
    # ------------------------------------------------------------------------

    def dump(self, indent=""):
        """ Render a manager! """
        print(indent, "Manager", self.id)
        indent += "  "

        for group in self._groups:
            self.render_group(group, indent)

    def render_group(self, group, indent=""):
        """ Render a group! """
        print(indent, "Group", group.id)
        indent += "    "

        for item in group.items:
            if isinstance(item, Group):
                print("Surely, a group cannot contain another group!!!!")
                self.render_group(item, indent)

            else:
                self.render_item(item, indent)

    def render_item(self, item, indent=""):
        """ Render an item! """

        if hasattr(item, "groups"):
            item.dump(indent)

        else:
            print(indent, "Item", item.id)
