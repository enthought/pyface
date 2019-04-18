from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from pyface.action.api import Action, MenuManager
from pyface.image_resource import ImageResource
from ..combo_field import ComboField


class TestComboField(unittest.TestCase):

    def test_combo_field(self):
        widget = ComboField(
            parent=None,
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget.value = 'two'

            self.assertEqual(widget._get_control_value(), 'two')
            self.assertEqual(widget._get_control_text(), 'two')
        finally:
            widget.destroy()

    def test_combo_field_set(self):
        widget = ComboField(
            parent=None,
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget._set_control_value('two')

            self.assertEqual(widget.value, 'two')
        finally:
            widget.destroy()

    def test_combo_field_formatter(self):
        widget = ComboField(
            parent=None,
            values=[1, 2, 3, 4],
            tooltip='Dummy',
            formatter=str,
        )

        widget._create()
        try:
            widget.show(True)
            widget.value = 2

            self.assertEqual(widget._get_control_value(), 2)
            self.assertEqual(widget._get_control_text(), '2')
        finally:
            widget.destroy()

    def test_combo_field_formatter_changed(self):
        widget = ComboField(
            parent=None,
            values=[1, 2, 3, 4],
            value=2,
            tooltip='Dummy',
            formatter=str,
        )

        widget._create()
        try:
            widget.show(True)
            widget.formatter = 'Number {}'.format

            self.assertEqual(widget._get_control_value(), 2)
            self.assertEqual(widget._get_control_text(), 'Number 2')
        finally:
            widget.destroy()

    def test_combo_field_formatter_set(self):
        widget = ComboField(
            parent=None,
            values=[1, 2, 3, 4],
            tooltip='Dummy',
            formatter=str,
        )

        widget._create()
        try:
            widget.show(True)
            widget._set_control_value(2)

            self.assertEqual(widget.value, 2)
        finally:
            widget.destroy()

    def test_combo_field_icon_formatter(self):
        image = ImageResource('question')
        widget = ComboField(
            parent=None,
            values=[1, 2, 3, 4],
            tooltip='Dummy',
            formatter=lambda x: (image, str(x)),
        )

        widget._create()
        try:
            widget.show(True)
            widget.value = 2

            self.assertEqual(widget._get_control_value(), 2)
            self.assertEqual(widget._get_control_text(), '2')
        finally:
            widget.destroy()

    def test_combo_field_values(self):
        widget = ComboField(
            parent=None,
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget.values = ['four', 'five', 'one', 'six']

            self.assertEqual(widget.value, 'four')
        finally:
            widget.destroy()

    def test_combo_field_tooltip(self):
        widget = ComboField(
            parent=None,
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)

            widget.tooltip = "New tooltip."

            self.assertEqual(widget._get_control_tooltip(), "New tooltip.")
        finally:
            widget.destroy()

    def test_combo_field_menu(self):
        widget = ComboField(
            parent=None,
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget.menu = MenuManager(Action(name='Test'), name='Test')
        finally:
            widget.destroy()
