# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""Interface for all action managers."""


from traits.api import Bool, Constant, Event, Instance, Interface, List, Str

from pyface.action.action_controller import ActionController
from pyface.action.group import Group


class IActionManager(Interface):
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
    groups = List(Instance(Group))

    #: The manager's unique identifier (if it has one).
    id = Str()

    #: Is the action manager visible?
    visible = Bool(True)

    # Events ----

    #: fixme: We probably need more granular events than this!
    changed = Event()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, *items, **traits):
        """ Creates a new action manager.

        Parameters
        ----------
        items : collection of strings, Group, or ActionManagerItem s
            Positional arguments are interpreted as Items or Groups
            managed by the action manager.
        traits : additional traits
            Traits to be passed to the usual Traits ``__init__``.

        Notes
        -----

        If a Group is passed as a positional agrument then it is added to the
        manager and any subsequent Items arguments are appended to the Group
        until another Group is encountered.

        If a string is passed, a Group is created with id set to the string.
        """

    # ------------------------------------------------------------------------
    # 'IActionManager' interface.
    # ------------------------------------------------------------------------

    def append(self, item):
        """ Append an item to the manager.

        Parameters
        ----------
        item : string, Group instance or ActionManagerItem
            The item to append.

        Notes
        -----

        If the item is a group, the Group is appended to the manager's list
        of groups.  It the item is a string, then a group is created with
        the string as the ``id`` and the new group is appended to the list
        of groups.  If the item is an ActionManagerItem then the item is
        appended to the manager's default group.
        """

    def destroy(self):
        """ Called when the manager is no longer required.

        By default this method simply calls 'destroy' on all of the manager's
        groups.
        """

    def insert(self, index, item):
        """ Insert an item into the manager at the specified index.

        Parameters
        ----------
        index : int
            The position at which to insert the object
        item : string, Group instance or ActionManagerItem
            The item to insert.

        Notes
        -----

        If the item is a group, the Group is inserted into the manager's list
        of groups.  It the item is a string, then a group is created with
        the string as the ``id`` and the new group is inserted into the list
        of groups.  If the item is an ActionManagerItem then the item is
        inserted into the manager's defualt group.
        """

    def find_group(self, id):
        """ Find a group with a specified Id.

        Parameters
        ----------
        id : str
            The id of the group to find.

        Returns
        -------
        group : Group
            The group which matches the id, or None if no such group exists.
        """

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

    def walk(self, fn):
        """ Walk the manager applying a function at every item.

        The components are walked in pre-order.

        Parameters
        ----------
        fn : Callable
            A callable to apply to the tree of groups and items, starting with
            the manager.
        """

    def walk_group(self, group, fn):
        """ Walk a group applying a function at every item.

        The components are walked in pre-order.

        Parameters
        ----------
        group : Group
            The group to walk.
        fn : Callable
            A callable to apply to the tree of groups and items.
        """

    def walk_item(self, item, fn):
        """ Walk an item (may be a sub-menu manager remember!).

        The components are walked in pre-order.

        Parameters
        ----------
        item : item
            The item to walk.  This may be a submenu or similar in addition to
            simple Action items.
        fn : Callable
            A callable to apply to the tree of items and subgroups.
        """
