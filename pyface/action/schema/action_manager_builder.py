# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Base action manager builder class

This module provides a base class that takes a schema for an action manager
and builds the concrete action manager and its groups and items, folding in
schema additions.
"""

import logging

from collections import defaultdict

from traits.api import HasTraits, Instance, List

from .schema import Schema, ToolBarSchema
from .schema_addition import SchemaAddition
from ._topological_sort import before_after_sort


# Logging.
logger = logging.getLogger(__name__)


class ActionManagerBuilder(HasTraits):
    """ Builds action managers from schemas, merging schema additions.
    """

    #: An ActionController to use with the action managers created by the
    #: builder.  May be None.
    controller = Instance("pyface.action.action_controller.ActionController")

    #: Schema additions to apply to all managers built by this builder.
    #: Any additions which do not match part of the supplied schema will be
    #: ignored.
    additions = List(Instance(SchemaAddition))

    # ------------------------------------------------------------------------
    # 'ActionManagerBuilder' interface.
    # ------------------------------------------------------------------------

    def create_action_manager(self, schema):
        """ Create a manager for the given schema using the additions.

        Any additions whose paths do not match the supplied

        Parameters
        ----------
        schema : Schema
            An Schema for an ActionManager subclass (ie. one of MenuBarSchema,
            MenuSchema, or ToolBarSchema).

        Returns
        -------
        manager : ActionManager
            The concrete ActionManager instance corresponding to the Schema
            with addtions.  This does not yet have concrete toolkit widgets
            associated with it: usually those will be created separately.
        """
        additions_map = defaultdict(list)
        for addition in self.additions:
            if addition.path:
                additions_map[addition.path].append(addition)

        manager = self._create_action_manager_recurse(schema, additions_map)
        manager.controller = self.controller
        return manager

    def get_additional_toolbar_schemas(self):
        """ Get any top-level toolbars from additions.

        Unlike menus, there is no base toolbar manager, so additions which
        contribute new toolbars appear with no path.  It is up to the class
        using the builder how it wants to handle these additional toolbars.

        Returns
        -------
        schemas : list of ToolBarSchema
            The additional toolbars specified in self.additions.
        """
        schemas = []
        for addition in self.additions:
            if not addition.path:
                schema = addition.factory()
                if isinstance(schema, ToolBarSchema):
                    schemas.append(schema)
                else:
                    logger.error(
                        "Invalid top-level schema addition: %r. Only "
                        "ToolBar schemas can be path-less.",
                        schema,
                    )
        return schemas

    def prepare_item(self, item, path):
        """ Called immediately after a concrete Pyface item has been created
        (or, in the case of items that are not produced from schemas,
        immediately before they are processed).

        This hook can be used to perform last-minute transformations or
        configuration. Returns a concrete Pyface item.

        Parameters
        ----------
        item : pyface.action item
            A concrete Pyface item.
        path : str
            The path to the item in the Schema.

        Returns
        -------
        item : pyface.action item
            A modified or transformed Pyface item.
        """
        return item

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_ordered_schemas(self, schemas):
        begin = []
        middle = []
        end = []

        for schema in schemas:
            absolute_position = getattr(schema, "absolute_position", None)
            if absolute_position is None:
                middle.append(schema)
            elif absolute_position == "last":
                end.append(schema)
            else:
                begin.append(schema)

        schemas = (
            before_after_sort(begin)
            + before_after_sort(middle)
            + before_after_sort(end)
        )
        return schemas

    def _group_items_by_id(self, items):
        """ Group a list of action items by their ID.

        Action items are Schemas and Groups, MenuManagers, etc.

        Return a dictionary {item_id: list_of_items}, and a list containing
        all the ids ordered by their appearance in the `all_items` list. The
        ordered IDs are used as a replacement for an ordered dictionary, to
        keep compatibility with Python <2.7 .

        """

        ordered_items_ids = []
        id_to_items = defaultdict(list)

        for item in items:
            if item.id not in id_to_items:
                ordered_items_ids.append(item.id)
            id_to_items[item.id].append(item)

        return id_to_items, ordered_items_ids

    def _group_items_by_class(self, items):
        """ Group a list of action items by their class.

        Action items are Schemas and Groups, MenuManagers, etc.

        Return a dictionary {item_class: list_of_items}, and a list containing
        all the classes ordered by their appearance in the `all_items` list.
        The ordered classes are used as a replacement for an ordered
        dictionary, to keep compatibility with Python <2.7 .

        """

        ordered_items_class = []
        class_to_items = defaultdict(list)

        for item in items:
            if item.__class__ not in class_to_items:
                ordered_items_class.append(item.__class__)
            class_to_items[item.__class__].append(item)

        return class_to_items, ordered_items_class

    def _unpack_schema_additions(self, items):
        """ Unpack additions, since they may themselves be schemas. """

        unpacked_items = []

        for item in items:
            if isinstance(item, SchemaAddition):
                unpacked_items.append(item.factory())
            else:
                unpacked_items.append(item)

        return unpacked_items

    def _merge_items_with_same_path(self, id_to_items, ordered_items_ids):
        """ Merge items with the same path if possible.

        Items must be subclasses of `Schema` and they must be instances of
        the same class to be merged.

        """

        merged_items = []
        for item_id in ordered_items_ids:
            items_with_same_id = id_to_items[item_id]

            # Group items by class.
            class_to_items, ordered_items_class = self._group_items_by_class(
                items_with_same_id
            )

            for items_class in ordered_items_class:
                items_with_same_class = class_to_items[items_class]

                if len(items_with_same_class) == 1:
                    merged_items.extend(items_with_same_class)

                else:
                    # Only schemas can be merged.
                    if issubclass(items_class, Schema):
                        # Merge into a single schema.
                        items_content = sum(
                            (item.items for item in items_with_same_class), []
                        )

                        merged_item = items_with_same_class[0].clone_traits()
                        merged_item.items = items_content
                        merged_items.append(merged_item)

                    else:
                        merged_items.extend(items_with_same_class)

        return merged_items

    def _preprocess_schemas(self, schema, additions, path):
        """ Sort and merge a schema and a set of schema additions. """

        # Determine the order of the items at this path.
        if additions[path]:
            all_items = self._get_ordered_schemas(
                schema.items + additions[path]
            )
        else:
            all_items = schema.items

        unpacked_items = self._unpack_schema_additions(all_items)

        id_to_items, ordered_items_ids = self._group_items_by_id(
            unpacked_items
        )

        merged_items = self._merge_items_with_same_path(
            id_to_items, ordered_items_ids
        )

        return merged_items

    def _create_action_manager_recurse(self, schema, additions, path=""):
        """ Recursively create a manager for the given schema and additions map.

        Items with the same path are merged together in a single entry if
        possible (i.e., if they have the same class).

        When a list of items is merged, their children are added to a clone
        of the first item in the list. As a consequence, traits like menu
        names etc. are inherited from the first item.

        """
        from pyface.action.action_manager import ActionManager

        # Compute the new action path.
        if path:
            path = path + "/" + schema.id
        else:
            path = schema.id

        preprocessed_items = self._preprocess_schemas(schema, additions, path)

        # Create the actual children by calling factory items.
        children = []
        for item in preprocessed_items:
            if isinstance(item, Schema):
                item = self._create_action_manager_recurse(
                    item, additions, path
                )
            else:
                item = self.prepare_item(item, path + "/" + item.id)

            if isinstance(item, ActionManager):
                # Give even non-root action managers a reference to the
                # controller so that custom Groups, MenuManagers, etc. can get
                # access to the state it holds.
                item.controller = self.controller

            children.append(item)

        # Finally, create the pyface.action instance for this schema.
        return self.prepare_item(schema.create(children), path)
