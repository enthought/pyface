from traits.testing.unittest_tools import unittest

try:
    from enaml.widgets.api import Label
    from traits_enaml.testing.gui_test_assistant import GuiTestAssistant
except ImportError:
    @unittest.skip("Enaml not installed")
    class GuiTestAssistant(object):
        pass

from pyface.tasks.api import EnamlTaskPane


class DummyTaskPane(EnamlTaskPane):

    def create_component(self):
        return Label(text='test label')


class TestEnamlTaskPane(GuiTestAssistant, unittest.TestCase):

    ###########################################################################
    # 'TestCase' interface
    ###########################################################################

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.task_pane = DummyTaskPane()
        with self.event_loop():
            self.task_pane.create(None)

    def tearDown(self):
        if self.task_pane.control is not None:
            with self.delete_widget(self.task_pane.control):
                self.task_pane.destroy()
        del self.task_pane
        GuiTestAssistant.tearDown(self)

    ###########################################################################
    # Tests
    ###########################################################################

    def test_creation(self):
        self.assertIsInstance(self.task_pane.component, Label)
        self.assertIsNotNone(self.task_pane.control)

    def test_destroy(self):
        task_pane = self.task_pane
        with self.delete_widget(task_pane.control):
            task_pane.destroy()
        self.assertIsNone(task_pane.control)
        # Second destruction is a no-op.
        task_pane.destroy()
