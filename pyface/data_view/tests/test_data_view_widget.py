# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from itertools import cycle
import platform
import unittest

from traits.api import (
    Callable,
    provides,
    TraitError,
)
from traits.observation.api import (
    pop_exception_handler,
    push_exception_handler,
)
from traits.testing.optional_dependencies import numpy as np, requires_numpy
from traits.testing.unittest_tools import UnittestTools

from pyface.gui import GUI
from pyface.toolkit import toolkit
from pyface.window import Window

from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.data_models.api import ArrayDataModel
from pyface.data_view.data_view_widget import DataViewWidget
from pyface.data_view.i_data_view_widget import (
    IDataViewWidget, MDataViewWidget,
)
from pyface.data_view.value_types.api import FloatValue, TextValue
from pyface.ui.null.widget import Widget as NullWidget


is_wx = (toolkit.toolkit == "wx")
is_linux = (platform.system() == "Linux")


class FakeDataModel(AbstractDataModel):

    fake_get_column_count = Callable()

    fake_can_have_children = Callable()

    fake_get_row_count = Callable()

    fake_get_value = Callable()

    fake_get_value_type = Callable()

    def get_column_count(self):
        return self.fake_get_column_count()

    def can_have_children(self, row):
        return self.fake_can_have_children(row)

    def get_row_count(self, row):
        return self.fake_get_row_count(row)

    def get_value(self, row, column):
        return self.fake_get_value(row, column)

    def get_value_type(self, row, column):
        return self.fake_get_value_type(row, column)


class FakeControl:

    def __init__(self):
        self.header_visible = False
        self.selection_type = "row"
        self.selection_mode = "none"
        self.selection = []


@provides(IDataViewWidget)
class FakeWidget(MDataViewWidget, NullWidget):

    def _get_control_header_visible(self):
        return self.control_header_visible

    def _set_control_header_visible(self, header_visible):
        self.control.header_visible = header_visible

    def _get_control_selection_type(self):
        return self.control.selection_type

    def _set_control_selection_type(self, selection_type):
        self.control.selection_type = selection_type

    def _get_control_selection_mode(self):
        return self.control.selection_mode

    def _set_control_selection_mode(self, selection_mode):
        self.control.selection_mode = selection_mode

    def _get_control_selection(self):
        return self.control.selection

    def _set_control_selection(self, selection):
        self.control.selection = selection

    def _observe_control_selection(self, remove=False):
        pass

    def _create_control(self, parent):
        return FakeControl()


class TestMDataViewWidgetWithFakeDataModel(unittest.TestCase):
    """ Test MDataViewWidget with a fake data model and without a real
    GUI toolkit.
    """

    def setUp(self):
        push_exception_handler(reraise_exceptions=True)
        self.addCleanup(pop_exception_handler)

        self.data_model = FakeDataModel(
            fake_get_column_count=lambda: 1,
            fake_get_row_count=lambda row: 1,
            fake_can_have_children=lambda row: True,
            fake_get_value=lambda row, column: None,
            fake_get_value_type=lambda row, column: TextValue(),
        )
        self.widget = FakeWidget(
            parent=None,
            data_model=self.data_model,
        )

    def test_lifecycle(self):
        self.widget._create()
        self.widget.destroy()

    def test_init_state(self):
        self.widget.header_visible = False
        self.widget.selection_mode = "single"
        self.widget.selection_type = "row"
        self.widget.data_model.fake_can_have_children = lambda row: True
        self.widget.data_model.fake_get_row_count = lambda row: 2
        self.widget.selection = [((1, ), ())]

        self.assertIsNone(self.widget.control)

        self.widget._create()

        self.assertEqual(self.widget.control.header_visible, False)
        self.assertEqual(self.widget.control.selection_mode, "single")
        self.assertEqual(self.widget.control.selection_type, "row")
        self.assertEqual(self.widget.control.selection, [((1, ), ())])

    def test_selection_mode_single(self):
        self.widget.data_model.fake_can_have_children = lambda row: True
        self.widget.data_model.fake_get_row_count = lambda row: 5
        self.widget.selection_mode = "single"

        # this should not fail.
        self.widget.selection = [((1, 4), ())]

    def test_selection_mode_single_row_invalid(self):
        self.widget.data_model.fake_can_have_children = lambda row: True
        self.widget.data_model.fake_get_row_count = lambda row: 1

        self.widget.selection_mode = "single"
        self.widget.selection_type = "row"

        row = (1, 4)
        column = ()
        self.assertTrue(self.widget.data_model.is_column_valid(column))
        # this is why the selection is not accepted
        self.assertFalse(self.widget.data_model.is_row_valid(row))

        with self.assertRaises(TraitError):
            self.widget.selection = [(row, column)]

        with self.assertRaises(TraitError):
            self.widget.selection.append((row, column))

    def test_selection_mode_single_column_type_row_invalid(self):
        self.widget.data_model.fake_can_have_children = lambda row: True
        self.widget.data_model.fake_get_row_count = lambda row: 0

        self.widget.selection_mode = "single"
        self.widget.selection_type = "column"

        row = ()
        column = (0, )
        self.assertTrue(self.widget.data_model.is_row_valid(row))
        self.assertTrue(self.widget.data_model.is_column_valid(column))
        self.assertTrue(self.widget.data_model.can_have_children(row))
        # this is why the index is not accepted
        self.assertEqual(self.widget.data_model.get_row_count(row), 0)

        with self.assertRaises(TraitError):
            self.widget.selection = [(row, column)]

        with self.assertRaises(TraitError):
            self.widget.selection.append((row, column))

    def test_selection_mode_single_column_type_row_invalid_no_children(self):
        self.widget.data_model.fake_can_have_children = lambda row: False
        self.widget.data_model.fake_get_row_count = lambda row: 10

        self.widget.selection_mode = "single"
        self.widget.selection_type = "column"

        row = ()
        column = (0, )
        self.assertTrue(self.widget.data_model.is_row_valid(row))
        self.assertTrue(self.widget.data_model.is_column_valid(column))
        self.assertGreater(self.widget.data_model.get_row_count(row), 0)
        # this is why the selection is not accepted
        self.assertFalse(self.widget.data_model.can_have_children(row))

        with self.assertRaises(TraitError):
            self.widget.selection = [(row, column)]

        with self.assertRaises(TraitError):
            self.widget.selection.append((row, column))

    def test_selection_mode_single_row_type_column_invalid(self):
        self.widget.selection_mode = "single"
        self.widget.selection_type = "row"

        row = (0, )
        column = (0, )  # bad because selection type is row
        self.assertTrue(self.widget.data_model.is_row_valid(row))
        self.assertTrue(self.widget.data_model.is_column_valid(column))

        with self.assertRaises(TraitError):
            self.widget.selection = [(row, column)]

        with self.assertRaises(TraitError):
            self.widget.selection.append((row, column))

    def test_selection_mode_single_column_invalid(self):
        self.widget.selection_mode = "single"
        self.widget.selection_type = "column"

        row = (0, )
        column = (1, )  # bad because it is invalid
        self.assertTrue(self.widget.data_model.is_row_valid(row))
        self.assertFalse(self.widget.data_model.is_column_valid(column))

        with self.assertRaises(TraitError):
            self.widget.selection = [(row, column)]

        with self.assertRaises(TraitError):
            self.widget.selection.append((row, column))

    def test_selection_mode_single_max_length_validation(self):
        self.widget.data_model.fake_get_row_count = lambda row: 10
        self.widget.selection_type = "row"
        self.widget.selection_mode = "single"
        # this is okay
        self.widget.selection = []
        # this is okay
        self.widget.selection = [((0, ), ())]
        # this is okay too
        self.widget.selection = [((1, ), ())]
        # this is not okay
        with self.assertRaises(TraitError):
            self.widget.selection = [((0, ), ()), ((1, ), ())]

    def test_selection_mode_none_max_length_validation(self):
        self.widget.selection_type = "row"
        self.widget.selection_mode = "none"
        # this is okay
        self.widget.selection = []
        # this is not okay
        with self.assertRaises(TraitError):
            self.widget.selection = [((0, ), ())]


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
        self.widget.selection_type = "item"
        self.widget.selection = [((1, 4), (2,)), ((2, 0), (4,))]

        self.widget.selection_mode = "single"

        self.assertEqual(self.widget._get_control_selection_mode(), "single")
        self.assertEqual(self.widget.selection, [])

        self.widget.selection = [((1, 4), (2,))]
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
        self.widget.selection = [((1, 4), ())]

        self.widget.selection_type = "column"

        self.assertEqual(self.widget._get_control_selection_type(), "column")
        self.assertEqual(self.widget.selection, [])

        self.widget.selection = [((1, ), (0, ))]
        self.widget.selection_type = "item"

        self.assertEqual(self.widget._get_control_selection_type(), "item")
        self.assertEqual(self.widget.selection, [])

        self.widget.selection = [((1, 4), (2, ))]
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

    @unittest.skipIf(is_wx, "Selection mode 'none' not supported")
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
        self.assertEqual(self.widget._get_control_selection(),  [((1, 4), ())])

    def test_selection_mode_single_invalid(self):
        self.widget.selection_mode = "single"
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 4), ()), (2, 1), ()]

    @unittest.skipIf(is_wx, "Selection mode 'extended' not supported in Wx and Linux")
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

    def test_selection_mode_change_when_selection_change(self):
        modes = cycle(["extended", "single"])

        self.widget.selection_mode = next(modes)
        self._create_widget_control()
        self.assertEqual(self.widget._get_control_selection_mode(), "extended")

        def change_selection_type(event):
            self.widget.selection_mode = next(modes)

        self.widget.observe(
            change_selection_type, "selection.items", dispatch="ui")
        self.addCleanup(
            self.widget.observe,
            change_selection_type, "selection.items", dispatch="ui",
            remove=True,
        )

        # switch from "extended" to "single"
        self.widget.selection = [((0,), ()), ((1,), ())]
        self.gui.process_events()
        self.assertEqual(self.widget._get_control_selection_mode(), "single")
        self.assertEqual(self.widget.selection, [])
        # switch from "single" to "extended"
        self.widget.selection = [((1,), ())]
        self.gui.process_events()
        self.assertEqual(self.widget._get_control_selection_mode(), "extended")
        # switch from "extended" to "single" again
        self.widget.selection.extend([((0,), ()), ((1,), ())])
        self.gui.process_events()
        self.assertEqual(self.widget._get_control_selection_mode(), "single")
        self.assertEqual(self.widget._get_control_selection(), [])
        self.assertEqual(self.widget.selection, [])

    @unittest.skipIf(is_wx, "Selection type 'column' not supported")
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

    @unittest.skipIf(is_wx, "Selection type 'item' not supported")
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

    def test_selection_type_change_when_selection_change(self):
        types = cycle(["column", "row"])

        self.widget.selection_type = next(types)
        self._create_widget_control()
        self.assertEqual(self.widget._get_control_selection_type(), "column")

        def change_selection_type(event):
            self.widget.selection_type = next(types)

        self.widget.observe(
            change_selection_type, "selection.items", dispatch="ui")
        self.addCleanup(
            self.widget.observe,
            change_selection_type, "selection.items", dispatch="ui",
            remove=True,
        )

        # Switch from "column" to "row"
        self.widget.selection = [((0,), (2,)), ((1,), (4,))]
        self.gui.process_events()
        self.assertEqual(self.widget.selection, [])
        self.assertEqual(self.widget._get_control_selection_type(), "row")
        self.assertEqual(self.widget._get_control_selection(), [])
        # Switch from "row" to "column"
        self.widget.selection = [((1,), ()), ((2,), ())]
        self.gui.process_events()
        self.assertEqual(self.widget.selection, [])
        self.assertEqual(self.widget._get_control_selection_type(), "column")
        self.assertEqual(self.widget._get_control_selection(), [])
        # Switch from "column" to "row" again
        self.widget.selection = [((0,), (2,)), ((1,), (4,))]
        self.gui.process_events()
        self.assertEqual(self.widget.selection, [])
        self.assertEqual(self.widget._get_control_selection_type(), "row")
        self.assertEqual(self.widget._get_control_selection(), [])

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

    def test_selection_type_row_invalid_column_append(self):
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection.append(((1, 2), (2,)))

        self.assertEqual(self.widget.selection, [])

    @unittest.skipIf(is_wx, "Selection mode 'item' not supported")
    def test_selection_type_item_invalid_row_too_big(self):
        self.widget.selection_type = 'item'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 10), (2,))]

    @unittest.skipIf(is_wx, "Selection mode 'item' not supported")
    def test_selection_type_item_invalid_row_too_long(self):
        self.widget.selection_type = 'item'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 4, 5, 6), (2,))]

    @unittest.skipIf(is_wx, "Selection mode 'item' not supported")
    def test_selection_type_item_invalid_column(self):
        self.widget.selection_type = 'item'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 2), (10,))]

    @unittest.skipIf(is_wx, "Selection mode 'item' not supported")
    def test_selection_type_column_invalid_row_too_long(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 4, 5, 6), (2,))]

    @unittest.skipIf(is_wx, "Selection mode 'column' not supported")
    def test_selection_type_column_invalid_row_too_big(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((10,), (2,))]

    @unittest.skipIf(is_wx, "Selection mode 'column' not supported")
    def test_selection_type_column_invalid_row_not_parent(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((1, 2), (2,))]

    @unittest.skipIf(is_wx, "Selection mode 'column' not supported")
    def test_selection_type_column_invalid_column(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection = [((), (10,))]

    @unittest.skipIf(is_wx, "Selection mode 'column' not supported")
    def test_selection_type_column_invalid_column_with_append(self):
        self.widget.selection_type = 'column'
        self._create_widget_control()

        with self.assertRaises(TraitError):
            self.widget.selection.append(((), (10,)))

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
