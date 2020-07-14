# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from traits.testing.optional_dependencies import numpy as np, requires_numpy
from traits.testing.unittest_tools import UnittestTools

from pyface.gui import GUI
from pyface.toolkit import toolkit
from pyface.window import Window

from pyface.data_view.data_models.api import ArrayDataModel
from pyface.data_view.data_view_widget import DataViewWidget
from pyface.data_view.value_types.api import FloatValue


is_wx = (toolkit.toolkit == "wx")


@requires_numpy
class TestWidget(unittest.TestCase, UnittestTools):

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
        self.data = np.arange(120.0).reshape(4, 5, 6)
        self.model = ArrayDataModel(data=self.data, value_type=FloatValue())
        return DataViewWidget(
            parent=self.parent.control,
            data_model=self.model
        )

    def _create_widget_control(self):
        self.widget._create()
        self.addCleanup(self._destroy_widget)
        self.parent.show(True)
        self.gui.process_events()

    def _destroy_parent(self):
        self.parent.destroy()
        self.gui.process_events()
        self.parent = None

    def _destroy_widget(self):
        self.widget.destroy()
        self.gui.process_events()
        self.widget = None

    def test_defaults(self):
        self.assertTrue(self.widget.header_visible)

    def test_lifecycle(self):
        self._create_widget_control()

    def test_header_visible(self):
        self._create_widget_control()

        self.assertTrue(self.widget._get_control_header_visible())

        self.widget.header_visible = False
        self.gui.process_events()

        self.assertFalse(self.widget._get_control_header_visible())

    def test_header_visible_before_control(self):
        self.widget.header_visible = False

        self._create_widget_control()
        self.assertFalse(self.widget._get_control_header_visible())

    def test_selection_mode_change(self):
        self._create_widget_control()
        self.selection = [((1, 4), (2,)), ((2, 0), (4,))]

        self.widget.selection_mode = "single"

        self.assertEqual(self.widget._get_control_selection_mode(), "single")
        self.assertEqual(self.widget.selection, [])

        self.selection = [((1, 4), (2,))]
        if not is_wx:
            self.widget.selection_mode = "none"

            self.assertEqual(self.widget._get_control_selection_mode(), "none")
            self.assertEqual(self.widget.selection, [])

        self.widget.selection_mode = "extended"

        self.assertEqual(self.widget._get_control_selection_mode(), "extended")
        self.assertEqual(self.widget.selection, [])

    @unittest.skipIf(is_wx, "Selection type changing not supported")
    def test_selection_type_change(self):
        self._create_widget_control()

        self.widget.selection_type = "column"

        self.assertEqual(self.widget._get_control_selection_type(), "column")
        self.assertEqual(self.widget.selection, [])

        self.widget.selection_type = "item"

        self.assertEqual(self.widget._get_control_selection_type(), "item")
        self.assertEqual(self.widget.selection, [])

        self.widget.selection_type = "row"

        self.assertEqual(self.widget._get_control_selection_type(), "row")
        self.assertEqual(self.widget.selection, [])

    @unittest.skipIf(is_wx, "Selection mode 'none' not supported")
    def test_selection_mode_none(self):
        self.widget.selection_mode = "none"

        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_mode(), "none")

        self.widget.selection = []
        self.gui.process_events()

        self.assertEqual(self.widget.selection, [])
        self.assertEqual(self.widget._get_control_selection(), [])

    def test_selection_mode_single(self):
        self.widget.selection_mode = "single"

        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_mode(), "single")

        self.widget.selection = [((1, 4), ())]

        self.gui.process_events()

        self.assertEqual(self.widget.selection, [((1, 4), ())])
        self.assertEqual(self.widget._get_control_selection(),  [((1, 4), ())])

    def test_selection_mode_extended(self):
        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_mode(), "extended")

        self.widget.selection = [((1, 4), ()), ((2, 0), ())]
        self.gui.process_events()

        self.assertEqual(self.widget.selection, [((1, 4), ()), ((2, 0), ())])
        self.assertEqual(
            self.widget._get_control_selection(),
            [((1, 4), ()), ((2, 0), ())],
        )

    @unittest.skipIf(is_wx, "Selection type 'column' not supported")
    def test_selection_type_column(self):
        self.widget.selection_type = "column"

        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_type(), "column")

        self.widget.selection = [((0,), (2,)), ((1,), (4,))]

        self.gui.process_events()

        self.assertEqual(self.widget.selection, [((0,), (2,)), ((1,), (4,))])
        self.assertEqual(self.widget._get_control_selection(),  [((0,), (2,)), ((1,), (4,))])

    @unittest.skipIf(is_wx, "Selection mode 'item' not supported")
    def test_selection_type_item(self):
        self.widget.selection_type = "item"

        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_type(), "item")

        self.widget.selection = [((1, 4), (2,)), ((2, 0), (4,))]
        self.gui.process_events()

        self.assertEqual(self.widget.selection, [((1, 4), (2,)), ((2, 0), (4,))])
        self.assertEqual(
            self.widget._get_control_selection(),
            [((1, 4), (2,)), ((2, 0), (4,))],
        )

    def test_selection_invalid_row(self):
        self._create_widget_control()

        self.widget.selection = [((7, 10), ())]

        self.gui.process_events()

        self.assertEqual(self.widget.selection, [((7, 10), ())])
        self.assertEqual(self.widget._get_control_selection(),  [((7, 10), ())])

    @unittest.skipIf(is_wx, "Selection mode 'item' not supported")
    def test_selection_invalid_item(self):
        self.widget.selection_type = 'item'
        self._create_widget_control()

        self.widget.selection = [((1, 4, 5, 6), (2,))]

        self.gui.process_events()

        self.assertEqual(self.widget.selection, [((1, 4, 5, 6), (2,))])
        self.assertEqual(
            self.widget._get_control_selection(),
            [((1, 4, 5, 6), (2,))]
        )
