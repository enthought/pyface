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

API for the ``pyface.data_view`` subpackage.
Note that this public-facing API is provisional and may change in future
minor releases until Pyface 8.

- :class:`~.AbstractDataExporter`
- :class:`~.AbstractDataModel`
- :class:`~.AbstractValueType`
- :class:`~.DataViewWidget`
- :class:`~.DataWrapper`

Data Formats
------------

- :class:`~.DataFormat`
- :func:`~.text_format`
- :attr:`~.csv_format`
- :attr:`~.csv_column_format`
- :attr:`~.csv_row_format`
- :attr:`~.html_format`
- :attr:`~.npy_format`
- :attr:`~.standard_text_format`
- :attr:`~.table_format`
- :attr:`~.text_column_format`
- :attr:`~.text_row_format`
- :func:`~.from_csv`
- :func:`~.from_csv_column`
- :func:`~.from_csv_row`
- :func:`~.from_json`
- :func:`~.from_npy`
- :func:`~.to_csv`
- :func:`~.to_csv_column`
- :func:`~.to_csv_row`
- :func:`~.to_json`
- :func:`~.to_npy`

Index Managers
--------------

- :class:`~.AbstractIndexManager`
- :class:`~.IntIndexManager`
- :class:`~.TupleIndexManager`

Exceptions
----------
- :class:`~.DataViewError`
- :class:`~.DataViewGetError`
- :class:`~.DataViewSetError`

Interfaces
----------
- :class:`~.IDataViewWidget`
- :class:`~.IDataWrapper`

"""

from pyface.data_view.abstract_data_exporter import AbstractDataExporter
from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.abstract_value_type import AbstractValueType
from pyface.data_view.data_formats import (
    csv_column_format, csv_format, csv_row_format, from_csv, from_csv_column,
    from_csv_row, from_json, from_npy, html_format, npy_format,
    standard_text_format, to_csv, to_csv_column, to_csv_row, to_json, to_npy,
    table_format, text_column_format, text_row_format
)
from pyface.data_view.data_view_errors import (
    DataViewError, DataViewGetError, DataViewSetError
)
from pyface.data_view.i_data_view_widget import IDataViewWidget
from pyface.data_view.i_data_wrapper import (
    DataFormat, IDataWrapper, text_format
)
from pyface.data_view.index_manager import (
    AbstractIndexManager, IntIndexManager, TupleIndexManager
)


# ----------------------------------------------------------------------------
# Deferred imports
# ----------------------------------------------------------------------------

# These imports have the side-effect of performing toolkit selection

_toolkit_imports = {
    'DataViewWidget': 'data_view_widget',
    'DataWrapper': 'data_wrapper',
}


def __getattr__(name):
    """Lazily load attributes with side-effects

    In particular, lazily load toolkit backend names.  For efficiency, lazily
    loaded objects are injected into the module namespace
    """
    # sentinel object for no result
    not_found = object()
    result = not_found

    if name in _toolkit_imports:
        from pyface.toolkit import toolkit_object
        source = _toolkit_imports[name]
        result = toolkit_object(f"data_view.{source}:{name}")

    if result is not_found:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    globals()[name] = result
    return result


# ----------------------------------------------------------------------------
# Introspection support
# ----------------------------------------------------------------------------

def __dir__():
    return sorted(set(globals()) | set(_toolkit_imports))
