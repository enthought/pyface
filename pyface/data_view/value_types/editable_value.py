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

from pyface.data_view.data_view_errors import DataViewSetError
from pyface.data_view.abstract_value_type import AbstractValueType


class EditableValue(AbstractValueType):
    """ A base class for editable values.

    This class provides two things beyond the base AbstractValueType:
    a trait ``is_editable`` which allows toggling editing state on and
    off, and an ``is_valid`` method that is used for validation before
    setting a value.
    """

    #: Whether or not the value is editable, assuming the underlying data can
    #: be set.
    is_editable = Bool(True, update_value_type=True)

    def is_valid(self, model, row, column, value):
        """ Whether or not the value is valid for the data item specified.

        The default implementation returns True for all values.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.
        value : Any
            The value to validate.

        Returns
        -------
        is_valid : bool
            Whether or not the value is valid.
        """
        return True

    # AbstractValueType Interface --------------------------------------------

    def has_editor_value(self, model, row, column):
        """ Return whether or not the value can be edited.

        A cell is editable if the underlying data can be set, and the
        ``is_editable`` flag is set to True

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.

        Returns
        -------
        has_editor_value : bool
            Whether or not the value is editable.
        """
        return model.can_set_value(row, column) and self.is_editable

    def set_editor_value(self, model, row, column, value):
        """ Set the edited value.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being set.
        column : sequence of int
            The column in the data model being set.
        value : Any
            The value being set.

        Raises
        -------
        DataViewSetError
            If the value cannot be set.
        """
        if self.is_valid(model, row, column, value):
            model.set_value(row, column, value)
        else:
            raise DataViewSetError("Invalid value set: {!r}".format(value))
