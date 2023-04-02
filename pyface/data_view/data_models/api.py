# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""

API for the ``pyface.data_view.data_models`` subpackage.

Data Accessors
--------------

- :class:`~.AbstractDataAccessor`
- :class:`~.AttributeDataAccessor`
- :class:`~.ConstantDataAccessor`
- :class:`~.IndexDataAccessor`
- :class:`~.KeyDataAccessor`

Data Models
-----------

- :class:`~.RowTableDataModel`
- :class:`~.ArrayDataModel`. Note that this data model is only available if
  ``numpy`` is available in the environment.

"""
try:
    import numpy  # noqa: F401
except ImportError:
    pass
else:
    del numpy
    from .array_data_model import ArrayDataModel  # noqa: F401

from .data_accessors import (  # noqa: F401
    AbstractDataAccessor, AttributeDataAccessor, ConstantDataAccessor,
    IndexDataAccessor, KeyDataAccessor
)
from .row_table_data_model import RowTableDataModel  # noqa: F401
