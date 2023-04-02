# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from ..heading_text import HeadingText
from ..split_application_window import SplitApplicationWindow
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestSplitApplicationWindow(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = SplitApplicationWindow()

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
        with self.assertTraitChanges(self.window, "opening", count=1):
            with self.assertTraitChanges(self.window, "opened", count=1):
                with self.event_loop():
                    self.window.open()

        with self.assertTraitChanges(self.window, "closing", count=1):
            with self.assertTraitChanges(self.window, "closed", count=1):
                with self.event_loop():
                    self.window.close()

    def test_horizontal_split(self):
        # test that horizontal split works
        self.window.direction = "horizontal"
        with self.assertTraitChanges(self.window, "opening", count=1):
            with self.assertTraitChanges(self.window, "opened", count=1):
                with self.event_loop():
                    self.window.open()

        with self.assertTraitChanges(self.window, "closing", count=1):
            with self.assertTraitChanges(self.window, "closed", count=1):
                with self.event_loop():
                    self.window.close()

    def test_contents(self):
        # test that contents works
        self.window.lhs = HeadingText
        self.window.rhs = HeadingText
        with self.assertTraitChanges(self.window, "opening", count=1):
            with self.assertTraitChanges(self.window, "opened", count=1):
                with self.event_loop():
                    self.window.open()

        with self.assertTraitChanges(self.window, "closing", count=1):
            with self.assertTraitChanges(self.window, "closed", count=1):
                with self.event_loop():
                    self.window.close()

    def test_contents_toolkit_control(self):
        # test that toolkit control contents works
        def create_toolkit_control(parent):
            widget = HeadingText(parent)
            widget.create()
            return widget.control

        self.window.lhs = create_toolkit_control
        self.window.rhs = create_toolkit_control
        with self.assertTraitChanges(self.window, "opening", count=1):
            with self.assertTraitChanges(self.window, "opened", count=1):
                with self.event_loop():
                    self.window.open()

        with self.assertTraitChanges(self.window, "closing", count=1):
            with self.assertTraitChanges(self.window, "closed", count=1):
                with self.event_loop():
                    self.window.close()

    def test_ratio(self):
        # test that ratio split works
        self.window.ratio = 0.25
        with self.assertTraitChanges(self.window, "opening", count=1):
            with self.assertTraitChanges(self.window, "opened", count=1):
                with self.event_loop():
                    self.window.open()

        with self.assertTraitChanges(self.window, "closing", count=1):
            with self.assertTraitChanges(self.window, "closed", count=1):
                with self.event_loop():
                    self.window.close()
