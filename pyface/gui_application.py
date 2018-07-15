# Copyright (c) 2014-2017 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" Define a base application class to create the event loop, and launch
the creation of application windows.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging
from traceback import format_exception, format_exception_only

from traits.api import (
    Bool, Instance, List, ReadOnly, Tuple, Undefined, Vetoable, on_trait_change
)

from .application import (
    ApplicationEvent, ApplicationExit, BaseApplication
)
from .i_dialog import IDialog
from .i_image_resource import IImageResource
from .i_splash_screen import ISplashScreen
from .i_window import IWindow

logger = logging.getLogger(__name__)


class GUIApplication(BaseApplication):
    """ A basic Pyface GUI application.

    This handles setting up starting up the GUI, window management, logging,
    and other common features that we want when creating a GUI application.

    Often you will want to subclass this application, but it can be used as-is
    by hooking a listener to the `application_initialized` event::

        from pyface.api import ApplicationWindow, HeadingText

        class MainWindow(ApplicationWindow):
            def _create_contents(self, parent):
                self._label = HeadingText(parent, text="Hello World")
                return self._label.control

        def main():
            application = Application(id='hello-world', name='Hello World')
            window = MainWindow()
            application.on_trait_change(
                lambda: application.add_window(window),
                'application_initialized'
            )
            application.run()

    """

    # -------------------------------------------------------------------------
    # 'Application' interface
    # -------------------------------------------------------------------------

    # Branding ----------------------------------------------------------------

    #: The splash screen for the application. No splash screen by default
    splash_screen = Instance(ISplashScreen)

    #: The about dialog for the application.
    about_dialog = Instance(IDialog)

    #: Icon for the application
    icon = Instance(IImageResource)

    # Window management -------------------------------------------------------

    #: Default window size
    window_size = Tuple((800, 600))

    #: Currently active Window if any
    active_window = Instance(IWindow)

    #: List of all open windows in the application
    windows = List(Instance(IWindow))

    #: The Pyface GUI instance for the application
    gui = ReadOnly

    # Protected interface -----------------------------------------------------

    #: Flag if the exiting of the application was explicitely requested by user
    # An 'explicit' exit is when the 'exit' method is called.
    # An 'implicit' exit is when the user closes the last open window.
    _explicit_exit = Bool(False)

    # Window lifecycle methods -----------------------------------------------

    def add_window(self, window):
        """ Add a new window to the windows we are tracking. """
        if window.size == (-1, -1):
            window.size = self.window_size
        if not window.title:
            window.title = self.name
        if self.icon:
            window.icon = self.icon

        # Keep a handle on all windows created so that non-active windows don't
        # get garbage collected
        self.windows.append(window)

        window.open()

    def do_about(self):
        """ Display the about dialog, if it exists. """
        if self.about_dialog is not None:
            self.about_dialog.open()

    # -------------------------------------------------------------------------
    # 'BaseApplication' interface
    # -------------------------------------------------------------------------

    def start(self):
        """ Start the application, setting up things that are required

        Subclasses should open at least one ApplicationWindow or subclass in
        their start method, and should call the superclass start() method
        before doing any work themselves.
        """
        from pyface.gui import GUI

        ok = super(Application, self).start()
        if ok:
            # create the GUI so that the splash screen comes up first thing
            if self.gui is Undefined:
                self.gui = GUI(splash_screen=self.splash_screen)

        return ok

    # -------------------------------------------------------------------------
    # 'BaseApplication' private interface
    # -------------------------------------------------------------------------

    def _run(self):
        """ Actual implementation of running the application: starting the GUI
        event loop.
        """
        # Fire a notification that the app is running.  This is guaranteed to
        # happen after all initialization has occurred and the event loop has
        # started.  A listener for this event is a good place to do things like
        # opening application windows and other activities where you want the
        # event loop running.
        self.gui.invoke_later(
            self._fire_application_event, 'application_initialized'
        )

        # start the GUI - script blocks here
        self.gui.start_event_loop()
        return True

    # Exception handling ------------------------------------------------------

    def _unhandled_exception(self, type, value, traceback):
        """ Show an error dialog with exception information, if possible. """
        from pyface.message_dialog import error

        informative = """An unexpected error occurred: {}""".format(
            format_exception_only(type, value))
        detail = format_exception(type, value, traceback)
        error("Unhandled Exception", informative=informative, detail=detail)

    def _excepthook(self, type, value, traceback):
        """ Handle any exceptions not explicitly caught

        Try to display an appropriate error dialog, if possible.  Fail over to
        the standard excepthook if that doesn't work.
        """
        try:
            if issubclass(type, ApplicationExit):
                if value.args:
                    logger.excpetion("Unhandled ApplicationExit")
                else:
                    logger.info("Unhandled ApplicationExit")
                self._exit()
            else:
                # try to log the exception, could fail eg. if disk full
                logger.exception("Unhandled exception")
                self._unhandled_exception(type, value, traceback)
        except Exception:
            # something went wrong, use base class excepthook
            super(Application, self)._excepthook(type, value, traceback)

    # Destruction methods -----------------------------------------------------

    def _can_exit(self):
        """ Check with each window to see if it can be closed

        The fires closing events for each window, and returns False if any
        listener vetos.
        """
        if not super(Application, self)._can_exit():
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

    # -------------------------------------------------------------------------
    # Private interface
    # -------------------------------------------------------------------------

    # Initialization utilities ------------------------------------------------

    @on_trait_change('windows:activate')
    def _on_activate_window(self, window, trait, old, new):
        """ Listener that tracks currently active window.
        """
        self.active_window = window

    # Destruction utilities ---------------------------------------------------

    @on_trait_change('windows:closed')
    def _on_window_closed(self, window, trait, old, new):
        """ Listener that ensures window handles are released when closed.
        """
        if window in self.windows:
            self.windows.remove(window)
