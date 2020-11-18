# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from pyface.qt import QtCore, QtGui


from traits.api import Any, Bool, HasTraits, Instance, provides


from pyface.i_widget import IWidget, MWidget


@provides(IWidget)
class Widget(MWidget, HasTraits):
    """ The toolkit specific implementation of a Widget.  See the IWidget
    interface for the API documentation.
    """

    # 'IWidget' interface ----------------------------------------------------

    #: The toolkit specific control that represents the widget.
    control = Any()

    #: The control's optional parent control.
    parent = Any()

    #: Whether or not the control is visible
    visible = Bool(True)

    #: Whether or not the control is enabled
    enabled = Bool(True)

    # Private interface ----------------------------------------------------

    #: The event filter for the widget.
    _event_filter = Instance(QtCore.QObject)

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def show(self, visible):
        """ Show or hide the widget.

        Parameter
        ---------
        visible : bool
            Visible should be ``True`` if the widget should be shown.
        """
        self.visible = visible
        if self.control is not None:
            self.control.setVisible(visible)

    def enable(self, enabled):
        """ Enable or disable the widget.

        Parameter
        ---------
        enabled : bool
            The enabled state to set the widget to.
        """
        self.enabled = enabled
        if self.control is not None:
            self.control.setEnabled(enabled)

    def destroy(self):
        self._remove_event_listeners()
        if self.control is not None:
            self.control.hide()
            self.control.deleteLater()
            self.control = None

    def _add_event_listeners(self):
        self.control.installEventFilter(self._event_filter)

    def _remove_event_listeners(self):
        if self._event_filter is not None:
            if self.control is not None:
                self.control.removeEventFilter(self._event_filter)
            self._event_filter = None

    # Trait change handlers --------------------------------------------------

    def _visible_changed(self, new):
        if self.control is not None:
            self.show(new)

    def _enabled_changed(self, new):
        if self.control is not None:
            self.enable(new)

    def __event_filter_default(self):
        return WidgetEventFilter(self)


class WidgetEventFilter(QtCore.QObject):
    """ An internal class that watches for certain events on behalf of the
    Widget instance.

    This filter watches for show and hide events to make sure that visible
    state of the widget is the opposite of Qt's isHidden() state.  This is
    needed in case other code hides the toolkit widget
    """

    def __init__(self, widget):
        """ Initialise the event filter. """
        QtCore.QObject.__init__(self)
        self._widget = widget

    def eventFilter(self, obj, event):
        """ Adds any event listeners required by the window. """
        widget = self._widget
        # Sanity check.
        if obj is not widget.control:
            return False

        event_type = event.type()

        if event_type in {QtCore.QEvent.Show, QtCore.QEvent.Hide}:
            widget.visible = not widget.control.isHidden()

        return False
