# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# Copyright (c) 2017, Enthought, Inc
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply
#
# Author: Riverbank Computing Limited
# Description: <Enthought pyface package component>


# Major package imports.
from pyface.qt import QtCore, QtGui

# Enthought library imports.
from traits.api import Any, Bool, HasTraits, provides

# Local imports.
from pyface.i_widget import IWidget, MWidget


@provides(IWidget)
class Widget(MWidget, HasTraits):
    """ The toolkit specific implementation of a Widget.  See the IWidget
    interface for the API documentation.
    """

    # 'IWidget' interface ----------------------------------------------------

    #: The toolkit specific control that represents the widget.
    control = Any

    #: The control's optional parent control.
    parent = Any

    #: Whether or not the control is visible
    visible = Bool(True)

    #: Whether or not the control is enabled
    enabled = Bool(True)

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
        if self.control is not None:
            self._remove_event_listeners()
            self.control.hide()
            self.control.deleteLater()
            self.control = None

    # Trait change handlers --------------------------------------------------

    def _visible_changed(self, new):
        if self.control is not None:
            self.show(new)

    def _enabled_changed(self, new):
        if self.control is not None:
            self.enable(new)


class WidgetEventFilter(QtCore.QObject):
    """ An internal class that watches for certain events on behalf of the
    Widget instance.
    """

    def __init__(self, widget):
        """ Initialise the event filter. """
        QtCore.QObject.__init__(self)
        widget.control.installEventFilter(self)
        self._widget = widget

    def eventFilter(self, obj, event):
        """ Adds any event listeners required by the window. """
        widget = self._widget
        # Sanity check.
        if obj is not widget.control:
            return False

        event_type = event.type()

        if event_type in {QtCore.QEvent.Show, QtCore.QEvent.Hide}:
            widget.visible = widget.control.isVisible()

        return False
