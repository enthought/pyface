# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from pyface.qt import QtCore
from pyface.qt.QtCore import Qt

from traits.api import Any, Bool, HasTraits, Instance, Str, provides

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

    #: A tooltip for the widget.
    tooltip = Str()

    #: An optional context menu for the widget.
    context_menu = Instance("pyface.action.menu_manager.MenuManager")

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

    def focus(self):
        """ Set the keyboard focus to this widget.
        """
        if self.control is not None:
            self.control.setFocus()

    def has_focus(self):
        """ Does the widget currently have keyboard focus?

        Returns
        -------
        focus_state : bool
            Whether or not the widget has keyboard focus.
        """
        return (
            self.control is not None
            and self.control.hasFocus()
        )

    def destroy(self):
        if self.control is not None:
            self.control.deleteLater()
            super().destroy()

    def _add_event_listeners(self):
        super()._add_event_listeners()
        self.control.installEventFilter(self._event_filter)

    def _remove_event_listeners(self):
        if self._event_filter is not None:
            if self.control is not None:
                self.control.removeEventFilter(self._event_filter)
            self._event_filter = None
        super()._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_tooltip(self):
        """ Toolkit specific method to get the control's tooltip. """
        return self.control.toolTip()

    def _set_control_tooltip(self, tooltip):
        """ Toolkit specific method to set the control's tooltip. """
        self.control.setToolTip(tooltip)

    def _observe_control_context_menu(self, remove=False):
        """ Toolkit specific method to change the control menu observer. """
        if remove:
            self.control.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
            self.control.customContextMenuRequested.disconnect(
                self._handle_control_context_menu
            )
        else:
            self.control.customContextMenuRequested.connect(
                self._handle_control_context_menu
            )
            self.control.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def _handle_control_context_menu(self, pos):
        """ Signal handler for displaying context menu. """
        if self.control is not None and self.context_menu is not None:
            pos = self.control.mapToGlobal(pos)
            menu = self.context_menu.create_menu(self.control)
            menu.show(pos.x(), pos.y())

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

        if event_type in {QtCore.QEvent.Type.Show, QtCore.QEvent.Type.Hide}:
            widget.visible = not widget.control.isHidden()

        return False
