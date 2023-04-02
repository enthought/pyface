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

from pyface.tasks.api import SplitEditorAreaPane
from pyface.toolkit import toolkit_object

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestSplitEditorAreaPane(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.area_pane = SplitEditorAreaPane()

    def tearDown(self):
        if self.area_pane.control is not None:
            with self.delete_widget(self.area_pane.control):
                self.area_pane.destroy()
        GuiTestAssistant.tearDown(self)

    def test_create_destroy(self):
        # test that creating and destroying works as expected
        with self.event_loop():
            self.area_pane.create(None)
        with self.event_loop():
            self.area_pane.destroy()
