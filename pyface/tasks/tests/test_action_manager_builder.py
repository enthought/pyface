# Standard library imports.
import unittest

# Enthought library imports.
from pyface.action.api import Action, ActionItem, ActionManager, Group, \
     MenuManager, MenuBarManager
from pyface.tasks.action.api import GroupSchema, MenuSchema, MenuBarSchema, \
     SchemaAddition
from pyface.tasks.action.task_action_manager_builder import \
     TaskActionManagerBuilder
from pyface.tasks.api import Task


class ActionManagerBuilderTestCase(unittest.TestCase):

    def assertActionElementsEqual(self, first, second):
        """ Checks that two action managers are (logically) equivalent.
        """
        children1 = children2 = []
        self.assertEquals(type(first), type(second))
        self.assertEquals(first.id, second.id)

        if isinstance(first, ActionItem):
            self.assertEquals(first.action.name, second.action.name)

        elif isinstance(first, ActionManager):
            if not isinstance(first, MenuBarManager):
                self.assertEquals(first.name, second.name)
            children1, children2 = first.groups, second.groups

        elif isinstance(first, Group):
            self.assertEquals(first.separator, second.separator)
            children1, children2 = first.items, second.items

        self.assertEquals(len(children1), len(children2))
        for i in xrange(len(children1)):
            self.assertActionElementsEqual(children1[i], children2[i])

    def setUp(self):
        """ Create some dummy actions to use while testing.
        """
        for i in xrange(1, 7):
            action_id = 'action%i' % i
            setattr(self, action_id, Action(id=action_id, name='Action %i' % i))

    def test_simple_menu_bar(self):
        """ Does constructing a simple menu with no additions work?
        """
        schema = MenuBarSchema(
            MenuSchema(self.action1, self.action2, id='File', name='&File'),
            MenuSchema(self.action3, self.action4, id='Edit', name='&Edit'))
        builder = TaskActionManagerBuilder(task=Task(menu_bar=schema))
        actual = builder.create_menu_bar_manager()
        desired = MenuBarManager(MenuManager(self.action1, self.action2,
                                             id='File', name='&File'),
                                 MenuManager(self.action3, self.action4,
                                             id='Edit', name='&Edit'),
                                 id='MenuBar')
        self.assertActionElementsEqual(actual, desired)

    def test_additions_menu_bar(self):
        """ Does constructing a menu with a few additions work?
        """
        schema = MenuBarSchema(
            MenuSchema(GroupSchema(self.action1, self.action2, id='FileGroup'),
                       id='File'))
        extras = [ SchemaAddition(factory=lambda: self.action3, 
                                  before='action1',
                                  path='MenuBar/File/FileGroup'),
                   SchemaAddition(factory=lambda: self.action4, 
                                  before='action1',
                                  path='MenuBar/File/FileGroup'),
                   SchemaAddition(factory=lambda: self.action5,
                                  path='MenuBar/File/FileGroup')]
        builder = TaskActionManagerBuilder(task=Task(menu_bar=schema,
                                                     extra_actions=extras))
        actual = builder.create_menu_bar_manager()
        desired = MenuBarManager(MenuManager(Group(self.action3, self.action4,
                                                   self.action1, self.action2,
                                                   self.action5,
                                                   id='FileGroup'),
                                             id='File'),
                                 id='MenuBar')
        self.assertActionElementsEqual(actual, desired)

    def test_absolute_ordering(self):
        """ Does specifying absolute_position work?
        """
        schema = MenuBarSchema(
            MenuSchema(GroupSchema(self.action1, self.action2, id='FileGroup'),
                       id='File'))
        extras = [ SchemaAddition(factory=lambda: self.action3,
                                  absolute_position='last',
                                  path='MenuBar/File/FileGroup'),
                   SchemaAddition(factory=lambda: self.action4,
                                  absolute_position='first',
                                  path='MenuBar/File/FileGroup'),
                   SchemaAddition(factory=lambda: self.action5,
                                  absolute_position='first',
                                  path='MenuBar/File/FileGroup')]
        builder = TaskActionManagerBuilder(task=Task(menu_bar=schema,
                                                     extra_actions=extras))
        actual = builder.create_menu_bar_manager()
        desired = MenuBarManager(MenuManager(Group(self.action4, self.action5,
                                                   self.action1, self.action2,
                                                   self.action3,
                                                   id='FileGroup'),
                                             id='File'),
                                 id='MenuBar')
        self.assertActionElementsEqual(actual, desired)

    def test_absolute_and_before_after(self):
        """ Does specifying absolute_position along with before, after work?
        """
        schema = MenuBarSchema(
            MenuSchema(GroupSchema(self.action1, self.action2, id='FileGroup'),
                       id='File'))
        extras = [ SchemaAddition(factory=lambda: self.action3,
                                  id='action3',
                                  after='action2',
                                  path='MenuBar/File/FileGroup'),
                   SchemaAddition(factory=lambda: self.action4,
                                  after='action3',
                                  path='MenuBar/File/FileGroup'),
                   SchemaAddition(factory=lambda: self.action5,
                                  id='action5',
                                  absolute_position='last',
                                  path='MenuBar/File/FileGroup'),
                   SchemaAddition(factory=lambda: self.action6,
                                  absolute_position='last',
                                  before='action5',
                                  path='MenuBar/File/FileGroup')
                   ]
        builder = TaskActionManagerBuilder(task=Task(menu_bar=schema,
                                                     extra_actions=extras))
        actual = builder.create_menu_bar_manager()
        desired = MenuBarManager(MenuManager(Group(self.action1, self.action2,
                                                   self.action3, self.action4,
                                                   self.action6, self.action5,
                                                   id='FileGroup'),
                                             id='File'),
                                 id='MenuBar')
        self.assertActionElementsEqual(actual, desired)

if __name__ == '__main__':
    unittest.main()
