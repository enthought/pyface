# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
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


from traits.api import Any, Bool, HasTraits, provides


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
            self.control.Destroy()
            self.control = None
