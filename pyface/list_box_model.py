""" The model for list boxes. """

# Enthought library imports
from traits.api import Event, HasTraits


# Classes for event traits.
class ListModelEvent(object):
    """ Information about list model changes. """


class ListBoxModel(HasTraits):
    """ The model for list boxes. """

    #### Events ####

    #: Fired when the contents of the list have changed.
    list_changed = Event

    def get_item_count(self):
        """ Returns the number of items in the list. """
        raise NotImplementedError

    def get_item_at(self, index):
        """ Returns the item at the specified index.

        Parameters
        ----------
        index : int
            The index to return the value of.
        """
        raise NotImplementedError

    def fire_list_changed(self):
        """ Invoke this method when the list has changed. """
        self.list_changed = ListModelEvent()
