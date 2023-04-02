# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Test the api module. """

import unittest


class TestApi(unittest.TestCase):
    def test_all_imports(self):
        from pyface.data_view.api import (  # noqa: F401
            AbstractDataExporter,
            AbstractDataModel,
            AbstractValueType,
            csv_column_format,
            csv_format,
            csv_row_format,
            from_csv,
            from_csv_column,
            from_csv_row,
            from_json,
            from_npy,
            html_format,
            npy_format,
            standard_text_format,
            to_csv,
            to_csv_column,
            to_csv_row,
            to_json,
            to_npy,
            table_format,
            text_column_format,
            text_format,
            text_row_format,
            DataViewError,
            DataViewGetError,
            DataViewSetError,
            DataViewWidget,
            DataWrapper,
            IDataViewWidget,
            IDataWrapper,
            AbstractIndexManager,
            IntIndexManager,
            TupleIndexManager,
            DataFormat,
        )

    def test_api_items_count(self):
        # This test helps developer to keep the above list
        # up-to-date. Bump the number when the API content changes.
        from pyface.data_view import api
        items_in_api = {
            name
            for name in dir(api)
            if not name.startswith("_")
        }
        self.assertEqual(len(items_in_api), 34)
