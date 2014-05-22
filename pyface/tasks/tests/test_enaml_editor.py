from traits.testing.unittest_tools import unittest

try:
    from enaml.widgets.api import Label
    from traits_enaml.testing.gui_test_assistant import GuiTestAssistant
except ImportError:
    @unittest.skip("Enaml not installed")
    class GuiTestAssistant(object):
        pass

from traits.api import Str
from pyface.tasks.api import EnamlEditor


class DummyStrEditor(EnamlEditor):

    obj = Str

    def create_component(self):
        return Label(text=self.obj)

class TestEnamlEditor(GuiTestAssistant, unittest.TestCase):

    ###########################################################################
    # 'TestCase' interface
    ###########################################################################

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.obj = 'test message'
        self.editor = DummyStrEditor(obj=self.obj)
        with self.event_loop():
            self.editor.create(None)

    def tearDown(self):
        if self.editor.control is not None:
            with self.delete_widget(self.editor.control):
                self.editor.destroy()
        del self.editor
        GuiTestAssistant.tearDown(self)

    ###########################################################################
    # Tests
    ###########################################################################

    def test_creation(self):
        self.assertIsInstance(self.editor.component, Label)
        self.assertEqual(self.editor.component.text, self.obj)
        self.assertIsNotNone(self.editor.control)

    def test_destroy(self):
        editor = self.editor
        with self.delete_widget(editor.control):
            editor.destroy()
        self.assertIsNone(editor.control)
        # Second destruction is a no-op.
        editor.destroy()
