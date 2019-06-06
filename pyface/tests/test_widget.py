from __future__ import absolute_import

import unittest

from traits.testing.unittest_tools import UnittestTools

from ..toolkit import toolkit_object
from ..widget import Widget

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


class ConcreteWidget(Widget):
    def _create_control(self, parent):
        if toolkit_object.toolkit == 'wx':
            import wx
            control = wx.Window(parent)
            control.Enable(self.enabled)
            control.Show(self.visible)
        elif toolkit_object.toolkit == 'qt4':
            from pyface.qt import QtGui
            control = QtGui.QWidget(parent)
            control.setEnabled(self.enabled)
            control.setVisible(self.visible)
        else:
            control = None
        return control


class TestWidget(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.widget = Widget()

    def tearDown(self):
        del self.widget

    def test_defaults(self):
        self.assertTrue(self.widget.enabled)
        self.assertTrue(self.widget.visible)

    def test_create(self):
        # create is not Implemented
        with self.assertRaises(NotImplementedError):
            self.widget._create()

    def test_destroy(self):
        # test that destroy works even when no control
        self.widget.destroy()

    def test_show(self):
        with self.assertTraitChanges(self.widget, 'visible', count=1):
            self.widget.show(False)

        self.assertFalse(self.widget.visible)

    def test_visible(self):
        with self.assertTraitChanges(self.widget, 'visible', count=1):
            self.widget.visible = False

        self.assertFalse(self.widget.visible)

    def test_enable(self):
        with self.assertTraitChanges(self.widget, 'enabled', count=1):
            self.widget.enable(False)

        self.assertFalse(self.widget.enabled)

    def test_enabled(self):
        with self.assertTraitChanges(self.widget, 'enabled', count=1):
            self.widget.enabled = False

        self.assertFalse(self.widget.enabled)


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestConcreteWidget(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.widget = ConcreteWidget()

    def tearDown(self):
        if self.widget.control is not None:
            with self.delete_widget(self.widget.control):
                self.widget.destroy()
        del self.widget
        GuiTestAssistant.tearDown(self)

    def test_lifecycle(self):
        with self.event_loop():
            self.widget._create()
        with self.event_loop():
            self.widget.destroy()

    def test_initialize(self):
        self.widget.visible = False
        self.widget.enabled = False
        with self.event_loop():
            self.widget._create()

        self.assertFalse(self.widget.control.isVisible())
        self.assertFalse(self.widget.control.isEnabled())

    def test_show(self):
        with self.event_loop():
            self.widget._create()

        with self.assertTraitChanges(self.widget, 'visible', count=1):
            with self.event_loop():
                self.widget.show(False)

        self.assertFalse(self.widget.control.isVisible())

    def test_visible(self):
        with self.event_loop():
            self.widget._create()

        with self.assertTraitChanges(self.widget, 'visible', count=1):
            with self.event_loop():
                self.widget.visible = False

        self.assertFalse(self.widget.control.isVisible())

    def test_enable(self):
        with self.event_loop():
            self.widget._create()

        with self.assertTraitChanges(self.widget, 'enabled', count=1):
            with self.event_loop():
                self.widget.enable(False)

        self.assertFalse(self.widget.control.isEnabled())

    def test_enabled(self):
        with self.event_loop():
            self.widget._create()

        with self.assertTraitChanges(self.widget, 'enabled', count=1):
            with self.event_loop():
                self.widget.enabled = False

        self.assertFalse(self.widget.control.isEnabled())
