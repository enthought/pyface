# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.data_view.abstract_data_exporter import AbstractDataExporter
from pyface.data_view.data_view_errors import DataViewGetError


class ItemExporter(AbstractDataExporter):
    """ Export a single item from a data view.

    This is suitable for drag and drop or copying of the content of a single
    item in a data view.  If passed an multiple items it will fail by
    raising ``DataViewGetError``; drag and drop support will then ignore this
    as an exporter to use.
    """

    def add_data(self, data_wrapper, model, indices):
        """ Add data to the data wrapper from the model and indices.

        Parameters
        ----------
        data_wrapper : DataWrapper
            The data wrapper that will be used to export data.
        model : AbstractDataModel
            The data model holding the data.
        indices : list of (row, column) index pairs
            The indices where the data is to be stored.
        """
        # only export single item values
        if len(indices) == 1:
            super().add_data(data_wrapper, model, indices)

    def get_data(self, model, indices):
        """ Get the data to be exported from the model and indices.

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
        if len(indices) != 1:
            raise DataViewGetError("ItemExporter can only export single values")
        row, column = indices[0]
        return self.get_value(model, row, column)
