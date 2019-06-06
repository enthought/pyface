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

from traits.api import Enum, HasTraits
from traits.testing.unittest_tools import UnittestTools

from pyface.gui import GUI
from pyface.toolkit import toolkit
from pyface.util.testing import has_traitsui
from pyface.window import Window
from ..traitsui_widget_action import TraitsUIWidgetAction


@unittest.skipIf(not has_traitsui(), "TraitsUI not installed")
class TestTraitsUIWidgetAction(unittest.TestCase, UnittestTools):

    def setUp(self):
        self.gui = GUI()
        self.parent = Window()
        self.parent._create()
        self.parent.open()
        self.addCleanup(self._destroy_parent)
        self.gui.process_events()

    def _destroy_parent(self):
        self.parent.destroy()
        self.gui.process_events()
        self.parent = None

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
        control = action.create_control(self.parent.control)
        self.gui.process_events()

        editor = control._ui.get_editors('value')[0]

        with self.assertTraitChanges(action, 'value', count=1):
            if toolkit.toolkit in {'qt', 'qt4'}:
                editor.control.setCurrentIndex(1)
                editor.control.activated.emit(1)
            elif toolkit.toolkit == 'wx':
                import wx
                event = wx.CommandEvent(wx.EVT_CHOICE.typeId,
                                        editor.control.GetId())
                event.SetString('b')
                wx.PostEvent(editor.control.GetEventHandler(), event)
            else:
                self.skipTest("Unknown toolkit")
            self.gui.process_events()

        self.assertEqual(action.value, 'b')

    def test_traitsui_widget_action_model(self):
        from traitsui.api import View, Item

        class SimpleEnumAction(TraitsUIWidgetAction):
            view = View(Item('value'))

        model = self.create_model()
        action = SimpleEnumAction(name="Simple", model=model)
        control = action.create_control(self.parent.control)
        self.gui.process_events()

        editor = control._ui.get_editors('value')[0]

        with self.assertTraitChanges(model, 'value', count=1):
            if toolkit.toolkit in {'qt', 'qt4'}:
                editor.control.setCurrentIndex(1)
                editor.control.activated.emit(1)
            elif toolkit.toolkit == 'wx':
                import wx
                event = wx.CommandEvent(wx.EVT_CHOICE.typeId,
                                        editor.control.GetId())
                event.SetString('b')
                wx.PostEvent(editor.control.GetEventHandler(), event)
            else:
                self.skipTest("Unknown toolkit")
            self.gui.process_events()

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
        control = action.create_control(self.parent.control)
        self.gui.process_events()

        editor = control._ui.get_editors('value')[0]

        with self.assertTraitChanges(model, 'value', count=1):
            if toolkit.toolkit in {'qt', 'qt4'}:
                editor.control.setCurrentIndex(1)
                editor.control.activated.emit(1)
            elif toolkit.toolkit == 'wx':
                import wx
                event = wx.CommandEvent(wx.EVT_CHOICE.typeId,
                                        editor.control.GetId())
                event.SetString('b')
                wx.PostEvent(editor.control.GetEventHandler(), event)
            else:
                self.skipTest("Unknown toolkit")
            self.gui.process_events()

        self.assertEqual(model.value, 'b')

        editor = control._ui.get_editors('value')[1]

        with self.assertTraitChanges(action, 'value', count=1):
            if toolkit.toolkit in {'qt', 'qt4'}:
                editor.control.setCurrentIndex(2)
                editor.control.activated.emit(2)
            elif toolkit.toolkit == 'wx':
                event = wx.CommandEvent(wx.EVT_CHOICE.typeId,
                                        editor.control.GetId())
                event.SetString('c')
                wx.PostEvent(editor.control.GetEventHandler(), event)
            else:
                self.skipTest("Unknown toolkit")
            self.gui.process_events()

        self.assertEqual(action.value, 'c')
