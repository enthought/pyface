# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The abstract interface for all pyface dialogs. """


from traits.api import Bool, Enum, HasTraits, Int, Str


from pyface.constant import OK
from pyface.i_window import IWindow


class IDialog(IWindow):
    """ The abstract interface for all pyface dialogs.

    Usage: Sub-class this class and either override '_create_contents' or
    more simply, just override the two methods that do the real work:-

    1) '_create_dialog_area' creates the main content of the dialog.
    2) '_create_buttons'     creates the dialog buttons.
    """

    # 'IDialog' interface -------------------------------------------------#

    #: The label for the 'cancel' button.  The default is toolkit specific.
    cancel_label = Str()

    #: The context sensitive help Id (the 'Help' button is only shown iff this
    #: is set).
    help_id = Str()

    #: The label for the 'help' button.  The default is toolkit specific.
    help_label = Str()

    #: The label for the 'ok' button.  The default is toolkit specific.
    ok_label = Str()

    #: Is the dialog resizeable?
    resizeable = Bool(True)

    #: The return code after the window is closed to indicate whether the dialog
    #: was closed via 'Ok' or 'Cancel').
    return_code = Int(OK)

    #: The dialog style (is it modal or not).
    # FIXME v3: It doesn't seem possible to use non-modal dialogs.  (How do you
    # get access to the buttons?)
    style = Enum("modal", "nonmodal")

    # ------------------------------------------------------------------------
    # 'IDialog' interface.
    # ------------------------------------------------------------------------

    def open(self):
        """ Opens the dialog.

        If the dialog is modal then the dialog's event loop is entered and the
        dialog closed afterwards.  The 'return_code' trait is updated according
        to the button the user pressed and this value is also returned.

        If the dialog is non-modal the return_code trait is set to 'OK'.

        Returns
        -------
        return_code : OK or CANCEL
            The value of the ``return_code`` trait.
        """

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_buttons(self, parent):
        """ Create and return the buttons.

        Parameters
        ----------
        parent : toolkit control
            The dialog's toolkit control to be used as the parent for
            buttons.

        Returns
        -------
        buttons : toolkit control
            A control containing the dialog's buttons.

        """

    def _create_contents(self, parent):
        """ Create and return the dialog's contents.

        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control to be used as the parent for
            widgets in the contents.

        Returns
        -------
        control : toolkit control
            A control to be used for contents of the window.
        """

    def _create_dialog_area(self, parent):
        """ Create and return the main content of the dialog's window.

        Parameters
        ----------
        parent : toolkit control
            A toolkit control to be used as the parent for widgets in the
            contents.

        Returns
        -------
        control : toolkit control
            A control to be used for main contents of the dialog.
        """

    def _show_modal(self):
        """ Opens the dialog as a modal dialog.

        Returns
        -------
        return_code : OK or CANCEL
            The return code from the user's interactions.
        """


class MDialog(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IDialog interface.

    Implements: open()
    Reimplements: _add_event_listeners(), create()
    """

    # ------------------------------------------------------------------------
    # 'IDialog' interface.
    # ------------------------------------------------------------------------

    def open(self):
        """ Opens the dialog.

        If the dialog is modal then the dialog's event loop is entered and the
        dialog closed afterwards.  The 'return_code' trait is updated according
        to the button the user pressed and this value is also returned.

        If the dialog is non-modal the return_code trait is set to 'OK'.

        Returns
        -------
        return_code : OK or CANCEL
            The value of the ``return_code`` trait.
        """
        if self.control is None:
            self.create()

        if self.style == "modal":
            self.return_code = self._show_modal()
            self.close()

        else:
            self.show(True)
            self.return_code = OK

        return self.return_code

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def create(self, parent=None):
        """ Creates the window's widget hierarchy. """

        super().create(parent=parent)

        self._create_contents(self.control)
