# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import sys
import unittest

from traits.api import Instance
from traits.testing.api import UnittestTools

from pyface.testing.widget_mixin import WidgetMixin
from ..application_window import ApplicationWindow
from ..toolkit import toolkit_object
from ..widget import Widget

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

is_qt = (toolkit_object.toolkit in {"qt4", "qt"})
is_linux = (sys.platform == "linux")
is_mac = (sys.platform == "darwin")


class ConcreteWidget(Widget):
    def _create_control(self, parent):
        if toolkit_object.toolkit == "wx":
            import wx

            control = wx.Window(parent)
            control.Enable(self.enabled)
            control.Show(self.visible)
        elif toolkit_object.toolkit in {"qt4", "qt"}:
            from pyface.qt import QtGui
            from pyface.qt.QtCore import Qt

            control = QtGui.QWidget(parent)
            control.setEnabled(self.enabled)
            control.setVisible(self.visible)
            control.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
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
        self.widget.create()
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
            self.widget.create()

    def test__create(self):
        # _create is not Implemented
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
            self.widget.create()
        with self.event_loop():
            self.widget.destroy()

    def test_initialize(self):
        self.widget.visible = False
        self.widget.enabled = False
        with self.event_loop():
            self.widget.create()

        self.assertFalse(self.widget.control.isVisible())
        self.assertFalse(self.widget.control.isEnabled())

    def test_show(self):
        with self.event_loop():
            self.widget.create()

        with self.assertTraitChanges(self.widget, "visible", count=1):
            with self.event_loop():
                self.widget.show(False)

        self.assertFalse(self.widget.control.isVisible())

    def test_visible(self):
        with self.event_loop():
            self.widget.create()

        with self.assertTraitChanges(self.widget, "visible", count=1):
            with self.event_loop():
                self.widget.visible = False

        self.assertFalse(self.widget.control.isVisible())

    def test_contents_visible(self):
        window = MainWindow()
        window.create()

        try:
            with self.event_loop():
                window.open()

            # widget visible trait stays True when parent is hidden
            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = False

            # widget visible trait stays True when parent is shown
            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = True
        finally:
            window.destroy()

    def test_contents_hidden(self):
        window = MainWindow()
        window.create()

        try:
            with self.event_loop():
                window.open()
                window.widget.visible = False

            # widget visible trait stays False when parent is hidden
            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = False

            # widget visible trait stays False when parent is shown
            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = True
        finally:
            window.destroy()

    @unittest.skipUnless(is_qt, "Qt-specific test of hidden state")
    def test_contents_hide_external_change(self):
        window = MainWindow()
        window.create()

        try:
            with self.event_loop():
                window.open()

            # widget visibile trait stays True when parent is hidden
            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = False

            self.assertFalse(window.widget.control.isVisible())
            self.assertFalse(window.widget.control.isHidden())

            # widget visibile trait becomes False when widget is hidden
            with self.assertTraitChanges(window.widget, "visible"):
                with self.event_loop():
                    window.widget.control.hide()

            self.assertFalse(window.widget.visible)
            self.assertFalse(window.widget.control.isVisible())
            self.assertTrue(window.widget.control.isHidden())

            # widget visibile trait stays False when parent is shown
            with self.assertTraitDoesNotChange(window.widget, "visible"):
                with self.event_loop():
                    window.visible = True

            self.assertFalse(window.widget.control.isVisible())
            self.assertTrue(window.widget.control.isHidden())
        finally:
            window.destroy()

    @unittest.skipUnless(is_qt, "Qt-specific test of hidden state")
    def test_show_widget_with_parent_is_invisible_qt(self):
        # Test setting the widget visible to true when its parent visibility
        # is false.
        window = MainWindow()
        window.create()

        try:
            # given
            with self.event_loop():
                window.open()
                window.widget.visible = False

            with self.event_loop():
                window.visible = False

            # when
            with self.event_loop():
                window.widget.visible = True

            # then
            self.assertTrue(window.widget.visible)
            self.assertFalse(window.widget.control.isVisible())
            self.assertFalse(window.widget.control.isHidden())

        finally:
            window.destroy()

    @unittest.skipUnless(is_qt, "Qt-specific test of hidden state")
    def test_show_widget_then_parent_is_invisible_qt(self):
        # Test showing the widget when the parent is also visible, and then
        # make the parent invisible
        window = MainWindow()
        window.create()

        try:
            # given
            with self.event_loop():
                window.open()
                window.visible = True

            with self.event_loop():
                window.widget.visible = True

            # when
            with self.event_loop():
                window.visible = False

            # then
            self.assertTrue(window.widget.visible)
            self.assertFalse(window.widget.control.isVisible())
            self.assertFalse(window.widget.control.isHidden())

        finally:
            window.destroy()

    def test_enable(self):
        with self.event_loop():
            self.widget.create()

        with self.assertTraitChanges(self.widget, "enabled", count=1):
            with self.event_loop():
                self.widget.enable(False)

        self.assertFalse(self.widget.control.isEnabled())

    def test_enabled(self):
        with self.event_loop():
            self.widget.create()

        with self.assertTraitChanges(self.widget, "enabled", count=1):
            with self.event_loop():
                self.widget.enabled = False

        self.assertFalse(self.widget.control.isEnabled())

    @unittest.skipUnless(
        is_mac,
        "Broken on Linux and Windows",
    )
    def test_focus(self):
        with self.event_loop():
            self.widget.create()

        self.assertFalse(self.widget.has_focus())

        with self.event_loop():
            self.widget.focus()

        self.assertTrue(self.widget.has_focus())


class TestWidgetCommon(WidgetMixin, unittest.TestCase):

    def _create_widget_simple(self, **traits):
        traits.setdefault("tooltip", "Dummy")
        return ConcreteWidget(**traits)
