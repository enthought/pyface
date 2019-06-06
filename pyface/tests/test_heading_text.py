from __future__ import absolute_import

import unittest

from ..heading_text import HeadingText
from ..image_resource import ImageResource
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestHeadingText(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = Window()
        self.window._create()

    def tearDown(self):
        if self.widget.control is not None:
            with self.delete_widget(self.widget.control):
                self.widget.destroy()

        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()

        del self.widget
        del self.window
        GuiTestAssistant.tearDown(self)

    def test_lifecycle(self):
        # test that destroy works
        with self.event_loop():
            self.widget = HeadingText(self.window.control)
        with self.event_loop():
            self.widget.destroy()

    def test_message(self):
        # test that create works with message
        with self.event_loop():
            self.widget = HeadingText(self.window.control, text="Hello")
        with self.event_loop():
            self.widget.destroy()

    def test_image(self):
        # test that image works
        # XXX this image doesn't make sense here, but that's fine
        # XXX this isn't implemented in qt4 backend, but shouldn't fail
        with self.event_loop():
            self.widget = HeadingText(
                self.window.control, image=ImageResource('core.png')
            )
        with self.event_loop():
            self.widget.destroy()

    def test_level(self):
        # test that create works with level
        # XXX this image doesn't make sense here, but that's fine
        # XXX this isn't implemented in qt4 backend, but shouldn't fail
        with self.event_loop():
            self.widget = HeadingText(self.window.control, level=2)
        with self.event_loop():
            self.widget.destroy()
