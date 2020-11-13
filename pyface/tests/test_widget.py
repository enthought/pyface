# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from traits.api import Instance
from traits.testing.unittest_tools import UnittestTools

from ..application_window import ApplicationWindow
from ..toolkit import toolkit_object
from ..widget import Widget

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

is_qt = (toolkit_object.toolkit in {"qt4", "qt"})


class ConcreteWidget(Widget):
    def _create_control(self, parent):
        if toolkit_object.toolkit == "wx":
            import wx

            control = wx.Window(parent)
            control.Enable(self.enabled)
            control.Show(self.visible)
        elif toolkit_object.toolkit in {"qt4", "qt"}:
            from pyface.qt import QtGui

            control = QtGui.QWidget(parent)
            control.setEnabled(self.enabled)
            control.setVisible(self.visible)
        else:
            control = None
        return control


class MainWindow(ApplicationWindow):

    widget = Instance(ConcreteWidget)

    def _create_contents(self, parent):
        """ Create and return the window's contents.
        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control to be used as the parent for
            widgets in the contents.

        Returns
        -------
        control : toolkit control
            A control to be used for contents of the window.
        """
        self.widget = ConcreteWidget(parent=parent)
        self.widget._create()
        return self.widget.control


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
        with self.assertTraitChanges(self.widget, "visible", count=1):
            self.widget.show(False)

        self.assertFalse(self.widget.visible)

    def test_visible(self):
        with self.assertTraitChanges(self.widget, "visible", count=1):
            self.widget.visible = False

        self.assertFalse(self.widget.visible)

    def test_enable(self):
        with self.assertTraitChanges(self.widget, "enabled", count=1):
            self.widget.enable(False)

        self.assertFalse(self.widget.enabled)

    def test_enabled(self):
        with self.assertTraitChanges(self.widget, "enabled", count=1):
            self.widget.enabled = False

        self.assertFalse(self.widget.enabled)


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
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

        with self.assertTraitChanges(self.widget, "visible", count=1):
            with self.event_loop():
                self.widget.show(False)

        self.assertFalse(self.widget.control.isVisible())

    def test_visible(self):
        with self.event_loop():
            self.widget._create()

        with self.assertTraitChanges(self.widget, "visible", count=1):
            with self.event_loop():
                self.widget.visible = False

        self.assertFalse(self.widget.control.isVisible())

    def test_contents_visible(self):
        window = MainWindow()
        window._create()

        try:
            with self.event_loop():
                window.open()

            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = False

            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = True
        finally:
            window.destroy()

    def test_contents_hidden(self):
        window = MainWindow()
        window._create()

        try:
            with self.event_loop():
                window.open()
                window.widget.visible = False

            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = False

            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = True
        finally:
            window.destroy()

    @unittest.skipUnless(is_qt, "Qt-specific test of hidden state")
    def test_contents_hide_external_change(self):
        window = MainWindow()
        window._create()

        try:
            with self.event_loop():
                window.open()

            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = False

            self.assertFalse(window.widget.control.isVisible())
            self.assertFalse(window.widget.control.isHidden())

            with self.assertTraitChanges(window.widget, "visible"):
                with self.event_loop():
                    window.widget.control.hide()

            self.assertFalse(window.widget.control.isVisible())
            self.assertTrue(window.widget.control.isHidden())

            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = True

            self.assertFalse(window.widget.control.isVisible())
            self.assertTrue(window.widget.control.isHidden())
        finally:
            window.destroy()

    def test_enable(self):
        with self.event_loop():
            self.widget._create()

        with self.assertTraitChanges(self.widget, "enabled", count=1):
            with self.event_loop():
                self.widget.enable(False)

        self.assertFalse(self.widget.control.isEnabled())

    def test_enabled(self):
        with self.event_loop():
            self.widget._create()

        with self.assertTraitChanges(self.widget, "enabled", count=1):
            with self.event_loop():
                self.widget.enabled = False

        self.assertFalse(self.widget.control.isEnabled())
