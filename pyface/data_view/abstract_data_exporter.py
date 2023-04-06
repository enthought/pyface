# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Bool, Instance

from pyface.data_view.data_view_errors import DataViewGetError
from pyface.data_view.i_data_wrapper import DataFormat


class AbstractDataExporter(ABCHasStrictTraits):
    """ ABC for classes that export data from a data view.

    Concrete classes should implement the ``get_data`` method so that
    it produces a value that can be serialized using the provided
    ``format``.  Some convenience methods are provided to get
    text values, as that is a common use-case.
    """

    #: The DataFormat used to serialize the exported data.
    format = Instance(DataFormat)

    #: Whether to get item data from the text channel, if available.
    is_text = Bool()

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
        try:
            data = self.get_data(model, indices)
            data_wrapper.set_format(self.format, data)
        except DataViewGetError:
            pass

    @abstractmethod
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
        raise NotImplementedError()

    def get_value(self, model, row, column):
        """ Utility method to extract a value at a given index.

        If ``is_text`` is True, it will use the ``get_text()`` method
        to extract the value, otherwise it will try to use the
        editor value if it exists, and failing that the raw value
        returned from the model.
        """
        value_type = model.get_value_type(row, column)
        if self.is_text:
            if value_type.has_text(model, row, column):
                value = value_type.get_text(model, row, column)
            else:
                value = ""
        elif value_type.has_editor_value(model, row, column):
            value = value_type.get_editor_value(model, row, column)
        else:
            value = model.get_value(row, column)
        return value

    def _is_text_default(self):
        return self.format.mimetype.startswith('text/')
