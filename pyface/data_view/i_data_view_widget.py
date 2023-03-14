# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
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
    Bool, Enum, HasTraits, Instance, List, Property,
    TraitError, Tuple, cached_property,
)

from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.abstract_data_exporter import AbstractDataExporter
from pyface.i_drop_handler import IDropHandler
from pyface.i_layout_widget import ILayoutWidget


logger = logging.getLogger(__name__)


class IDataViewWidget(ILayoutWidget):
    """ Interface for data view widgets. """

    #: The data model for the data view.
    data_model = Instance(AbstractDataModel, allow_none=False)

    #: Whether or not the column headers are visible.
    header_visible = Bool(True)

    #: The global drop handlers for the data view.  These are intended to
    #: handle drop actions which either affect the whole data view, or where
    #: the data handler can work out how to change the underlying data without
    #: additional input.
    drop_handlers = List(Instance(IDropHandler, allow_none=False))

    #: What can be selected.  Implementations may optionally allow "column"
    #: and "item" selection types.
    selection_type = Enum("row",)

    #: How selections are modified.  Implementations may optionally allow
    #: "none" for no selection, or possibly other multiple selection modes
    #: as supported by the toolkit.
    selection_mode = Enum("extended", "single")

    #: The selected indices in the view.
    selection = List(Tuple)

    #: Exporters available for the DataViewWidget.
    exporters = List(Instance(AbstractDataExporter))


class MDataViewWidget(HasTraits):
    """ Mixin class for data view widgets. """

    # IDataViewWidget Interface traits --------------------------------------

    #: The data model for the data view.
    data_model = Instance(AbstractDataModel, allow_none=False)

    #: Whether or not the column headers are visible.
    header_visible = Bool(True)

    #: The global drop handlers for the data view.  These are intended to
    #: handle drop actions which either affect the whole data view, or where
    #: the data handler can work out how to change the underlying data without
    #: additional input.
    drop_handlers = List(Instance(IDropHandler, allow_none=False))

    #: The selected indices in the view.  This should never be mutated, any
    #: changes should be by replacement of the entire list.
    selection = Property(observe='_selection.items')

    #: Exporters available for the DataViewWidget.
    exporters = List(Instance(AbstractDataExporter))

    # Private traits --------------------------------------------------------

    #: Whether the selection is currently being updated.
    _selection_updating_flag = Bool()

    #: The selected indices in the view.  This should never be mutated, any
    #: changes should be by replacement of the entire list.
    _selection = List(Tuple)

    # ------------------------------------------------------------------------
    # MDataViewWidget Interface
    # ------------------------------------------------------------------------

    def _header_visible_updated(self, event):
        """ Observer for header_visible trait. """
        if self.control is not None:
            self._set_control_header_visible(event.new)

    def _get_control_header_visible(self):
        """ Toolkit specific method to get the visibility of the header.

        Returns
        -------
        control_header_visible : bool
            Whether or not the control's header is visible.
        """
        raise NotImplementedError()

    def _set_control_header_visible(self, control_header_visible):
        """ Toolkit specific method to set the visibility of the header.

        Parameters
        ----------
        control_header_visible : bool
            Whether or not the control's header is visible.
        """
        raise NotImplementedError()

    def _selection_type_updated(self, event):
        """ Observer for selection_type trait. """
        if self.control is not None:
            self._set_control_selection_type(event.new)
            self.selection = []

    def _get_control_selection_type(self):
        """ Toolkit specific method to get the selection type.

        Returns
        -------
        selection_type : str
            The type of selection the control is using.
        """
        raise NotImplementedError()

    def _set_control_selection_type(self, selection_type):
        """ Toolkit specific method to change the selection type.

        Parameters
        ----------
        selection_type : str
            The type of selection the control is using.
        """
        raise NotImplementedError()

    def _selection_mode_updated(self, event):
        """ Observer for selection_mode trait. """
        if self.control is not None:
            self._set_control_selection_mode(event.new)
            self.selection = []

    def _get_control_selection_mode(self):
        """ Toolkit specific method to get the selection mode.

        Returns
        -------
        selection_mode : str
            The selection mode the control is using (eg. single vs. extended
            selection).
        """
        raise NotImplementedError()

    def _set_control_selection_mode(self, selection_mode):
        """ Toolkit specific method to change the selection mode.

        Parameters
        ----------
        selection_mode : str
            The selection mode the control is using (eg. single vs. extended
            selection).
        """
        raise NotImplementedError()

    def _selection_updated(self, event):
        """ Observer for selection trait. """
        if self.control is not None and not self._selection_updating_flag:
            with self._selection_updating():
                self._set_control_selection(self.selection)

    def _get_control_selection(self):
        """ Toolkit specific method to get the selection.

        Returns
        -------
        selection : list of pairs of row and column indices
            The selected elements of the control.
        """
        raise NotImplementedError()

    def _set_control_selection(self, selection):
        """ Toolkit specific method to change the selection.

        Parameters
        ----------
        selection : list of pairs of row and column indices
            The selected elements of the control.
        """
        raise NotImplementedError()

    def _observe_control_selection(self, remove=False):
        """ Toolkit specific method to watch for changes in the selection.

        The _update_selection method is available as a toolkit-independent
        callback when the selection changes, but particular toolkits may
        choose to implement their own callbacks with similar functionality
        if appropriate.
        """
        raise NotImplementedError()

    def _update_selection(self, *args, **kwargs):
        """ Handle a toolkit even that  changes the selection.

        This is designed to be usable as a callback for a toolkit event
        or signal handler, so it accepts any arguments.
        """
        if not self._selection_updating_flag:
            with self._selection_updating():
                self._selection = self._get_control_selection()

    # ------------------------------------------------------------------------
    # Widget Interface
    # ------------------------------------------------------------------------

    def create(self, parent=None):
        """ Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """
        super().create(parent=parent)

        self.show(self.visible)
        self.enable(self.enabled)

    def _initialize_control(self):
        """ Initializes the toolkit specific control.
        """
        logger.debug('Initializing DataViewWidget')
        super()._initialize_control()
        self._set_control_header_visible(self.header_visible)
        self._set_control_selection_mode(self.selection_mode)
        self._set_control_selection_type(self.selection_type)
        self._set_control_selection(self.selection)

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
            '_selection.items',
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
            '_selection.items',
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

    # Trait property handlers

    @cached_property
    def _get_selection(self):
        return self._selection

    def _set_selection(self, selection):
        if self.selection_mode == 'none' and len(selection) != 0:
            raise TraitError(
                "Selection must be empty when selection_mode is 'none', "
                "got {!r}".format(selection)
            )
        elif self.selection_mode == 'single' and len(selection) > 1:
            raise TraitError(
                "Selection must have at most one element when selection_mode "
                "is 'single', got {!r}".format(selection)
            )

        if self.selection_type == 'row':
            for row, column in selection:
                if column != ():
                    raise TraitError(
                        "Column values must be () when selection_type is "
                        "'row', got {!r}".format(column)
                    )
                if not self.data_model.is_row_valid(row):
                    raise TraitError(
                        "Invalid row index {!r}".format(row)
                    )
        elif self.selection_type == 'column':
            for row, column in selection:
                if not (self.data_model.is_row_valid(row)
                        and self.data_model.can_have_children(row)
                        and self.data_model.get_row_count(row) > 0):
                    raise TraitError(
                        "Row values must have children when selection_type "
                        "is 'column', got {!r}".format(column)
                    )
                if not self.data_model.is_column_valid(column):
                    raise TraitError(
                        "Invalid column index {!r}".format(column)
                    )
        else:
            for row, column in selection:
                if not self.data_model.is_row_valid(row):
                    raise TraitError(
                        "Invalid row index {!r}".format(row)
                    )
                if not self.data_model.is_column_valid(column):
                    raise TraitError(
                        "Invalid column index {!r}".format(column)
                    )

        self._selection = selection
