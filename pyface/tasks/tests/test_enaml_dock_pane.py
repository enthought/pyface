import unittest

from traits.etsconfig.api import ETSConfig

# Skip tests if Enaml is not installed or we're using the wx backend.
SKIP_REASON = None
if ETSConfig.toolkit not in ['', 'qt4']:
    SKIP_REASON = "Enaml does not support WX"
else:
    try:
        from enaml.widgets.api import Label
        from traits_enaml.testing.gui_test_assistant import GuiTestAssistant
    except ImportError:
        SKIP_REASON = "Enaml not installed"

if SKIP_REASON is not None:
    # Dummy class so that the TestEnamlTaskPane class definition below
    # doesn't fail.

    class GuiTestAssistant(object):
        pass

from pyface.tasks.api import EnamlDockPane, Task


class DummyDockPane(EnamlDockPane):

    def create_component(self):
        return Label(text='test label')


@unittest.skipIf(SKIP_REASON is not None, SKIP_REASON)
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
