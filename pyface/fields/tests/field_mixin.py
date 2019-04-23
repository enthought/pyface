# Copyright (c) 2019, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from traits.testing.unittest_tools import UnittestTools

from pyface.action.api import Action, MenuManager
from pyface.gui import GUI
from pyface.window import Window


class FieldMixin(UnittestTools):
    """ Mixin which provides standard methods for all fields. """

    def setUp(self):
        self.gui = GUI()

        self.parent = Window()
        self.parent._create()
        self.addCleanup(self._destroy_parent)
        self.gui.process_events()

        self.widget = self._create_widget()

        self.parent.open()
        self.gui.process_events()

    def _create_widget(self):
        raise NotImplementedError()

    def _create_widget_control(self):
        self.widget._create()
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

    # Tests ------------------------------------------------------------------

    def test_field_tooltip(self):
        self._create_widget_control()
        self.widget.tooltip = "New tooltip."
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_tooltip(), "New tooltip.")

    def test_field_menu(self):
        self._create_widget_control()
        self.widget.menu = MenuManager(Action(name='Test'), name='Test')
        self.gui.process_events()
