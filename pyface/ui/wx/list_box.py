""" A simple list box widget with a model-view architecture. """
from __future__ import absolute_import

# Major package imports.
import wx

# Enthought library imports.
from traits.api import Event, Instance, Int

# Local imports.
from pyface.list_box_model import ListBoxModel
from .widget import Widget


class ListBox(Widget):
    """ A simple list box widget with a model-view architecture. """

    # The model that provides the data for the list box.
    model = Instance(ListBoxModel)

    # The objects currently selected in the list.
    selection = Int(-1)

    # Events.

    # An item has been activated.
    item_activated = Event

    # Default style.
    STYLE = wx.LB_SINGLE | wx.LB_HSCROLL | wx.LB_NEEDED_SB


    def __init__(self, parent, **traits):
        """ Creates a new list box. """

        # Base-class constructors.
        super(ListBox, self).__init__(**traits)

        # Create the widget!
        self._create_control(parent)

        # Listen for changes to the model.
        self.model.on_trait_change(self._on_model_changed, "list_changed")

        return

    def dispose(self):
        self.model.on_trait_change(self._on_model_changed, "list_changed",
                                   remove = True)
        self.model.dispose()
        return

    ###########################################################################
    # 'ListBox' interface.
    ###########################################################################

    def refresh(self):
        """ Refreshes the list box. """

        # For now we just clear out the entire list.
        self.control.Clear()

        # Populate the list.
        self._populate()

        return

    ###########################################################################
    # wx event handlers.
    ###########################################################################

    def _on_item_selected(self, event):
        """ Called when an item in the list is selected. """

        listbox = event.GetEventObject()

        self.selection = listbox.GetSelection()

        return

    def _on_item_activated(self, event):
        """ Called when an item in the list is activated. """

        listbox = event.GetEventObject()
        index = listbox.GetSelection()

        # Trait event notification.
        self.item_activated = index

        return

    ###########################################################################
    # Trait handlers.
    ###########################################################################

    #### Static ###############################################################

    def _selection_changed(self, index):
        """ Called when the selected item is changed. """

        if index != -1:
            self.control.SetSelection(index)

        return

    #### Dynamic ##############################################################

    def _on_model_changed(self, event):
        """ Called when the model has changed. """

        # For now we just clear out the entire list.
        self.refresh()

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_control(self, parent):
        """ Creates the widget. """

        self.control = wx.ListBox(parent, -1, style = self.STYLE)

        # Wire it up!
        wx.EVT_LISTBOX(self.control, self.control.GetId(),
                       self._on_item_selected)
        wx.EVT_LISTBOX_DCLICK(self.control, self.control.GetId(),
                              self._on_item_activated)

        # Populate the list.
        self._populate()

        return

    def _populate(self):
        """ Populates the list box. """

        for index in range(self.model.get_item_count()):
            label, item = self.model.get_item_at(index)
            self.control.Append(label, item)

        return

#### EOF ######################################################################
