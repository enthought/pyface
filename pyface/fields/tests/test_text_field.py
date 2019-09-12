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

import unittest

from pyface.toolkit import toolkit
from ..text_field import TextField
from .field_mixin import FieldMixin


is_wx = (toolkit.toolkit == 'wx')


class TestTextField(FieldMixin, unittest.TestCase):

    def _create_widget(self):
        return TextField(
            parent=self.parent.control,
            value='test',
            tooltip='Dummy',
        )

    # Tests ------------------------------------------------------------------

    def test_text_field(self):
        self._create_widget_control()

        self.widget.value = 'new value'
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), 'new value')

    def test_text_field_set(self):
        self._create_widget_control()

        with self.assertTraitChanges(self.widget, 'value', count=1):
            self.widget._set_control_value('new value')
            self.gui.process_events()

        self.assertEqual(self.widget.value, 'new value')

    def test_text_field_echo(self):
        self.widget.echo = 'password'
        self._create_widget_control()

        self.assertEqual(self.widget._get_control_echo(), 'password')

    @unittest.skipIf(is_wx, "Can't change password mode for wx after control "
                     "creation.")
    def test_text_field_echo_change(self):
        self._create_widget_control()

        self.widget.echo = 'password'
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_echo(), 'password')

    def test_text_field_placeholder(self):
        self._create_widget_control()

        self.widget.placeholder = 'test'
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_placeholder(), 'test')

    def test_text_field_readonly(self):
        self.widget.read_only = True
        self._create_widget_control()

        self.gui.process_events()

        self.assertEqual(self.widget._get_control_read_only(), True)

    @unittest.skipIf(is_wx, "Can't change read_only mode for wx after control "
                     "creation.")
    def test_text_field_readonly_change(self):
        self._create_widget_control()

        self.widget.read_only = True
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_read_only(), True)

