# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Classes for extracting data from objects

This module provides helper classes for the row table data model and
related classes for extracting data from an object in a consistent way.
"""

from abc import abstractmethod
from collections.abc import Hashable, MutableMapping, MutableSequence

from traits.api import (
    ABCHasStrictTraits, Any, Event, Instance, Int, Str, observe
)
from traits.trait_base import xgetattr, xsetattr

from pyface.data_view.abstract_data_model import DataViewSetError
from pyface.data_view.abstract_value_type import AbstractValueType
from pyface.data_view.value_types.api import TextValue


class AbstractDataAccessor(ABCHasStrictTraits):
    """ Accessor that gets and sets data on an object.
    """

    #: A human-readable label for the accessor.
    title = Str()

    #: The value type of the title of this accessor, suitable for use in a
    #: header.
    title_type = Instance(AbstractValueType, factory=TextValue)

    #: The value type of the data accessed.
    value_type = Instance(AbstractValueType)

    #: An event fired when accessor is updated update.  The payload is
    #: a tuple of the accessor info and whether the title or value changed
    #: (or both).
    updated = Event

    @abstractmethod
    def get_value(self, obj):
        """ Return a value for the provided object.

        Parameters
        ----------
        obj : Any
            The object that contains the data.

        Returns
        -------
        value : Any
            The data value contained in the object.
        """
        raise NotImplementedError()

    def can_set_value(self, obj):
        """ Return whether the value can be set on the provided object.

        Parameters
        ----------
        obj : Any
            The object that contains the data.

        Returns
        -------
        can_set_value : bool
            Whether or not the value can be set.
        """
        return False

    def set_value(self, obj, value):
        """ Set the value on the provided object.

        Parameters
        ----------
        obj : Any
            The object that contains the data.
        value : Any
            The data value to set.

        Raises
        -------
        DataViewSetError
            If setting the value fails.
        """
        raise DataViewSetError(
            "Cannot set {!r} column of {!r}.".format(self.title, obj)
        )

    # trait observers

    @observe('title,title_type.updated')
    def _title_updated(self, event):
        self.updated = (self, 'title')

    @observe('value_type.updated')
    def _value_type_updated(self, event):
        self.updated = (self, 'value')


class ConstantDataAccessor(AbstractDataAccessor):
    """ DataAccessor that returns a constant value.
    """

    #: The value to return.
    value = Any()

    def get_value(self, obj):
        """ Return the value ignoring the provided object.

        Parameters
        ----------
        obj : Any
            An object.

        Returns
        -------
        value : Any
            The data value contained in this class' value trait.
        """
        return self.value

    @observe('value')
    def _value_updated(self, event):
        self.updated = (self, 'value')


class AttributeDataAccessor(AbstractDataAccessor):
    """ DataAccessor that presents an extended attribute on an object.

    This is suitable for use with Python objects, including HasTraits
    classes.
    """

    #: The extended attribute name of the trait holding the value.
    attr = Str()

    def get_value(self, obj):
        """ Return the attribute value for the provided object.

        Parameters
        ----------
        obj : Any
            The object that contains the data.

        Returns
        -------
        value : Any
            The data value contained in the object's attribute.
        """
        return xgetattr(obj, self.attr)

    def can_set_value(self, obj):
        """ Return whether the value can be set on the provided object.

        Parameters
        ----------
        obj : Any
            The object that contains the data.

        Returns
        -------
        can_set_value : bool
            Whether or not the value can be set.
        """
        return bool(self.attr)

    def set_value(self, obj, value):
        if not self.can_set_value(obj):
            raise DataViewSetError(
                "Attribute is not specified for {!r}".format(self)
            )
        xsetattr(obj, self.attr, value)

    @observe('attr')
    def _attr_updated(self, event):
        self.updated = (self, 'value')

    def _title_default(self):
        # create human-friendly version of extended attribute
        attr = self.attr.split('.')[-1]
        title = attr.replace('_', ' ').title()
        return title


class IndexDataAccessor(AbstractDataAccessor):
    """ DataAccessor that presents an index on a sequence object.

    This is suitable for use with a sequence.
    """

    #: The index in a sequence which holds the value.
    index = Int()

    def get_value(self, obj):
        """ Return the indexed value for the provided object.

        Parameters
        ----------
        obj : sequence
            The object that contains the data.

        Returns
        -------
        value : Any
            The data value contained in the object at the index.
        """
        return obj[self.index]

    def can_set_value(self, obj):
        """ Return whether the value can be set on the provided object.

        Parameters
        ----------
        obj : Any
            The object that contains the data.

        Returns
        -------
        can_set_value : bool
            Whether or not the value can be set.
        """
        return isinstance(obj, MutableSequence) and 0 <= self.index < len(obj)

    def set_value(self, obj, value):
        """ Set the value on the provided object.

        Parameters
        ----------
        obj : Any
            The object that contains the data.
        value : Any
            The data value to set.

        Raises
        -------
        DataViewSetError
            If setting the value fails.
        """
        if not self.can_set_value(obj):
            raise DataViewSetError(
                "Cannot set {!r} index of {!r}.".format(self.index, obj)
            )
        obj[self.index] = value

    @observe('index')
    def _index_updated(self, event):
        self.updated = (self, 'value')

    def _title_default(self):
        title = str(self.index)
        return title


class KeyDataAccessor(AbstractDataAccessor):
    """ DataAccessor that presents an item on a mapping object.

    This is suitable for use with a mapping, such as a dictionary.
    """

    #: The key in the mapping holding the value.
    key = Instance(Hashable)

    def get_value(self, obj):
        """ Return the key's value for the provided object.

        Parameters
        ----------
        obj : mapping
            The object that contains the data.

        Returns
        -------
        value : Any
            The data value contained in the given key of the object.
        """
        return obj[self.key]

    def can_set_value(self, obj):
        """ Set the value on the provided object.

        Parameters
        ----------
        obj : mapping
            The object that contains the data.
        value : Any
            The data value to set.

        Raises
        -------
        DataViewSetError
            If setting the value fails.
        """
        return isinstance(obj, MutableMapping)

    def set_value(self, obj, value):
        """ Set the value on the provided object.

        Parameters
        ----------
        obj : Any
            The object that contains the data.
        value : Any
            The data value to set.

        Raises
        -------
        DataViewSetError
            If setting the value fails.
        """
        if not self.can_set_value(obj):
            raise DataViewSetError(
                "Cannot set {!r} key of {!r}.".format(self.key, obj)
            )
        obj[self.key] = value

    @observe('key')
    def _key_updated(self, event):
        self.updated = (self, 'value')

    def _title_default(self):
        title = str(self.key).title()
        return title
