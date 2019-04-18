from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from pyface.action.api import Action, MenuManager
from ..spin_field import SpinField


class TestSpinField(unittest.TestCase):

    def test_spin_field(self):
        widget = SpinField(
            parent=None,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget.value = 5

            self.assertEqual(widget._get_control_value(), 5)
        finally:
            widget.destroy()

    def test_spin_field_set(self):
        widget = SpinField(
            parent=None,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget._set_control_value(5)

            self.assertEqual(widget.value, 5)
        finally:
            widget.destroy()

    def test_spin_field_bounds(self):
        widget = SpinField(
            parent=None,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)

            widget.bounds = (10, 50)

            self.assertEqual(widget._get_control_bounds(), (10, 50))
            self.assertEqual(widget._get_control_value(), 10)
            self.assertEqual(widget.value, 10)
        finally:
            widget.destroy()

    def test_spin_field_tooltip(self):
        widget = SpinField(
            parent=None,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)

            widget.tooltip = "New tooltip."

            self.assertEqual(widget._get_control_tooltip(), "New tooltip.")
        finally:
            widget.destroy()

    def test_spin_field_menu(self):
        widget = SpinField(
            parent=None,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget.menu = MenuManager(Action(name='Test'), name='Test')
        finally:
            widget.destroy()
