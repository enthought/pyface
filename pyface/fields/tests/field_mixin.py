# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from pyface.testing.layout_widget_mixin import LayoutWidgetMixin


class FieldMixin(LayoutWidgetMixin):
    """ Mixin which provides standard methods for all fields. """

    def test_text_field_alignment(self):
        self._create_widget_control()

        self.widget.alignment = 'right'
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_alignment(), 'right')
