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
        from pyface.data_view.exporters.api import (  # noqa: F401
            ItemExporter,
            RowExporter,
        )

    def test_api_items_count(self):
        # This test helps developer to keep the above list
        # up-to-date. Bump the number when the API content changes.
        from pyface.data_view.exporters import api
        items_in_api = {
            name
            for name in dir(api)
            if not name.startswith("_")
        }
        self.assertEqual(len(items_in_api), 2)
