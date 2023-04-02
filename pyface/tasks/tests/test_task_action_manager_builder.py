# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from contextlib import contextmanager
import unittest


from pyface.action.api import (
    Action,
    ActionItem,
    ActionManager,
    Group,
    MenuManager,
    MenuBarManager,
)
from pyface.action.schema.api import (
    GroupSchema,
    MenuSchema,
    MenuBarSchema,
    SchemaAddition,
)
from pyface.tasks.action.task_action_manager_builder import (
    TaskActionManagerBuilder,
)
from pyface.tasks.api import Task


class ActionManagerBuilderTestCase(unittest.TestCase):

    # 'TestCase' protocol -------------------------------------------------#

    def setUp(self):
        """ Create some dummy actions to use while testing.
        """
        for i in range(1, 7):
            action_id = "action%i" % i
            setattr(
                self, action_id, Action(id=action_id, name="Action %i" % i)
            )

    # 'ActionManagerBuilderTestCase' protocol -----------------------------#

    def assertActionElementsEqual(self, first, second):
        """ Checks that two action managers are (logically) equivalent.
        """
        children1 = children2 = []
        self.assertEqual(type(first), type(second))
        self.assertEqual(first.id, second.id)

        if isinstance(first, ActionItem):
            self.assertEqual(first.action.name, second.action.name)

        elif isinstance(first, ActionManager):
            if not isinstance(first, MenuBarManager):
                self.assertEqual(first.name, second.name)
            children1, children2 = first.groups, second.groups

        elif isinstance(first, Group):
            self.assertEqual(first.separator, second.separator)
            children1, children2 = first.items, second.items

        self.assertEqual(len(children1), len(children2))
        for i in range(len(children1)):
            self.assertActionElementsEqual(children1[i], children2[i])

    def reset_unique_ids(self):
        import pyface.util.id_helper as id_helper
        id_helper.object_counter = id_helper._ObjectCounter()

    @contextmanager
    def unique_id_context_manager(self):
        self.reset_unique_ids()
        try:
            yield
        finally:
            self.reset_unique_ids()

    # Tests ----------------------------------------------------------------

    def test_simple_menu_bar(self):
        """ Does constructing a simple menu with no additions work?
        """
        schema = MenuBarSchema(
            MenuSchema(self.action1, self.action2, id="File", name="&File"),
            MenuSchema(self.action3, self.action4, id="Edit", name="&Edit"),
        )
        builder = TaskActionManagerBuilder(task=Task(menu_bar=schema))
        actual = builder.create_menu_bar_manager()
        desired = MenuBarManager(
            MenuManager(self.action1, self.action2, id="File", name="&File"),
            MenuManager(self.action3, self.action4, id="Edit", name="&Edit"),
            id="MenuBar",
        )
        self.assertActionElementsEqual(actual, desired)

    # Tests about schema additions -----------------------------------------

    def test_additions_menu_bar(self):
        """ Does constructing a menu with a few additions work?
        """
        schema = MenuBarSchema(
            MenuSchema(
                GroupSchema(self.action1, self.action2, id="FileGroup"),
                id="File",
            )
        )
        extras = [
            SchemaAddition(
                factory=lambda: self.action3,
                before="action1",
                path="MenuBar/File/FileGroup",
            ),
            SchemaAddition(
                factory=lambda: self.action4,
                before="action1",
                path="MenuBar/File/FileGroup",
            ),
            SchemaAddition(
                factory=lambda: self.action5, path="MenuBar/File/FileGroup"
            ),
        ]
        builder = TaskActionManagerBuilder(
            task=Task(menu_bar=schema, extra_actions=extras)
        )
        actual = builder.create_menu_bar_manager()
        desired = MenuBarManager(
            MenuManager(
                Group(
                    self.action3,
                    self.action4,
                    self.action1,
                    self.action2,
                    self.action5,
                    id="FileGroup",
                ),
                id="File",
            ),
            id="MenuBar",
        )
        self.assertActionElementsEqual(actual, desired)

    def test_extra_menu(self):
        """ Test contributing a whole new menu to the menu bar. """

        # Initial menu.
        schema = MenuBarSchema(
            MenuSchema(
                GroupSchema(self.action1, id="FileGroup"), id="FileMenu"
            )
        )

        # Contributed menu.
        extra_menu = MenuSchema(
            GroupSchema(self.action2, id="BarGroup"), id="DummyActionsMenu"
        )

        extra_actions = [
            SchemaAddition(
                path="MenuBar",
                factory=lambda: extra_menu,
                id="DummyActionsSMenu",
            )
        ]

        # Build the final menu.
        builder = TaskActionManagerBuilder(
            task=Task(menu_bar=schema, extra_actions=extra_actions)
        )
        actual = builder.create_menu_bar_manager()

        desired = MenuBarManager(
            MenuManager(Group(self.action1, id="FileGroup"), id="FileMenu"),
            MenuManager(
                Group(self.action2, id="BarGroup"), id="DummyActionsMenu"
            ),
            id="MenuBar",
        )

        self.assertActionElementsEqual(actual, desired)

    # Tests about merging schemas -----------------------------------------#

    def test_merging_redundant_items(self):
        """ Menus and groups with matching path are merged together. """

        # Initial menu.
        schema = MenuBarSchema(
            MenuSchema(
                GroupSchema(self.action1, id="FileGroup"),
                name="File menu number one",
                id="FileMenu",
            )
        )

        # Contributed menus.
        extra_menu = MenuSchema(
            GroupSchema(self.action2, id="FileGroup"),
            name="File menu number two",
            id="FileMenu",
        )

        extra_actions = [
            SchemaAddition(
                path="MenuBar",
                factory=lambda: extra_menu,
                id="DummyActionsSMenu",
            )
        ]

        # Build the final menu.
        builder = TaskActionManagerBuilder(
            task=Task(menu_bar=schema, extra_actions=extra_actions)
        )
        actual = builder.create_menu_bar_manager()

        # Note that we expect the name of the menu to be inherited from
        # the menu in the menu bar schema that is defined first.
        desired = MenuBarManager(
            MenuManager(
                Group(self.action1, self.action2, id="FileGroup"),
                name="File menu number one",
                id="FileMenu",
            ),
            id="MenuBar",
        )
        self.assertActionElementsEqual(actual, desired)

    def test_unwanted_merge(self):
        """ Test that we don't have automatic merges due to forgetting to set
        a schema ID. """
        with self.unique_id_context_manager():
            # Initial menu.
            schema = MenuBarSchema(
                MenuSchema(
                    GroupSchema(self.action1, id="FileGroup"), name="File 1"
                )
            )

            # Contributed menus.
            extra_menu = MenuSchema(
                GroupSchema(self.action2, id="FileGroup"), name="File 2"
            )

            extra_actions = [
                SchemaAddition(
                    path="MenuBar",
                    factory=lambda: extra_menu,
                    id="DummyActionsSMenu",
                )
            ]

            # Build the final menu.
            builder = TaskActionManagerBuilder(
                task=Task(menu_bar=schema, extra_actions=extra_actions)
            )
            actual = builder.create_menu_bar_manager()

            # Note that we expect the name of the menu to be inherited from
            # the menu in the menu bar schema that is defined first.
            desired = MenuBarManager(
                MenuManager(
                    Group(self.action1, id="FileGroup"),
                    name="File 1",
                    id="MenuSchema_1",
                ),
                MenuManager(
                    Group(self.action2, id="FileGroup"),
                    name="File 2",
                    id="MenuSchema_2",
                ),
                id="MenuBar",
            )
            self.assertActionElementsEqual(actual, desired)

    def test_merging_items_with_same_id_but_different_class(self):
        """ Schemas with the same path but different types (menus, groups)
        are not merged together.

        Having a group and a menu with the same path is of course bad practice,
        but we need a predictable outcome.

        """

        # Initial menu.
        schema = MenuBarSchema(
            MenuSchema(
                GroupSchema(self.action1, id="FileGroup"), id="FileSchema"
            )
        )

        # Contributed menus.
        extra_group = GroupSchema(self.action2, id="FileSchema")

        extra_actions = [
            SchemaAddition(
                path="MenuBar",
                factory=(lambda: extra_group),
                id="DummyActionsSMenu",
            )
        ]

        # Build the final menu.
        builder = TaskActionManagerBuilder(
            task=Task(menu_bar=schema, extra_actions=extra_actions)
        )
        actual = builder.create_menu_bar_manager()

        desired = MenuBarManager(
            MenuManager(Group(self.action1, id="FileGroup"), id="FileSchema"),
            Group(self.action2, id="FileSchema"),
            id="MenuBar",
        )
        self.assertActionElementsEqual(actual, desired)

    def test_merging_redundant_items_that_are_not_schemas(self):
        """ Items that are not schemas cannot be merged, but we should
        not crash, either. """

        # Initial menu.
        schema = MenuBarSchema(
            # This menu is not a schema...
            MenuManager(Group(self.action1, id="FileGroup"), id="FileMenu")
        )

        # Contributed menus.
        extra_menu = MenuSchema(
            GroupSchema(self.action2, id="FileGroup"), id="FileMenu"
        )

        extra_actions = [
            SchemaAddition(
                path="MenuBar",
                factory=lambda: extra_menu,
                id="DummyActionsSMenu",
            )
        ]

        # Build the final menu.
        builder = TaskActionManagerBuilder(
            task=Task(menu_bar=schema, extra_actions=extra_actions)
        )
        actual = builder.create_menu_bar_manager()

        desired = MenuBarManager(
            MenuManager(Group(self.action1, id="FileGroup"), id="FileMenu"),
            MenuManager(Group(self.action2, id="FileGroup"), id="FileMenu"),
            id="MenuBar",
        )
        self.assertActionElementsEqual(actual, desired)

    # Tests about ordering -------------------------------------------------

    def test_absolute_ordering(self):
        """ Does specifying absolute_position work?
        """
        schema = MenuBarSchema(
            MenuSchema(
                GroupSchema(self.action1, self.action2, id="FileGroup"),
                id="File",
            )
        )
        extras = [
            SchemaAddition(
                factory=lambda: self.action3,
                absolute_position="last",
                path="MenuBar/File/FileGroup",
            ),
            SchemaAddition(
                factory=lambda: self.action4,
                absolute_position="first",
                path="MenuBar/File/FileGroup",
            ),
            SchemaAddition(
                factory=lambda: self.action5,
                absolute_position="first",
                path="MenuBar/File/FileGroup",
            ),
        ]
        builder = TaskActionManagerBuilder(
            task=Task(menu_bar=schema, extra_actions=extras)
        )
        actual = builder.create_menu_bar_manager()
        desired = MenuBarManager(
            MenuManager(
                Group(
                    self.action4,
                    self.action5,
                    self.action1,
                    self.action2,
                    self.action3,
                    id="FileGroup",
                ),
                id="File",
            ),
            id="MenuBar",
        )
        self.assertActionElementsEqual(actual, desired)

    def test_absolute_and_before_after(self):
        """ Does specifying absolute_position along with before, after work?
        """
        schema = MenuBarSchema(
            MenuSchema(
                GroupSchema(self.action1, self.action2, id="FileGroup"),
                id="File",
            )
        )
        extras = [
            SchemaAddition(
                factory=lambda: self.action3,
                id="action3",
                after="action2",
                path="MenuBar/File/FileGroup",
            ),
            SchemaAddition(
                factory=lambda: self.action4,
                after="action3",
                path="MenuBar/File/FileGroup",
            ),
            SchemaAddition(
                factory=lambda: self.action5,
                id="action5",
                absolute_position="last",
                path="MenuBar/File/FileGroup",
            ),
            SchemaAddition(
                factory=lambda: self.action6,
                absolute_position="last",
                before="action5",
                path="MenuBar/File/FileGroup",
            ),
        ]
        builder = TaskActionManagerBuilder(
            task=Task(menu_bar=schema, extra_actions=extras)
        )
        actual = builder.create_menu_bar_manager()
        desired = MenuBarManager(
            MenuManager(
                Group(
                    self.action1,
                    self.action2,
                    self.action3,
                    self.action4,
                    self.action6,
                    self.action5,
                    id="FileGroup",
                ),
                id="File",
            ),
            id="MenuBar",
        )
        self.assertActionElementsEqual(actual, desired)
