from traits.testing.unittest_tools import unittest
from traits.etsconfig.api import ETSConfig

if ETSConfig.toolkit not in ['', 'qt4']:
    raise unittest.SkipTest("TestEnamlDockPane: Enaml does not support WX")

try:
    from enaml.widgets.api import Label
    from traits_enaml.testing.gui_test_assistant import GuiTestAssistant
except ImportError:
    raise unittest.SkipTest("Enaml not installed")

from pyface.tasks.api import EnamlDockPane, Task


class DummyDockPane(EnamlDockPane):

    def create_component(self):
        return Label(text='test label')


class TestEnamlDockPane(GuiTestAssistant, unittest.TestCase):

    ###########################################################################
    # 'TestCase' interface
    ###########################################################################

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dock_pane = DummyDockPane(task=Task(id='dummy_task'))
        with self.event_loop():
            self.dock_pane.create(None)

    def tearDown(self):
        if self.dock_pane.control is not None:
            with self.delete_widget(self.dock_pane.control):
                self.dock_pane.destroy()
        del self.dock_pane
        GuiTestAssistant.tearDown(self)

    ###########################################################################
    # Tests
    ###########################################################################

    def test_creation(self):
        self.assertIsInstance(self.dock_pane.component, Label)
        self.assertIsNotNone(self.dock_pane.control)

    def test_destroy(self):
        dock_pane = self.dock_pane
        with self.delete_widget(dock_pane.control):
            dock_pane.destroy()
        self.assertIsNone(dock_pane.control)
        # Second destruction is a no-op.
        dock_pane.destroy()
