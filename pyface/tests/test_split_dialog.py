from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..heading_text import HeadingText
from ..split_dialog import SplitDialog
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestDialog(unittest.TestCase, GuiTestAssistant):

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = SplitDialog()

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        GuiTestAssistant.tearDown(self)

    def test_create(self):
        # test that creation and destruction works as expected
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        self.dialog.destroy()

    def test_horizontal(self):
        # test that horizontal split works
        self.dialog.direction = 'horizontal'
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_ratio(self):
        # test that ratio works
        self.dialog.ratio = 0.25
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_contents(self):
        # test that contents works
        self.dialog.lhs = HeadingText
        self.dialog.rhs = HeadingText
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()
