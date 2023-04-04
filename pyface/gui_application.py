# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
This module defines a :py:class:`GUIApplication` subclass of
:py:class:`pyface.application.Application`.  This adds cross-platform GUI
application support to the base class via :py:class:`pyface.application.GUI`.

At a minimum this class expects to be provided with a factory that returns
:py:class:`pyface.i_window.IWindow` instances.  For pure Pyface applications
this is most likely to be a subclass of
:py:class:`pyface.application_window.ApplicationWindow`.

"""


import logging

from traits.api import (
    Bool,
    Callable,
    Instance,
    List,
    ReadOnly,
    Tuple,
    Undefined,
    Vetoable,
    observe,
)

from .application import Application
from .i_dialog import IDialog
from .i_splash_screen import ISplashScreen
from .i_window import IWindow
from .ui_traits import Image

logger = logging.getLogger(__name__)


def default_window_factory(application, **kwargs):
    """ The default window factory returns an application window.

    This is almost never the right thing, but allows users to get off the
    ground with the base class.
    """
    from pyface.application_window import ApplicationWindow

    return ApplicationWindow(**kwargs)


class GUIApplication(Application):
    """ A basic Pyface GUI application. """

    # 'GUIApplication' traits -------------------------------------------------

    # Branding ---------------------------------------------------------------

    #: The splash screen for the application. No splash screen by default
    splash_screen = Instance(ISplashScreen)

    #: The about dialog for the application.
    about_dialog = Instance(IDialog)

    #: Icon for the application (used in window titlebars)
    icon = Image

    #: Logo of the application (used in splash screens and about dialogs)
    logo = Image

    # Window management ------------------------------------------------------

    #: The window factory to use when creating a window for the application.
    window_factory = Callable(default_window_factory)

    #: Default window size
    window_size = Tuple((800, 600))

    #: Currently active Window if any
    active_window = Instance(IWindow)

    #: List of all open windows in the application
    windows = List(Instance(IWindow))

    #: The Pyface GUI instance for the application
    gui = ReadOnly

    # Protected interface ----------------------------------------------------

    #: Flag if the exiting of the application was explicitely requested by user
    # An 'explicit' exit is when the 'exit' method is called.
    # An 'implicit' exit is when the user closes the last open window.
    _explicit_exit = Bool(False)

    # -------------------------------------------------------------------------
    # 'GUIApplication' interface
    # -------------------------------------------------------------------------

    # Window lifecycle methods -----------------------------------------------

    def create_window(self, **kwargs):
        """ Create a new application window.

        By default uses the :py:attr:`window_factory` to do this.  Subclasses
        can override if they want to do something different or additional.

        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments to pass to the window factory.

        Returns
        -------
        window : IWindow  or None
            The new IWindow instance.
        """
        window = self.window_factory(application=self, **kwargs)

        if window.size == (-1, -1):
            window.size = self.window_size
        if not window.title:
            window.title = self.name
        if self.icon:
            window.icon = self.icon

        return window

    def add_window(self, window):
        """ Add a new window to the windows we are tracking. """

        # Keep a handle on all windows created so that non-active windows don't
        # get garbage collected
        self.windows.append(window)

        # Something might try to veto the opening of the window.
        opened = window.open()
        if opened:
            window.activate()

    # Action handlers --------------------------------------------------------

    def do_about(self):
        """ Display the about dialog, if it exists. """
        if self.about_dialog is not None:
            self.about_dialog.open()

    # -------------------------------------------------------------------------
    # 'Application' interface
    # -------------------------------------------------------------------------

    def start(self):
        """ Start the application, setting up things that are required

        Subclasses should open at least one ApplicationWindow or subclass in
        their start method, and should call the superclass start() method
        before doing any work themselves.
        """
        from pyface.gui import GUI

        ok = super().start()
        if ok:
            # create the GUI so that the splash screen comes up first thing
            if self.gui is Undefined:
                self.gui = GUI(splash_screen=self.splash_screen)

            # create the initial windows to show
            self._create_windows()

        return ok

    # -------------------------------------------------------------------------
    # 'GUIApplication' Private interface
    # -------------------------------------------------------------------------

    def _create_windows(self):
        """ Create the initial windows to display.

        By default calls :py:meth:`create_window` once. Subclasses can
        override this method.
        """
        window = self.create_window()
        self.add_window(window)

    # -------------------------------------------------------------------------
    # 'Application' private interface
    # -------------------------------------------------------------------------

    def _run(self):
        """ Actual implementation of running the application: starting the GUI
        event loop.
        """
        # Fire a notification that the app is running.  This is guaranteed to
        # happen after all initialization has occurred and the event loop has
        # started.  A listener for this event is a good place to do things
        # where you want the event loop running.
        self.gui.invoke_later(
            self._fire_application_event, "application_initialized"
        )

        # start the GUI - script blocks here
        self.gui.start_event_loop()
        return True

    # Destruction methods -----------------------------------------------------

    def _can_exit(self):
        """ Check with each window to see if it can be closed

        The fires closing events for each window, and returns False if any
        listener vetos.
        """
        if not super()._can_exit():
            return False

        for window in reversed(self.windows):
            window.closing = event = Vetoable()
            if event.veto:
                return False
        else:
            return True

    def _prepare_exit(self):
        """ Close each window """
        # ensure copy of list, as we modify original list while closing
        for window in list(reversed(self.windows)):
            window.destroy()
            window.closed = window

    def _exit(self):
        """ Shut down the event loop """
        self.gui.stop_event_loop()

    # Trait default handlers ------------------------------------------------

    def _window_factory_default(self):
        """ Default to ApplicationWindow

        This is almost never the right thing, but allows users to get off the
        ground with the base class.
        """
        from pyface.application_window import ApplicationWindow

        return lambda application, **kwargs: ApplicationWindow(**kwargs)

    def _splash_screen_default(self):
        """ Default SplashScreen """
        from pyface.splash_screen import SplashScreen

        dialog = SplashScreen()
        if self.logo:
            dialog.image = self.logo
        return dialog

    def _about_dialog_default(self):
        """ Default AboutDialog """
        from html import escape

        from pyface.about_dialog import AboutDialog

        additions = [
            "<h1>{}</h1>".format(escape(self.name)),
            "Copyright &copy; 2023 {}, all rights reserved".format(
                escape(self.company)
            ),
            "",
        ]
        additions += [escape(line) for line in self.description.split("\n\n")]

        dialog = AboutDialog(
            title="About {}".format(self.name), additions=additions
        )
        if self.logo:
            dialog.image = self.logo
        return dialog

    # Trait listeners --------------------------------------------------------

    @observe("windows:items:activated")
    def _on_activate_window(self, event):
        """ Listener that tracks currently active window.
        """
        window = event.object
        if window in self.windows:
            self.active_window = window

    @observe("windows:items:deactivated")
    def _on_deactivate_window(self, event):
        """ Listener that tracks currently active window.
        """
        self.active_window = None

    @observe("windows:items:closed")
    def _on_window_closed(self, event):
        """ Listener that ensures window handles are released when closed.
        """
        window = event.object
        if window in self.windows:
            self.windows.remove(window)
