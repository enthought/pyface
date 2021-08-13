# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from pyface.testing.layout_widget_mixin import LayoutWidgetMixin

from pyface.action.api import Action, MenuManager
from pyface.gui import GUI
from pyface.window import Window


class FieldMixin(LayoutWidgetMixin):
    """ Mixin which provides standard methods for all fields. """

    def test_field_tooltip(self):
        self._create_widget_control()
        self.widget.tooltip = "New tooltip."
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_tooltip(), "New tooltip.")

    def test_field_menu(self):
        self._create_widget_control()
        self.widget.menu = MenuManager(Action(name="Test"), name="Test")
        self.gui.process_events()
