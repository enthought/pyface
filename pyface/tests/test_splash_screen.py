from __future__ import absolute_import

from traits.testing.unittest_tools import unittest, UnittestTools

from ..gui import GUI
from ..image_resource import ImageResource
from ..splash_screen import SplashScreen


class TestWindow(unittest.TestCase, UnittestTools):

    def setUp(self):
        self.gui = GUI()
        self.window = SplashScreen()

    def test_destroy(self):
        # test that destroy works even when no control
        self.window.destroy()

    def test_open_close(self):
        # test that opening and closing works as expected
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_show(self):
        # test that show works as expected
        self.window._create()
        self.window.show(True)
        self.gui.process_events()
        self.window.show(False)
        self.gui.process_events()
        self.window.destroy()

    def test_image(self):
        # test that images work
        self.window.image = ImageResource('core')
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_text(self):
        # test that images work
        self.window.text = "Splash screen"
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_text_changed(self):
        # test that images work
        # XXX this throws a non-failing exception on wx
        #     - probably the way the test is written.
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        self.window.text = "Splash screen"
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()
