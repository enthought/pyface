from __future__ import absolute_import

import unittest

from ..gui import GUI
from ..image_resource import ImageResource
from ..splash_screen import SplashScreen
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestWindow(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = SplashScreen()

    def tearDown(self):
        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()

        del self.window
        GuiTestAssistant.tearDown(self)

    def test_destroy(self):
        # test that destroy works even when no control
        with self.event_loop():
            self.window.destroy()

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
        # test that show works as expected
        with self.event_loop():
            self.window._create()
        with self.event_loop():
            self.window.show(True)
        with self.event_loop():
            self.window.show(False)
        with self.event_loop():
            self.window.destroy()

    def test_image(self):
        # test that images work
        self.window.image = ImageResource('core')
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                with self.event_loop():
                    self.window.open()

        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                with self.event_loop():
                    self.window.close()

    def test_text(self):
        # test that images work
        self.window.text = "Splash screen"
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                with self.event_loop():
                    self.window.open()

        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                with self.event_loop():
                    self.window.close()

    def test_text_changed(self):
        # test that images work
        # XXX this throws a non-failing exception on wx
        #     - probably the way the test is written.
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                with self.event_loop():
                    self.window.open()

        with self.event_loop():
            self.window.text = "Splash screen"

        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                with self.event_loop():
                    self.window.close()
