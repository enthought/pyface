#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" The abstract interface for all pyface top-level windows. """


# Enthought library imports.
from traits.api import Event, Tuple, Unicode

# Local imports.
from pyface.constant import NO
from pyface.key_pressed_event import KeyPressedEvent
from pyface.i_widget import IWidget


class IWindow(IWidget):
    """ The abstract interface for all pyface top-level windows.

    A pyface top-level window has no visual representation until it is opened
    (ie. its 'control' trait will be None until it is opened).
    """

    #### 'IWindow' interface ##################################################

    #: The position of the window.
    position = Tuple

    #: The size of the window.
    size = Tuple

    #: The window title.
    title = Unicode

    #### Events #####

    #: The window has been activated.
    activated = Event

    #: The window has been closed.
    closed =  Event

    #: The window is about to be closed.
    closing =  Event

    #: The window has been deactivated.
    deactivated = Event

    #: A key was pressed while the window had focus.
    # FIXME v3: This smells of a hack. What's so special about key presses?
    # FIXME v3: Unicode
    key_pressed = Event(KeyPressedEvent)

    #: The window has been opened.
    opened = Event

    #: The window is about to open.
    opening = Event

    ###########################################################################
    # 'IWindow' interface.
    ###########################################################################

    def open(self):
        """ Opens the window. """

    def close(self):
        """ Closes the window. """

    def activate(self):
        """ Activates the window. """

    def show(self, visible):
        """ Show or hide the window.

        Parameter
        ---------
        visible : bool
            Visible should be ``True`` if the window should be shown.
        """

    def confirm(self, message, title=None, cancel=False, default=NO):
        """ Convenience method to show a confirmation dialog.

        Parameters
        ----------
        message : str
            The text of the message to display.
        title : str
            The text of the dialog title.
        cancel : bool
            ``True`` if the dialog should contain a Cancel button.
        default : NO, YES or CANCEL
            Which button should be the default button.
        """

    def information(
            self, message, title='Information', detail='', informative=''):
        """ Convenience method to show an information message dialog.

        Parameters
        ----------
        message : str
            The text of the message to display.
        title : str
            The text of the dialog title.
        detail : str
            Further details about the message.
        informative : str
            Explanatory text to display along with the message.

        """

    def warning(self, message, title='Warning', detail='', informative=''):
        """ Convenience method to show a warning message dialog.

        Parameters
        ----------
        message : str
            The text of the message to display.
        title : str
            The text of the dialog title.
        detail : str
            Further details about the message.
        informative : str
            Explanatory text to display along with the message.

        """

    def error(self, message, title='Error', detail='', informative=''):
        """ Convenience method to show an error message dialog.

        Parameters
        ----------
        message : str
            The text of the message to display.
        title : str
            The text of the dialog title.
        detail : str
            Further details about the message.
        informative : str
            Explanatory text to display along with the message.

        """

    ###########################################################################
    # Protected 'IWindow' interface.
    ###########################################################################

    def _add_event_listeners(self):
        """ Adds any event listeners required by the window. """


class MWindow(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IWindow interface.

    Implements: close(), confirm(), open()
    Reimplements: _create()
    """

    ###########################################################################
    # 'IWindow' interface.
    ###########################################################################

    def open(self):
        """ Opens the window. """

        # Trait notification.
        self.opening = self

        if self.control is None:
            self._create()

        self.show(True)

        # Trait notification.
        self.opened = self

    def close(self):
        """ Closes the window. """

        if self.control is not None:
            # Trait notification.
            self.closing = self

            # Cleanup the toolkit-specific control.
            self.destroy()

            # Trait notification.
            self.closed = self

    def confirm(self, message, title=None, cancel=False, default=NO):
        """ Convenience method to show a confirmation dialog.

        Parameters
        ----------
        message : str
            The text of the message to display.
        title : str
            The text of the dialog title.
        cancel : bool
            ``True`` if the dialog should contain a Cancel button.
        default : NO, YES or CANCEL
            Which button should be the default button.
        """
        from confirmation_dialog import confirm

        return confirm(self.control, message, title, cancel, default)

    def information(
            self, message, title='Information', detail='', informative=''):
        """ Convenience method to show an information message dialog.

        Parameters
        ----------
        message : str
            The text of the message to display.
        title : str
            The text of the dialog title.
        detail : str
            Further details about the message.
        informative : str
            Explanatory text to display along with the message.

        """
        from message_dialog import information

        information(self.control, message, title, detail, informative)

    def warning(self, message, title='Warning', detail='', informative=''):
        """ Convenience method to show a warning message dialog.

        Parameters
        ----------
        message : str
            The text of the message to display.
        title : str
            The text of the dialog title.
        detail : str
            Further details about the message.
        informative : str
            Explanatory text to display along with the message.

        """
        from message_dialog import warning

        warning(self.control, message, title, detail, informative)

    def error(self, message, title='Error', detail='', informative=''):
        """ Convenience method to show an error message dialog.

        Parameters
        ----------
        message : str
            The text of the message to display.
        title : str
            The text of the dialog title.
        detail : str
            Further details about the message.
        informative : str
            Explanatory text to display along with the message.

        """
        from message_dialog import error

        error(self.control, message, title, detail, informative)

    ###########################################################################
    # Protected 'IWidget' interface.
    ###########################################################################

    def _create(self):
        """ Creates the window's widget hierarchy. """

        # Create the toolkit-specific control.
        super(MWindow, self)._create()

        # Wire up event any event listeners required by the window.
        self._add_event_listeners()
