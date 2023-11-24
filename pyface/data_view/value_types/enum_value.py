# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Callable, List

from .editable_value import EditableValue


class EnumValue(EditableValue):
    """ Editable value that takes one of a collection of pre-set values.

    Each value can be associated with text, colors and images by supplying
    functions ``format``, ``colors`` and ``images``, respectively.
    """

    #: The list of values which are allowed for the value.
    values = List()

    #: A function that converts a value to a string for display.
    format = Callable(str, update_value_type=True)

    #: A map from valid values to colors.
    colors = Callable(None, update_value_type=True)

    #: A map from valid values to images.
    images = Callable(None, update_value_type=True)

    def is_valid(self, model, row, column, value):
        """ Whether or not the value is valid for the data item specified.

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
        return value in self.values

    def has_text(self, model, row, column):
        """ Get the display text from the underlying value.

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
        text : str
            The text to display.
        """
        return self.format is not None

    def get_text(self, model, row, column):
        """ Get the display text from the underlying value.

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
        text : str
            The text to display.
        """
        return self.format(model.get_value(row, column))

    def has_color(self, model, row, column):
        """ Whether or not the value has color data.

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
        has_color : bool
            Whether or not the value has data-associated color
            values.
        """
        return self.colors is not None

    def get_color(self, model, row, column):
        """ Get data-associated colour values for the given item.

        The default implementation returns white.

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
        color : Color
            The color associated with the cell.
        """
        return self.colors(model.get_value(row, column))

    def has_image(self, model, row, column):
        """ Whether or not the value has an image associated with it.

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
        has_image : bool
            Whether or not the value has an image associated with it.
        """
        return self.images is not None

    def get_image(self, model, row, column):
        """ An image associated with the underlying value.

        The default implementation returns None.

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
        image : IImage
            The image associated with the underlying value.
        """
        return self.images(model.get_value(row, column))
