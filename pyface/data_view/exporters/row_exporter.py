# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Bool

from pyface.data_view.abstract_data_exporter import AbstractDataExporter


class RowExporter(AbstractDataExporter):
    """ Export a collection of rows from a data view as a list of lists.

    This is suitable for drag and drop or copying of the content of multiple
    selected rows.

    This exports a list of data associated with each row in the
    indices.  Each row item is itself a list of values extracted
    from the model.

    If the format mimetype is a text mimetype, it will use the
    ``get_text()`` method to extract the values, otherwise it will
    try to use the editor value if it exists, and failing that
    the raw value returned from the model.
    """

    #: Whether or not to include row headers.
    row_headers = Bool()

    #: Whether or not to include column headers.
    column_headers = Bool()

    def get_data(self, model, indices):
        """ Get the data to be exported from the model and indices.

        This exports a list of data associated with each row in the
        indices.  Each row item is itself a list of values extracted
        from the model.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        indices : list of (row, column) index pairs
            The indices where the data is to be stored.

        Returns
        -------
        data : Any
            The data, of a type that can be serialized by the format.
        """
        rows = sorted({row for row, column in indices})
        n_columns = model.get_column_count()
        columns = [(column,) for column in range(n_columns)]

        if self.column_headers:
            rows = [()] + rows
        if self.row_headers:
            columns = [()] + columns

        return [
            [self.get_value(model, row, column,) for column in columns]
            for row in rows
        ]
