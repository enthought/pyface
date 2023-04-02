# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import platform
import unittest

from traits.api import TraitError
from traits.testing.optional_dependencies import numpy as np, requires_numpy

from pyface.toolkit import toolkit
from pyface.testing.layout_widget_mixin import LayoutWidgetMixin

# This import results in an error without numpy installed
# see enthought/pyface#742
if np is not None:
    from pyface.data_view.data_models.api import ArrayDataModel
from pyface.data_view.data_view_widget import DataViewWidget
from pyface.data_view.value_types.api import FloatValue


is_wx = (toolkit.toolkit == "wx")
is_linux = (platform.system() == "Linux")


# The available selection modes and types for the toolkit
selection_modes = DataViewWidget().trait("selection_mode").trait_type.values
selection_types = DataViewWidget().trait("selection_type").trait_type.values


@requires_numpy
class TestWidget(LayoutWidgetMixin, unittest.TestCase):

    def _create_widget_simple(self, **traits):
        self.data = np.arange(120.0).reshape(4, 5, 6)
        self.model = ArrayDataModel(data=self.data, value_type=FloatValue())
        traits.setdefault("data_model", self.model)
        return DataViewWidget(**traits)

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

    def test_init_selection(self):
        self.widget.selection = [((1, ), ())]
        self._create_widget_control()

        self.assertEqual(
            self.widget._get_control_selection(), [((1, ), ())]
        )

    def test_selection_mode_change(self):
        self._create_widget_control()
        self.widget.selection = [((1, 4), ()), ((2, 0), ())]

        self.widget.selection_mode = "single"

        self.assertEqual(self.widget._get_control_selection_mode(), "single")
        self.assertEqual(self.widget.selection, [])

        self.widget.selection = [((1, 4), ())]
        if "none" in selection_modes:
            self.widget.selection_mode = "none"

            self.assertEqual(self.widget._get_control_selection_mode(), "none")
            self.assertEqual(self.widget.selection, [])

        self.widget.selection_mode = "extended"

        self.assertEqual(self.widget._get_control_selection_mode(), "extended")
        self.assertEqual(self.widget.selection, [])

    @unittest.skipIf(
        len(selection_types) <= 1,
        "Changing selection types not supported",
    )
    def test_selection_type_change(self):
        self._create_widget_control()

        if "column" in selection_types:
            self.widget.selection_type = "column"
            self.assertEqual(
                self.widget._get_control_selection_type(),
                "column",
            )
            self.assertEqual(self.widget.selection, [])

        if "item" in selection_types:
            self.widget.selection_type = "item"
            self.assertEqual(self.widget._get_control_selection_type(), "item")
            self.assertEqual(self.widget.selection, [])

        if "row" in selection_types:
            self.widget.selection_type = "row"

            self.assertEqual(self.widget._get_control_selection_type(), "row")
            self.assertEqual(self.widget.selection, [])

    @unittest.skipIf(
        "none" not in selection_modes,
        "Selection mode 'none' not supported",
    )
    def test_selection_mode_none(self):
        self.widget.selection_mode = "none"
        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_mode(), "none")

        self.widget.selection = []
        self.gui.process_events()

        self.assertEqual(self.widget.selection, [])
        self.assertEqual(self.widget._get_control_selection(), [])

    @unittest.skipIf(
        "none" not in selection_modes,
        "Selection mode 'none' not supported",
    )
    def test_selection_mode_none_invalid(self):
        self.widget.selection_mode = "none"
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 4), ()), (2, 1), ()]

    def test_selection_mode_single(self):
        self.widget.selection_mode = "single"
        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_mode(), "single")

        self.widget.selection = [((1, 4), ())]
        self.gui.process_events()

        self.assertEqual(self.widget.selection, [((1, 4), ())])
        self.assertEqual(self.widget._get_control_selection(), [((1, 4), ())])

    def test_selection_mode_single_invalid(self):
        self.widget.selection_mode = "single"
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 4), ()), (2, 1), ()]

    @unittest.skipIf(
        is_wx and is_linux,
        "Selection mode 'extended' not working on Linux",
    )
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

    @unittest.skipIf(
        'column' not in selection_types,
        "Selection type 'column' not supported",
    )
    def test_selection_type_column(self):
        self.widget.selection_type = "column"
        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_type(), "column")

        self.widget.selection = [((0,), (2,)), ((1,), (4,))]

        self.gui.process_events()

        self.assertEqual(self.widget.selection, [((0,), (2,)), ((1,), (4,))])
        self.assertEqual(
            self.widget._get_control_selection(),
            [((0,), (2,)), ((1,), (4,))]
        )

    @unittest.skipIf(
        'item' not in selection_types,
        "Selection type 'item' not supported",
    )
    def test_selection_type_item(self):
        self.widget.selection_type = "item"
        self._create_widget_control()

        self.assertEqual(self.widget._get_control_selection_type(), "item")

        self.widget.selection = [((1, 4), (2,)), ((2, 0), (4,))]
        self.gui.process_events()

        self.assertEqual(
            self.widget.selection,
            [((1, 4), (2,)), ((2, 0), (4,))]
        )
        self.assertEqual(
            self.widget._get_control_selection(),
            [((1, 4), (2,)), ((2, 0), (4,))],
        )

    def test_selection_type_row_invalid_row_big(self):
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((10,), ())]

    def test_selection_type_row_invalid_row_long(self):
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 1, 1), ())]

    def test_selection_type_row_invalid_column(self):
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 2), (2,))]

    @unittest.skipIf(
        'item' not in selection_types,
        "Selection type 'column' not supported",
    )
    def test_selection_type_item_invalid_row_too_big(self):
        self.widget.selection_type = 'item'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 10), (2,))]

    @unittest.skipIf(
        'item' not in selection_types,
        "Selection type 'column' not supported",
    )
    def test_selection_type_item_invalid_row_too_long(self):
        self.widget.selection_type = 'item'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 4, 5, 6), (2,))]

    @unittest.skipIf(
        'item' not in selection_types,
        "Selection type 'column' not supported",
    )
    def test_selection_type_item_invalid_column(self):
        self.widget.selection_type = 'item'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 2), (10,))]

    @unittest.skipIf(
        'column' not in selection_types,
        "Selection type 'column' not supported",
    )
    def test_selection_type_column_invalid_row_too_long(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 4, 5, 6), (2,))]

    @unittest.skipIf(
        'column' not in selection_types,
        "Selection type 'column' not supported",
    )
    def test_selection_type_column_invalid_row_too_big(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((10,), (2,))]

    @unittest.skipIf(
        'column' not in selection_types,
        "Selection type 'column' not supported",
    )
    def test_selection_type_column_invalid_row_not_parent(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 2), (2,))]

    @unittest.skipIf(
        'column' not in selection_types,
        "Selection type 'column' not supported",
    )
    def test_selection_type_column_invalid_column(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((), (10,))]

    def test_selection_updated(self):
        self._create_widget_control()

        with self.assertTraitChanges(self.widget, 'selection'):
            self.widget._set_control_selection([((1, 4), ())])
            self.gui.process_events()

        self.assertEqual(self.widget.selection, [((1, 4), ())])
        self.assertEqual(
            self.widget._get_control_selection(),
            [((1, 4), ())],
        )

    def test_selection_updating_context_manager(self):
        self.assertFalse(self.widget._selection_updating_flag)

        with self.widget._selection_updating():
            self.assertTrue(self.widget._selection_updating_flag)
            with self.widget._selection_updating():
                self.assertTrue(self.widget._selection_updating_flag)
            self.assertTrue(self.widget._selection_updating_flag)

        self.assertFalse(self.widget._selection_updating_flag)

    def test_selection_updating_context_manager_exception(self):
        with self.assertRaises(ZeroDivisionError):
            with self.widget._selection_updating():
                with self.widget._selection_updating():
                    1/0

        self.assertFalse(self.widget._selection_updating_flag)
