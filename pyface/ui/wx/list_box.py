# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A simple list box widget with a model-view architecture. """

import warnings

import wx

from traits.api import Event, Instance, Int

from pyface.list_box_model import ListBoxModel
from .layout_widget import LayoutWidget


class ListBox(LayoutWidget):
    """ A simple list box widget with a model-view architecture. """

    # The model that provides the data for the list box.
    model = Instance(ListBoxModel)

    # The objects currently selected in the list.
    selection = Int(-1)

    # Events.

    # An item has been activated.
    item_activated = Event()

    # Default style.
    STYLE = wx.LB_SINGLE | wx.LB_HSCROLL | wx.LB_NEEDED_SB

    def __init__(self, parent=None, **traits):
        """ Creates a new list box. """

        create = traits.pop('create', True)

        # Base-class constructors.
        super().__init__(parent=parent, **traits)

        # Create the widget!
        if create:
            self.create()
            warnings.warn(
                "automatic widget creation is deprecated and will be removed "
                "in a future Pyface version, code should not pass the create "
                "parameter and should instead call create() explicitly",
                DeprecationWarning,
                stacklevel=2,
            )

    def create(self, parent=None):
        super().create(parent=parent)

        self._populate()

        # Listen for changes to the model.
        self.model.observe(self._on_model_changed, "list_changed")

    def dispose(self):
        self.model.observe(
            self._on_model_changed, "list_changed", remove=True
        )
        self.model.dispose()

    # ------------------------------------------------------------------------
    # 'ListBox' interface.
    # ------------------------------------------------------------------------

    def refresh(self):
        """ Refreshes the list box. """

        # For now we just clear out the entire list.
        self.control.Clear()

        # Populate the list.
        self._populate()

    # ------------------------------------------------------------------------
    # wx event handlers.
    # ------------------------------------------------------------------------

    def _on_item_selected(self, event):
        """ Called when an item in the list is selected. """

        listbox = event.GetEventObject()

        self.selection = listbox.GetSelection()

    def _on_item_activated(self, event):
        """ Called when an item in the list is activated. """

        listbox = event.GetEventObject()
        index = listbox.GetSelection()

        # Trait event notification.
        self.item_activated = index

    # ------------------------------------------------------------------------
    # Trait handlers.
    # ------------------------------------------------------------------------

    # Static ---------------------------------------------------------------

    def _selection_changed(self, index):
        """ Called when the selected item is changed. """

        if index != -1:
            self.control.SetSelection(index)

    # Dynamic -------------------------------------------------------------#

    def _on_model_changed(self, event):
        """ Called when the model has changed. """

        # For now we just clear out the entire list.
        self.refresh()

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Creates the widget. """

        control = wx.ListBox(parent, -1, style=self.STYLE)

        # Wire it up!
        control.Bind(
            wx.EVT_LISTBOX, self._on_item_selected, id=self.control.GetId()
        )
        control.Bind(
            wx.EVT_LISTBOX_DCLICK,
            self._on_item_activated,
            id=self.control.GetId(),
        )

        # Populate the list.
        return control

    def _populate(self):
        """ Populates the list box. """

        for index in range(self.model.get_item_count()):
            label, item = self.model.get_item_at(index)
            self.control.Append(label, item)
