# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
import unittest

try:
    from pyface.ui.wx.grid.api import GridRow, GridColumn, SimpleGridModel
except ImportError:
    wx_available = False
else:
    wx_available = True


@unittest.skipUnless(wx_available, "Wx is not available")
class CompositeGridModelTestCase(unittest.TestCase):
    def setUp(self):

        self.model = SimpleGridModel(
            data=[[None, 2], [3, 4]],
            rows=[GridRow(label="foo"), GridRow(label="bar")],
            columns=[GridColumn(label="cfoo"), GridColumn(label="cbar")],
        )

    def test_get_column_count(self):

        self.assertEqual(self.model.get_column_count(), 2)

    def test_get_row_count(self):

        self.assertEqual(self.model.get_row_count(), 2)

    def test_get_row_name(self):

        # Regardless of the rows specified in the composed models, the
        # composite model returns its own rows.
        self.assertEqual(self.model.get_row_name(0), "foo")
        self.assertEqual(self.model.get_row_name(1), "bar")

    def test_get_column_name(self):

        self.assertEqual(self.model.get_column_name(0), "cfoo")
        self.assertEqual(self.model.get_column_name(1), "cbar")

    def test_get_value(self):

        self.assertEqual(self.model.get_value(0, 0), None)
        self.assertEqual(self.model.get_value(0, 1), 2)
        self.assertEqual(self.model.get_value(1, 0), 3)
        self.assertEqual(self.model.get_value(1, 1), 4)

    def test_is_cell_empty(self):

        rows = self.model.get_row_count()
        columns = self.model.get_column_count()

        self.assertEqual(
            self.model.is_cell_empty(0, 0),
            True,
            "Cell containing None should be empty.",
        )
        self.assertEqual(
            self.model.is_cell_empty(rows+1, columns+1),
            True,
            "Cell outside the range of values should be empty.",
        )

        return
