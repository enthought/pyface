# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""

import wx

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
            self.control.Show(visible)

    def enable(self, enabled):
        """ Enable or disable the widget.

        Parameter
        ---------
        enabled : bool
            The enabled state to set the widget to.
        """
        self.enabled = enabled
        if self.control is not None:
            self.control.Enable(enabled)

    def focus(self):
        """ Set the keyboard focus to this widget.
        """
        if self.control is not None:
            self.control.SetFocus()

    def has_focus(self):
        """ Does the widget currently have keyboard focus?

        Returns
        -------
        focus_state : bool
            Whether or not the widget has keyboard focus.
        """
        return (
            self.control is not None
            and self.control.HasFocus()
        )

    def destroy(self):
        if self.control is not None:
            control = self.control
            super().destroy()
            control.Destroy()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_tooltip(self):
        """ Toolkit specific method to get the control's tooltip. """
        return self.control.GetToolTipText()

    def _set_control_tooltip(self, tooltip):
        """ Toolkit specific method to set the control's tooltip. """
        self.control.SetToolTip(tooltip)

    def _observe_control_context_menu(self, remove=False):
        """ Toolkit specific method to change the control menu observer. """
        if remove:
            self.control.Unbind(
                wx.EVT_CONTEXT_MENU, handler=self._handle_control_context_menu
            )
        else:
            self.control.Bind(
                wx.EVT_CONTEXT_MENU, self._handle_control_context_menu
            )

    def _handle_control_context_menu(self, event):
        """ Signal handler for displaying context menu. """
        if self.control is not None and self.context_menu is not None:
            menu = self.context_menu.create_menu(self.control)
            self.control.PopupMenu(menu)
