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

from traits.etsconfig.api import ETSConfig

# Skip tests if Enaml is not installed or we're using the wx backend.
SKIP_REASON = None
if ETSConfig.toolkit not in {"", "qt", "qt4"}:
    SKIP_REASON = "Enaml does not support WX"
else:
    try:
        from enaml.widgets.api import Label
        from traits_enaml.testing.gui_test_assistant import GuiTestAssistant
    except ImportError:
        SKIP_REASON = "traits_enaml is not installed"

if SKIP_REASON is not None:
    # Dummy class so that the TestEnamlTaskPane class definition below
    # doesn't fail.

    class GuiTestAssistant(object):  # noqa: F811
        pass


from pyface.tasks.api import EnamlTaskPane


class DummyTaskPane(EnamlTaskPane):
    def create_component(self):
        return Label(text="test label")


@unittest.skipIf(SKIP_REASON is not None, SKIP_REASON)
class TestEnamlTaskPane(GuiTestAssistant, unittest.TestCase):

    # ------------------------------------------------------------------------
    # 'TestCase' interface
    # ------------------------------------------------------------------------

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

    # ------------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------------

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
