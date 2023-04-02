# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The model for list boxes. """


from traits.api import Event, HasTraits


# Classes for event traits.
class ListModelEvent(object):
    """ Information about list model changes. """


class ListBoxModel(HasTraits):
    """ The model for list boxes. """

    # Events ----

    #: Fired when the contents of the list have changed.
    list_changed = Event()

    def get_item_count(self):
        """ Get the number of items in the list.

        Returns
        -------
        item_count : int
            The number of items in the list.
        """
        raise NotImplementedError()

    def get_item_at(self, index):
        """ Returns the item at the specified index.

        Parameters
        ----------
        index : int
            The index to return the value of.

        Returns
        -------
        label, item : str, any
            The user-visible string and model data of the item.
        """
        raise NotImplementedError()

    def fire_list_changed(self):
        """ Invoke this method when the list has changed. """
        self.list_changed = ListModelEvent()
