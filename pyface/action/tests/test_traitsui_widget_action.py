from __future__ import absolute_import

from traits.api import Enum, HasTraits
from traits.testing.unittest_tools import unittest, UnittestTools

from pyface.util.testing import has_traitsui
from ..traitsui_widget_action import TraitsUIWidgetAction


@unittest.skipIf(not has_traitsui(), "TraitsUI not installed")
class TestTraitsUIWidgetAction(unittest.TestCase, UnittestTools):

    def create_model(self):
        from traitsui.api import View, Item

        class SimpleEnum(HasTraits):
            value = Enum('a', 'b', 'c')
            view = View(Item('value'))

        return SimpleEnum()

    def test_traitsui_widget_action(self):
        from traitsui.api import View, Item

        class SimpleEnumAction(TraitsUIWidgetAction):
            value = Enum('a', 'b', 'c')
            view = View(Item('value'))

        action = SimpleEnumAction(name="Simple")
        parent = None
        control = action.create_control(parent)

        editor = control._ui.get_editors('value')[0]

        with self.assertTraitChanges(action, 'value', count=1):
            editor.control.setCurrentIndex(1)

        self.assertEqual(action.value, 'b')

    def test_traitsui_widget_action_model(self):
        from traitsui.api import View, Item

        class SimpleEnumAction(TraitsUIWidgetAction):
            view = View(Item('value'))

        model = self.create_model()
        action = SimpleEnumAction(name="Simple", model=model)
        parent = None
        control = action.create_control(parent)

        editor = control._ui.get_editors('value')[0]

        with self.assertTraitChanges(model, 'value', count=1):
            editor.control.setCurrentIndex(1)

        self.assertEqual(model.value, 'b')

    def test_traitsui_widget_action_model_view(self):
        from traitsui.api import HGroup, View, Item

        class ComplexEnumAction(TraitsUIWidgetAction):
            value = Enum('a', 'b', 'c')

            view = View(
                HGroup(
                    Item('value'),
                    Item('action.value'),
                )
            )

        model = self.create_model()
        action = ComplexEnumAction(name="Simple", model=model)
        parent = None
        control = action.create_control(parent)
        print(control._ui._editors)

        editor = control._ui.get_editors('value')[0]

        with self.assertTraitChanges(model, 'value', count=1):
            editor.control.setCurrentIndex(1)

        self.assertEqual(model.value, 'b')

        editor = control._ui.get_editors('value')[1]

        with self.assertTraitChanges(action, 'value', count=1):
            editor.control.setCurrentIndex(2)

        self.assertEqual(action.value, 'c')
