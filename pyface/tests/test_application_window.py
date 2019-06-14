from __future__ import absolute_import

import unittest

from ..action.api import Action, MenuManager, MenuBarManager, StatusBarManager, ToolBarManager
from ..application_window import ApplicationWindow
from ..toolkit import toolkit_object
from ..image_resource import ImageResource

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestApplicationWindow(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = ApplicationWindow()

    def tearDown(self):
        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()
        GuiTestAssistant.tearDown(self)

    def test_close(self):
        # test that close works even when no control
        self.window.close()

    def test_open_close(self):
        # test that opening and closing works as expected
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                with self.event_loop():
                    self.window.open()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                with self.event_loop():
                    self.window.close()

    def test_show(self):
        # test that show and hide works as expected
        with self.event_loop():
            self.window._create()
            self.window.show(True)
        with self.event_loop():
            self.window.show(False)
        with self.event_loop():
            self.window.close()

    def test_activate(self):
        # test that activation works as expected
        with self.event_loop():
            self.window.open()
        with self.event_loop():
            self.window.activate()
        with self.event_loop():
            self.window.close()

    def test_position(self):
        # test that default position works as expected
        self.window.position = (100, 100)
        with self.event_loop():
            self.window.open()
        with self.event_loop():
            self.window.close()

    def test_reposition(self):
        # test that changing position works as expected
        with self.event_loop():
            self.window.open()
        with self.event_loop():
            self.window.position = (100, 100)
        with self.event_loop():
            self.window.close()

    def test_size(self):
        # test that default size works as expected
        self.window.size = (100, 100)
        with self.event_loop():
            self.window.open()
        with self.event_loop():
            self.window.close()

    def test_resize(self):
        # test that changing size works as expected
        self.window.open()
        with self.event_loop():
            self.window.size = (100, 100)
        with self.event_loop():
            self.window.close()

    def test_title(self):
        # test that default title works as expected
        self.window.title = "Test Title"
        with self.event_loop():
            self.window.open()
        with self.event_loop():
            self.window.close()

    def test_retitle(self):
        # test that changing title works as expected
        with self.event_loop():
            self.window.open()
        with self.event_loop():
            self.window.title = "Test Title"
        with self.event_loop():
            self.window.close()

    def test_menubar(self):
        # test that menubar gets created as expected
        self.window.menu_bar_manager = MenuBarManager(
            MenuManager(
                Action(name="New"),
                Action(name="Open"),
                Action(name="Save"),
                Action(name="Close"),
                Action(name="Quit"),
                name='File',
            )
        )
        with self.event_loop():
            self.window._create()
        with self.event_loop():
            self.window.show(True)
        with self.event_loop():
            self.window.show(False)
        with self.event_loop():
            self.window.close()

    def test_toolbar(self):
        # test that toolbar gets created as expected
        self.window.tool_bar_managers = [
            ToolBarManager(
                Action(name="New", image=ImageResource('core')),
                Action(name="Open", image=ImageResource('core')),
                Action(name="Save", image=ImageResource('core')),
                Action(name="Close", image=ImageResource('core')),
                Action(name="Quit", image=ImageResource('core')),
            )
        ]
        with self.event_loop():
            self.window._create()
        with self.event_loop():
            self.window.show(True)
        with self.event_loop():
            self.window.show(False)
        with self.event_loop():
            self.window.close()

    def test_toolbar_changed(self):
        # test that toolbar gets changed as expected
        self.window.tool_bar_managers = [
            ToolBarManager(
                Action(name="New", image=ImageResource('core')),
                Action(name="Open", image=ImageResource('core')),
                Action(name="Save", image=ImageResource('core')),
                Action(name="Close", image=ImageResource('core')),
                Action(name="Quit", image=ImageResource('core')),
            )
        ]
        with self.event_loop():
            self.window._create()
        with self.event_loop():
            self.window.show(True)
        with self.event_loop():
            self.window.tool_bar_managers = [
                ToolBarManager(
                    Action(name="New", image=ImageResource('core')),
                    Action(name="Open", image=ImageResource('core')),
                    Action(name="Save", image=ImageResource('core')),
                    Action(name="Close", image=ImageResource('core')),
                    Action(name="Quit", image=ImageResource('core')),
                )
            ]
        with self.event_loop():
            self.window.show(False)
        with self.event_loop():
            self.window.close()

    def test_statusbar(self):
        # test that status bar gets created as expected
        self.window.status_bar_manager = StatusBarManager(
            message="hello world",
        )
        with self.event_loop():
            self.window._create()
        with self.event_loop():
            self.window.show(True)
        with self.event_loop():
            self.window.show(False)
        with self.event_loop():
            self.window.close()

    def test_statusbar_changed(self):
        # test that status bar gets changed as expected
        self.window.status_bar_manager = StatusBarManager(
            message="hello world",
        )
        with self.event_loop():
            self.window._create()
        with self.event_loop():
            self.window.show(True)
        with self.event_loop():
            self.window.status_bar_manager = StatusBarManager(
                message="goodbye world",
            )
        with self.event_loop():
            self.window.show(False)
        with self.event_loop():
            self.window.close()

    def test_icon(self):
        # test that status bar gets created as expected
        self.window.icon = ImageResource('core')
        with self.event_loop():
            self.window._create()
        with self.event_loop():
            self.window.show(True)
        with self.event_loop():
            self.window.show(False)
        with self.event_loop():
            self.window.close()
