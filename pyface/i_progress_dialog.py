# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""The interface for a dialog that allows the user to display progress of an
operation."""


from traits.api import Any, Bool, HasTraits, Int, Str


from pyface.i_dialog import IDialog


class IProgressDialog(IDialog):
    """ A simple progress dialog window which allows itself to be updated
    """

    # 'IProgressDialog' interface ---------------------------------#

    #: The message to display in the dialog
    message = Str()

    #: The minimum progress value
    min = Int()

    #: The maximum progress value
    max = Int()

    #: The margin around the progress bar
    margin = Int(5)

    #: Whether the operation can be cancelled
    can_cancel = Bool(False)

    #: Whether to show progress times
    show_time = Bool(False)

    #: Whether to show progress percent
    show_percent = Bool(False)

    #: Label for the 'cancel' button
    cancel_button_label = Str()

    # ------------------------------------------------------------------------
    # 'IProgressDialog' interface.
    # ------------------------------------------------------------------------

    def update(self, value):
        """ Update the progress bar to the desired value

        If the value is >= the maximum and the progress bar is not contained
        in another panel the parent window will be closed.

        Parameters
        ----------
        value :
            The progress value to set.
        """

    def change_message(self, message):
        """ Change the displayed message in the progress dialog

        Parameters
        ----------
        message : str or unicode
            The new message to display.

        """


class MProgressDialog(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IProgressDialog interface.

    Implements: update()
    """

    #: The progress bar toolkit object
    # XXX why not the control?
    progress_bar = Any()

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def open(self):
        """ Open the dialog """
        if self.max < self.min:
            msg = "Dialog min ({}) is greater than dialog max ({})."
            raise AttributeError(msg.format(self.min, self.max))

        super().open()

    # ------------------------------------------------------------------------
    # 'IProgressDialog' interface.
    # ------------------------------------------------------------------------

    def update(self, value):
        """ Update the progress bar to the desired value

        If the value is >= the maximum and the progress bar is not contained
        in another panel the parent window will be closed.

        Parameters
        ----------
        value :
            The progress value to set.
        """

        if self.progress_bar is not None:
            self.progress_bar.update(value)

        if value >= self.max:
            self.close()

    def change_message(self, message):
        """ Change the displayed message in the progress dialog

        Parameters
        ----------
        message : str or unicode
            The new message to display.

        """
        self.message = message
