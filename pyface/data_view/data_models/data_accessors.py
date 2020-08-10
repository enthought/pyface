# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
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
from collections import Hashable

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
        raise NotImplementedError()

    def can_set_value(self, obj):
        return False

    def set_value(self, obj, value):
        raise DataViewSetError(
            "Cannot set {!r} column of {!r}.".format(self.title, obj)
        )

    # trait observers

    @observe('title,title_type.updated')
    def title_updated(self, event):
        self.updated = (self, 'title')

    @observe('value_type.updated')
    def value_type_updated(self, event):
        self.updated = (self, 'value')


class AttributeDataAccessor(AbstractDataAccessor):
    """ DataAccessor that presents an extended attribute on an object.

    This is suitable for use with Python objects, including HasTraits
    classes.
    """

    #: The extended attribute name of the trait holding the value.
    attr = Str()

    def get_value(self, obj):
        return xgetattr(obj, self.attr, None)

    def can_set_value(self, obj):
        return self.attr != ''

    def set_value(self, obj, value):
        if not self.attr:
            raise DataViewSetError(
                "Attribute is not specified for {!r}".format(self)
            )
        xsetattr(obj, self.attr, value)

    @observe('attr')
    def attr_updated(self, event):
        self.updated = (self, 'value')

    def _title_default(self):
        # create human-friendly version of extended attribute
        attr = self.attr.split('.')[-1]
        title = attr.replace('_', ' ').title()
        return title


class IndexDataAccessor(AbstractDataAccessor):
    """ DataAccessor that presents an index on an object.

    This is suitable for use with a sequence.
    """

    #: The extended trait name of the trait holding the value.
    index = Int()

    def get_value(self, obj):
        try:
            return obj[self.index]
        except IndexError:
            return None

    def can_set_value(self, obj):
        return 0 <= self.index < len(obj)

    def set_value(self, obj, value):
        if not self.can_set_value(obj):
            raise DataViewSetError(
                "Cannot set {!r} index of {!r}.".format(self.index, obj)
            )
        obj[self.index] = value

    @observe('index')
    def index_updated(self, event):
        self.updated = (self, 'value')

    def _title_default(self):
        title = str(self.index)
        return title


class KeyDataAccessor(AbstractDataAccessor):
    """ DataAccessor that presents an item on an object.

    This is suitable for use with a mapping, such as a dictionary.
    """

    #: The extended trait name of the trait holding the value.
    key = Any()

    def get_value(self, obj):
        return obj.get(self.key, None)

    def can_set_value(self, obj):
        return isinstance(self.key, Hashable)

    def set_value(self, obj, value):
        if not self.can_set_value(obj):
            raise DataViewSetError(
                "Cannot set {!r} key of {!r}.".format(self.key, obj)
            )
        obj[self.key] = value

    @observe('key')
    def key_updated(self, event):
        self.updated = (self, 'value')

    def _title_default(self):
        title = str(self.key).title()
        return title
