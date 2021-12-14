# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance, provides

from pyface.qt.QtCore import Qt
from pyface.qt.QtGui import QWidget, QScrollArea

from pyface.i_scrolled import IScrolled, MScrolled
from .layout_widget import LayoutWidget


@provides(IScrolled)
class Scrolled(MScrolled, LayoutWidget):
    """ Widget that applies scrollbars to a toolkit control.

    This is an abstract class: subclasses need to provide an appropriate
    _create_contents method.
    """

    #: The contents of the scrolled widget.
    toolkit_contents = Instance(QWidget)

    def _create_control(self, parent):
        scrolled = QScrollArea(parent=parent)
        return scrolled

    def _initialize_control(self):
        self._set_horizontal_scroll(self.horizontal_scroll)
        self._set_vertical_scroll(self.vertical_scroll)

    def _add_event_listeners(self):
        super()._add_event_listeners()
        self.observe(
            self._vertical_scroll_updated,
            "vertical_scroll",
            dispatch="ui",
        )
        self.observe(
            self._horizontal_scroll_updated,
            "horizontal_scroll",
            dispatch="ui",
        )

    def _remove_event_listeners(self):
        self.observe(
            self._horizontal_scroll_updated,
            "horizontal_scroll",
            dispatch="ui",
            remove=True,
        )
        self.observe(
            self._vertical_scroll_updated,
            "vertical_scroll",
            dispatch="ui",
            remove=True,
        )
        super()._remove_event_listeners()

    def _initialize_contents(self):
        super()._initialize_content()
        self.setWidget(self._content)

    def _clear_contents(self):
        # ensure that the ownership of the contents is handed back to Python
        self.takeWidget()
        super()._clear_content()

    def _set_vertical_scroll(self, vertical_scroll):
        if vertical_scroll:
            self.control.setVerticalScrollBarPolicy(
                Qt.ScrollBarAsNeeded
            )
        else:
            self.control.setVerticalScrollBarPolicy(
                Qt.ScrollBarAlwaysOff
            )

    def _set_horizontal_scroll(self, horizontal_scroll):
        if horizontal_scroll:
            self.control.setHorizontalScrollBarPolicy(
                Qt.ScrollBarAsNeeded
            )
        else:
            self.control.setHorizontalScrollBarPolicy(
                Qt.ScrollBarAlwaysOff
            )

    def _vertical_scroll_updated(self, event):
        if self.control is not None:
            self._set_vertical_scroll(event.new)

    def _horizontal_scroll_updated(self, event):
        if self.control is not None:
            self._set_horizontal_scroll(event.new)
