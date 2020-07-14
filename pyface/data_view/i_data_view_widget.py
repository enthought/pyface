# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Bool, HasStrictTraits, Instance

from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.i_widget import IWidget


class IDataViewWidget(IWidget):

    #: Whether or not the column headers are visible.
    header_visible = Bool(True)

    #: The data model for the data view.
    data_model = Instance(AbstractDataModel, allow_none=False)


class MDataViewWidget(HasStrictTraits):

    #: Whether or not the column headers are visible.
    header_visible = Bool(True)

    #: The data model for the data view.
    data_model = Instance(AbstractDataModel, allow_none=False)

    def _add_event_listeners(self):
        super()._add_event_listeners()
        self.observe(
            self._header_visible_updated, 'header_visible', dispatch='ui')

    def _remove_event_listeners(self):
        self.observe(
            self._header_visible_updated,
            'header_visible',
            dispatch='ui',
            remove=True,
        )
        super()._remove_event_listeners()

    def _header_visible_updated(self, event):
        """ Observer for header_visible trait. """
        if self.control is not None:
            self._set_control_header_visible(event.new)

    def _get_control_header_visible(self):
        """ Toolkit specific method to get the visibility of the header. """
        raise NotImplementedError()

    def _set_control_header_visible(self, tooltip):
        """ Toolkit specific method to set the visibility of the header. """
        raise NotImplementedError()
