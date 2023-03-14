# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest.mock import patch

from traits.testing.api import UnittestTools

from pyface.action.api import Action, MenuManager
from pyface.gui import GUI
from pyface.window import Window


class WidgetMixin(UnittestTools):
    """ Mixin which provides standard methods for all widgets. """

    def setUp(self):
        self.gui = GUI()

        self.parent = self._create_parent()
        self.parent.create()
        self.addCleanup(self._destroy_parent)
        self.gui.process_events()

        self.widget = self._create_widget()

        self.parent.open()
        self.gui.process_events()

    def _create_parent(self):
        return Window()

    def _create_widget(self):
        return self._create_widget_simple(parent=self.parent.control)

    def _create_widget_simple(self, **traits):
        raise NotImplementedError()

    def _create_widget_control(self):
        self.widget.create()
        self.addCleanup(self._destroy_widget)
        self.widget.show(True)
        self.gui.process_events()

    def _destroy_parent(self):
        self.parent.destroy()
        self.gui.process_events()
        self.parent = None

    def _destroy_widget(self):
        self.widget.destroy()
        self.gui.process_events()
        self.widget = None

    def test_lazy_parent_create(self):
        self.widget = self._create_widget_simple()
        self.widget.create(parent=self.parent.control)
        try:
            self.assertIsNotNone(self.widget.control)
            self.widget.show(True)
            self.gui.process_events()
        finally:
            self.widget.destroy()

    def test_widget_tooltip(self):
        self._create_widget_control()
        self.widget.tooltip = "New tooltip."
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_tooltip(), "New tooltip.")

    def test_widget_tooltip_cleanup(self):
        widget = self._create_widget()
        with patch.object(widget, '_tooltip_updated', return_value=None) as updated:
            widget.create()
            try:
                widget.show(True)
                self.gui.process_events()
            finally:
                widget.destroy()
                self.gui.process_events()

            widget.tooltip = "New tooltip."

            updated.assert_not_called()

        widget = None

    def test_widget_menu(self):
        self._create_widget_control()
        self.widget.context_menu = MenuManager(Action(name="Test"), name="Test")

        self.gui.process_events()

    def test_widget_context_menu_cleanup(self):
        widget = self._create_widget()
        with patch.object(widget, '_context_menu_updated', return_value=None) as updated:
            widget.create()
            try:
                widget.show(True)
                self.gui.process_events()
            finally:
                widget.destroy()
                self.gui.process_events()

            widget.context_menu = MenuManager(Action(name="Test"), name="Test")

            updated.assert_not_called()

        widget = None
