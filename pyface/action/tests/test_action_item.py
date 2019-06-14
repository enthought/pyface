from __future__ import absolute_import

import unittest

from traits.testing.unittest_tools import UnittestTools

from pyface.image_cache import ImageCache
from pyface.toolkit import toolkit_object
from pyface.widget import Widget
from pyface.window import Window
from ..action import Action
from ..action_controller import ActionController
from ..action_item import ActionItem
from ..menu_manager import MenuManager
from ..menu_bar_manager import MenuBarManager
from ..tool_bar_manager import ToolBarManager


class FalseActionController(ActionController):

    def can_add_to_menu(self, action):
        """ Returns True if the action can be added to a menu/menubar. """

        return False

    def can_add_to_toolbar(self, action):
        """ Returns True if the action can be added to a toolbar. """

        return False


class TestActionItem(unittest.TestCase, UnittestTools):

    def setUp(self):
        # test whether function is called by updating list
        # XXX should really use mock
        self.memo = []

        def perform():
            self.memo.append('called')

        self.action = Action(name='Test', on_perform=perform)

    def control_factory(self, parent, action):
        if toolkit_object.toolkit == 'wx':
            import wx
            control = wx.Control(parent)
        elif toolkit_object.toolkit == 'qt4':
            from pyface.qt import QtGui
            control = QtGui.QWidget(parent)
        else:
            control = None
        return control

    def test_default_id(self):
        action_item = ActionItem(action=self.action)
        self.assertEqual(action_item.id, 'Test')

    def test_enabled_changed(self):
        # XXX these are only one-way changes, which seems wrong.
        action_item = ActionItem(action=self.action)
        with self.assertTraitChanges(self.action, 'enabled', count=1):
            action_item.enabled = False
        self.assertFalse(self.action.enabled)
        with self.assertTraitChanges(self.action, 'enabled', count=1):
            action_item.enabled = True
        self.assertTrue(self.action.enabled)

    def test_visible_changed(self):
        # XXX these are only one-way changes, which seems wrong.
        action_item = ActionItem(action=self.action)
        with self.assertTraitChanges(self.action, 'visible', count=1):
            action_item.visible = False
        self.assertFalse(self.action.visible)
        with self.assertTraitChanges(self.action, 'visible', count=1):
            action_item.visible = True
        self.assertTrue(self.action.visible)

    def test_destroy(self):
        action_item = ActionItem(action=self.action)
        # XXX test that it calls action.destroy
        action_item.destroy()

    def test_add_to_menu(self):
        window = Window()
        window.open()
        action_item = ActionItem(action=self.action)
        menu_bar_manager = MenuBarManager()
        menu_manager = MenuManager(name='Test')
        menu_bar = menu_bar_manager.create_menu_bar(window.control)
        menu = menu_manager.create_menu(menu_bar)
        action_item.add_to_menu(window.control, menu, None)
        window.close()

    def test_add_to_menu_controller(self):
        window = Window()
        window.open()
        action_item = ActionItem(action=self.action)
        menu_bar_manager = MenuBarManager()
        menu_manager = MenuManager(name='Test')
        menu_bar = menu_bar_manager.create_menu_bar(window.control)
        menu = menu_manager.create_menu(menu_bar)
        controller = ActionController()
        action_item.add_to_menu(window.control, menu, controller)
        window.close()

    def test_add_to_menu_controller_false(self):
        window = Window()
        window.open()
        action_item = ActionItem(action=self.action)
        menu_bar_manager = MenuBarManager()
        menu_manager = MenuManager(name='Test')
        menu_bar = menu_bar_manager.create_menu_bar(window.control)
        menu = menu_manager.create_menu(menu_bar)
        controller = FalseActionController()
        action_item.add_to_menu(window.control, menu, controller)
        window.close()

    def test_add_to_toolbar(self):
        window = Window()
        window.open()
        action_item = ActionItem(action=self.action)
        toolbar_manager = ToolBarManager(name='Test')
        image_cache = ImageCache(height=32, width=32)
        menu = toolbar_manager.create_tool_bar(window.control)
        action_item.add_to_toolbar(window.control, menu, image_cache, None, True)
        window.close()

    def test_add_to_toolbar_no_label(self):
        window = Window()
        window.open()
        action_item = ActionItem(action=self.action)
        toolbar_manager = ToolBarManager(name='Test')
        image_cache = ImageCache(height=32, width=32)
        menu = toolbar_manager.create_tool_bar(window.control)
        action_item.add_to_toolbar(window.control, menu, image_cache, None, False)
        window.close()

    def test_add_to_toolbar_controller(self):
        window = Window()
        window.open()
        action_item = ActionItem(action=self.action)
        toolbar_manager = ToolBarManager(name='Test')
        image_cache = ImageCache(height=32, width=32)
        menu = toolbar_manager.create_tool_bar(window.control)
        controller = ActionController()
        action_item.add_to_toolbar(window.control, menu, image_cache,
                                   controller, True)
        window.close()

    def test_add_to_toolbar_controller_false(self):
        window = Window()
        window.open()
        action_item = ActionItem(action=self.action)
        toolbar_manager = ToolBarManager(name='Test')
        image_cache = ImageCache(height=32, width=32)
        menu = toolbar_manager.create_tool_bar(window.control)
        controller = FalseActionController()
        action_item.add_to_toolbar(window.control, menu, image_cache,
                                   controller, True)
        window.close()

    def test_add_to_toolbar_widget(self):
        self.action.style = "widget"
        self.action.control_factory = self.control_factory

        window = Window()
        window.open()
        action_item = ActionItem(action=self.action)
        toolbar_manager = ToolBarManager(name='Test')
        image_cache = ImageCache(height=32, width=32)
        menu = toolbar_manager.create_tool_bar(window.control)

        try:
            action_item.add_to_toolbar(window.control, menu, image_cache, None, True)
        finally:
            window.close()
