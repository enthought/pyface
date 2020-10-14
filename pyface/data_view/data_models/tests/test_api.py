# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
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
    def test_all_imports_exclude_numpy_dependencies(self):
        # These objects do not depend on NumPy
        from pyface.data_view.data_models.api import (  # noqa: F401
            AbstractDataAccessor,
            AttributeDataAccessor,
            ConstantDataAccessor,
            IndexDataAccessor,
            KeyDataAccessor,
            RowTableDataModel,
        )

    def test_import_with_numpy_dependency(self):
        # These objects that require NumPy.
        try:
            import numpy  # noqa: F401
        except ImportError:
            self.skipTest("NumPy not available.")

        from pyface.data_view.data_models.api import (  # noqa: F401
            ArrayDataModel,
        )
