# Copyright (c) 2005-18, Enthought, Inc.
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
""" The abstract interface for all pyface top-level windows. """

# Enthought library imports.
from traits.api import Event, Tuple, Unicode, Vetoable, VetoableEvent

# Local imports.
from pyface.constant import NO
from pyface.key_pressed_event import KeyPressedEvent
from pyface.i_widget import IWidget


class IWindow(IWidget):
    """ The abstract interface for all pyface top-level windows.

    A pyface top-level window has no visual representation until it is opened
    (ie. its 'control' trait will be None until it is opened).
    """

    # 'IWindow' interface -----------------------------------------------------

    #: The position of the window.
    position = Tuple

    #: The size of the window.
    size = Tuple

    #: The window title.
    title = Unicode

    # Window Events ----------------------------------------------------------

    #: The window has been opened.
    opened = Event

    #: The window is about to open.
    opening = VetoableEvent

    #: The window has been activated.
    activated = Event

    #: The window has been closed.
    closed = Event

    #: The window is about to be closed.
    closing = VetoableEvent

    #: The window has been deactivated.
    deactivated = Event

    #: A key was pressed while the window had focus.
    # FIXME v3: This smells of a hack. What's so special about key presses?
    # FIXME v3: Unicode
    key_pressed = Event(KeyPressedEvent)

    # -------------------------------------------------------------------------
    # 'IWindow' interface.
    # -------------------------------------------------------------------------

    def open(self):
        """ Opens the window.

        This fires the :py:attr:`closing` vetoable event, giving listeners the
        opportunity to veto the opening of the window.

        If the window is opened, the :py:attr:`opened` event will be fired
        with the IWindow instance as the event value.

        Returns
        -------
        opened : bool
            Whether or not the window was opened.
        """

    def close(self, force=False):
        """ Closes the window.

        This fires the :py:attr:`closing` vetoable event, giving listeners the
        opportunity to veto the closing of the window.  If :py:obj:`force` is
        :py:obj:`True` then the window will close no matter what.

        If the window is closed, the closed event will be fired with the window
        object as the event value.

        Parameters
        ----------
        force : bool
            Whether the window should close despite vetos.

        Returns
        -------
        closed : bool
            Whether or not the window is closed.
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
        self, message, title='Information', detail='', informative=''
    ):
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


class MWindow(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IWindow interface.

    Implements: close(), confirm(), open()
    Reimplements: _create()
    """

    # -------------------------------------------------------------------------
    # 'IWindow' interface.
    # -------------------------------------------------------------------------

    def open(self):
        """ Opens the window.

        This fires the :py:attr:`closing` vetoable event, giving listeners the
        opportunity to veto the opening of the window.

        If the window is opened, the :py:attr:`opened` event will be fired
        with the IWindow instance as the event value.

        Returns
        -------
        opened : bool
            Whether or not the window was opened.
        """
        self.opening = event = Vetoable()
        if not event.veto:
            # Create the control, if necessary.
            if self.control is None:
                self._create()

            self.show(True)
            self.opened = self

        return self.control is not None and not event.veto

    def close(self, force=False):
        """ Closes the window.

        This fires the :py:attr:`closing` vetoable event, giving listeners the
        opportunity to veto the closing of the window.  If :py:obj:`force` is
        :py:obj:`True` then the window will close no matter what.

        If the window is closed, the closed event will be fired with the window
        object as the event value.

        Parameters
        ----------
        force : bool
            Whether the window should close despite vetos.

        Returns
        -------
        closed : bool
            Whether or not the window is closed.
        """
        if self.control is not None:
            self.closing = event = Vetoable()
            if force or not event.veto:
                self.destroy()
                self.closed = self

        return self.control is None

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
        from .confirmation_dialog import confirm

        return confirm(self.control, message, title, cancel, default)

    def information(
        self, message, title='Information', detail='', informative=''
    ):
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
        from .message_dialog import information

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
        from .message_dialog import warning

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
        from .message_dialog import error

        error(self.control, message, title, detail, informative)
