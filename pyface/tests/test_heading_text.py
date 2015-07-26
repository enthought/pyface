from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..gui import GUI
from ..heading_text import HeadingText
from ..image_resource import ImageResource
from ..window import Window


class TestHeadingText(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.window = Window()
        self.window._create()

    def tearDown(self):
        self.widget.destroy()
        self.window.destroy()

    def test_lifecycle(self):
        # test that destroy works
        self.widget = HeadingText(self.window.control)
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()

    def test_message(self):
        # test that create works with message
        self.widget = HeadingText(self.window.control, text="Hello")
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()

    def test_image(self):
        # test that image works
        # XXX this image doesn't make sense here, but that's fine
        # XXX this isn't implemented in qt4 backend, but shouldn't fail
        self.widget = HeadingText(self.window.control, image=ImageResource('core.png'))
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()

    def test_level(self):
        # test that create works with level
        # XXX this image doesn't make sense here, but that's fine
        # XXX this isn't implemented in qt4 backend, but shouldn't fail
        self.widget = HeadingText(self.window.control, level=2)
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()
