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


from traits.api import Str
from pyface.tasks.api import EnamlEditor


class DummyStrEditor(EnamlEditor):

    obj = Str()

    def create_component(self):
        return Label(text=self.obj)


@unittest.skipIf(SKIP_REASON is not None, SKIP_REASON)
class TestEnamlEditor(GuiTestAssistant, unittest.TestCase):

    # ------------------------------------------------------------------------
    # 'TestCase' interface
    # ------------------------------------------------------------------------

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.obj = "test message"
        self.editor = DummyStrEditor(obj=self.obj)
        with self.event_loop():
            self.editor.create(None)

    def tearDown(self):
        if self.editor.control is not None:
            with self.delete_widget(self.editor.control):
                self.editor.destroy()
        del self.editor
        GuiTestAssistant.tearDown(self)

    # ------------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------------

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
