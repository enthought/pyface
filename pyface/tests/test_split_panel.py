# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
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
            self.widget = SplitPanel(self.window.control)
        with self.event_loop():
            self.widget.destroy()

    def test_horizontal(self):
        # test that horizontal split works
        with self.event_loop():
            self.widget = SplitPanel(
                self.window.control, direction="horizontal"
            )
        with self.event_loop():
            self.widget.destroy()

    def test_ratio(self):
        # test that ratio works
        with self.event_loop():
            self.widget = SplitPanel(self.window.control, ratio=0.25)
        with self.event_loop():
            self.widget.destroy()

    def test_contents(self):
        # test that contents works
        with self.event_loop():
            self.widget = SplitPanel(
                self.window.control, lhs=HeadingText, rhs=HeadingText
            )
        with self.event_loop():
            self.widget.destroy()
