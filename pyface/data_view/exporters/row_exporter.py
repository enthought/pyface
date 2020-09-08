from traits.api import Bool

from pyface.data_view.abstract_data_exporter import AbstractDataExporter


class RowExporter(AbstractDataExporter):

    #: Whether or not to include row headers.
    row_headers = Bool()

    #: Whether or not to include column headers.
    column_headers = Bool()

    def get_data(self, model, indices):
        """ Get the data to be exported from the model and indices.

        This exports a list of data associated with each row in the
        indices.  Each row item is itself a list of values extracted
        from the model.

        If the format mimetype is a text mimetype, it will use the
        ``get_text()`` method to extract the value, otherwise it will
        try to use the editor value if it exists, and failing that
        the raw value returned from the model.

        Parameters
        ----------
        model : AbstractDataModel instance
            The data model holding the data.
        indices : list of (row, column) index pairs
            The indices where the data is to be stored.

        Returns
        -------
        data : any
            The data, of a type that can be serialized by the format.
        """
        if self.column_headers:
            indices = [((), ())] + indices
        rows = sorted({row for row, column in indices})

        n_columns = model.get_column_count()
        columns = [(column,) for column in range(n_columns)]
        if self.row_headers:
            columns = [()] + columns

        return [
            [self.get_value(model, row, column,) for column in columns]
            for row in rows
        ]
