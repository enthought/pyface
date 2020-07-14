# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from contextlib import contextmanager
import logging

from traits.api import (
    Bool, ComparisonMode, Enum, HasStrictTraits, Instance, List, Tuple,
)

from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.i_widget import IWidget


logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class IDataViewWidget(IWidget):
    """ Interface for data view widgets. """

    #: The data model for the data view.
    data_model = Instance(AbstractDataModel, allow_none=False)

    #: Whether or not the column headers are visible.
    header_visible = Bool(True)

    #: What can be selected.  Some backends may support more.
    selection_type = Enum("row",)

    #: How selections are modified.
    selection_mode = Enum("extended", "single")

    #: The selected indices in the view.
    selection = List(Tuple)


class MDataViewWidget(HasStrictTraits):
    """ Mixin class for data view widgets. """

    # IDataViewWidget Interface traits --------------------------------------

    #: The data model for the data view.
    data_model = Instance(AbstractDataModel, allow_none=False)

    #: Whether or not the column headers are visible.
    header_visible = Bool(True)

    #: What can be selected.
    selection_type = Enum("row")

    #: How selections are modified.
    selection_mode = Enum("extended", "single")

    #: The selected indices in the view.
    selection = List(Tuple, comparison_mode=ComparisonMode.identity)

    # Private traits --------------------------------------------------------

    #: Whether the selection is currently being updated.
    _selection_updating_flag = Bool

    # ------------------------------------------------------------------------
    # IDataViewWidget Interface
    # ------------------------------------------------------------------------

    def _header_visible_updated(self, event):
        """ Observer for header_visible trait. """
        if self.control is not None:
            self._set_control_header_visible(event.new)

    def _get_control_header_visible(self):
        """ Toolkit specific method to get the visibility of the header. """
        raise NotImplementedError()

    def _set_control_header_visible(self, control_header_visible):
        """ Toolkit specific method to set the visibility of the header. """
        raise NotImplementedError()

    def _selection_type_updated(self, event):
        """ Observer for selection_type trait. """
        if self.control is not None:
            self._set_control_selection_type(event.new)

    def _get_control_selection_type(self):
        """ Toolkit specific method to get the selection type. """
        raise NotImplementedError()

    def _set_control_selection_type(self, selection_type):
        """ Toolkit specific method to change the selection type. """
        raise NotImplementedError()

    def _selection_mode_updated(self, event):
        """ Observer for selection_mode trait. """
        if self.control is not None:
            self._set_control_selection_mode(event.new)

    def _get_control_selection_mode(self):
        """ Toolkit specific method to get the selection mode. """
        raise NotImplementedError()

    def _set_control_selection_mode(self, selection_mode):
        """ Toolkit specific method to change the selection mode. """
        raise NotImplementedError()

    def _selection_updated(self, event):
        """ Observer for selection trait. """
        if self.control is not None and not self._selection_updating_flag:
            with self._selection_updating():
                self._set_control_selection(self.selection)

    def _get_control_selection(self):
        """ Toolkit specific method to get the selection. """
        raise NotImplementedError()

    def _set_control_selection(self, selection):
        """ Toolkit specific method to change the selection. """
        raise NotImplementedError()

    def _observe_control_selection(self, remove=False):
        """ Toolkit specific method to watch for changes in the selection. """
        raise NotImplementedError()

    def _update_selection(self, *args, **kwargs):
        if not self._selection_updating_flag:
            with self._selection_updating():
                self.selection = self._get_control_selection()

    # ------------------------------------------------------------------------
    # Widget Interface
    # ------------------------------------------------------------------------

    def _create(self):
        """ Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """
        self.control = self._create_control(self.parent)
        self._initialize_control()
        self._add_event_listeners()

        self.show(self.visible)
        self.enable(self.enabled)

    def _initialize_control(self):
        """ Initializes the toolkit specific control.
        """
        logger.debug('Initializing DataViewWidget')
        self._set_control_header_visible(self.header_visible)
        self._set_control_selection_mode(self.selection_mode)
        self._set_control_selection_type(self.selection_type)

    def _add_event_listeners(self):
        logger.debug('Adding DataViewWidget listeners')
        super()._add_event_listeners()
        self.observe(
            self._header_visible_updated,
            'header_visible',
            dispatch='ui',
        )
        self.observe(
            self._selection_type_updated,
            'selection_type',
            dispatch='ui',
        )
        self.observe(
            self._selection_mode_updated,
            'selection_mode',
            dispatch='ui',
        )
        self.observe(
            self._selection_updated,
            'selection.items',
            dispatch='ui',
        )
        if self.control is not None:
            self._observe_control_selection()

    def _remove_event_listeners(self):
        logger.debug('Removing DataViewWidget listeners')
        if self.control is not None:
            self._observe_control_selection(remove=True)
        self.observe(
            self._header_visible_updated,
            'header_visible',
            dispatch='ui',
            remove=True,
        )
        self.observe(
            self._selection_type_updated,
            'selection_type',
            dispatch='ui',
            remove=True,
        )
        self.observe(
            self._selection_mode_updated,
            'selection_mode',
            dispatch='ui',
            remove=True,
        )
        self.observe(
            self._selection_updated,
            'selection.items',
            dispatch='ui',
            remove=True,
        )
        super()._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------

    @contextmanager
    def _selection_updating(self):
        """ Context manager to prevent loopback when updating selections. """
        if self._selection_updating_flag:
            yield
        else:
            self._selection_updating_flag = True
            try:
                yield
            finally:
                self._selection_updating_flag = False
