# Copyright (c) 2014-2016 by Enthought, Inc., Austin, TX
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
import sys
from traceback import format_exception, format_exception_only

from traits.api import Instance, List, Tuple, Vetoable

from .base_application import ApplicationEvent, BaseApplication
from .i_gui import IGUI
from .i_image_resource import IImageResource
from .i_splash_screen import ISplashScreen
from .i_window import IWindow

logger = logging.getLogger(__name__)


def clear_handlers(logger):
    """ Remove all handlers from the given logger. """
    for handler in logger.handlers[::-1]:
        if hasattr(handler, 'close'):
            handler.close()
        logger.removeHandler(handler)


class Application(BaseApplication):
    """ A basic Pyface application.

    This handles setting up starting up the GUI, window management, logging,
    and other common features that we want when creating a GUI application.

    Often you will want to subclass this application, but it can be used as-is
    by hooking a listener to the `application_initialized` event::


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
    gui = Instance(IGUI)

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

        # set up window listeners
        # NOTE: 'activated' is not fired on a window when the window first
        # opens and gets focus. It is only fired when the window comes from
        # lower in the stack to be the active window.
        window.on_trait_change(self._on_activate_window, 'activated')
        window.on_trait_change(self._on_window_closing, 'closing')
        window.on_trait_change(self._on_window_closed, 'closed')
        window.open()

    # -------------------------------------------------------------------------
    # 'BaseApplication' interface
    # -------------------------------------------------------------------------

    def start(self):
        """ Start the application, setting up things that are required

        Subclasses should open at least one ApplicationWindow or subclass in
        their start method, and should call the superclass start() method
        before doing any work themselves.
        """
        ok = super(Application, self).start()
        if ok:
            # set up logging so messages can be displayed on splash screen
            self._setup_logging()

            # create the GUI so that the splash screen comes up first thing
            self.gui

        return ok

    def stop(self):
        """ Stop the application, cleanly releasing resources, if possible. """
        ok = super(Application, self).stop()
        if ok:
            self._reset_logger()
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
        self.gui.set_trait_later(
            self, 'application_initialized',
            ApplicationEvent(application=self, event_type='initialized'))

        # start the GUI - script blocks here
        self.gui.start_event_loop()

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
            # try to log the exception, could fail eg. if disk full
            logger.exception(value)
            self._unhandled_exception(type, value, traceback)
        except Exception:
            # something went wrong, use base class excepthook
            super(Application, self)._excepthook(type, value, traceback)
        finally:
            sys.exit(1)

    # Destruction methods -----------------------------------------------------

    def _can_exit(self):
        """ Check with each window to see if it can be closed """
        for window in reversed(self.windows):
            window.closing = event = Vetoable()
            if event.veto:
                return False
        else:
            return True

    def _prepare_exit(self):
        """ Close each window """
        for window in reversed(self.windows):
            window.destroy()
            window.closed = True

    def _exit(self):
        """ Shut down the event loop """
        self.gui.stop_event_loop()

    # -------------------------------------------------------------------------
    # Private interface
    # -------------------------------------------------------------------------

    # Initialization utilities ------------------------------------------------

    def _setup_logging(self):
        """ Initialize logger.

        By default send logging to a stream and set the log level to info.
        Most applications will want to replace this with something more
        appropriate to their needs.
        """
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)

    def _on_activate_window(self, window, trait, old, new):
        """ Listener that ensures active undo command stack is correct.
        """
        self.active_window = window

    # Destruction utilities ---------------------------------------------------

    def _on_window_closing(self, window, trait, old, new):
        """ Custom behavior when the closing of a window is requested."""
        pass

    def _on_window_closed(self, window, trait, old, new):
        """ Listener that ensures window handles are released when closed.
        """
        self.windows.remove(window)
        window.on_trait_change(self._on_activate_window, 'activated', )
        window.on_trait_change(self._on_window_closing, 'closing')
        window.on_trait_change(self._on_window_closed, 'closed')

    def _reset_logger(self):
        """ Reset root logger to default WARNING level and remove all handlers.
        """
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)
        clear_handlers(logger)

    # Trait initializers ------------------------------------------------------

    def _gui_default(self):
        from pyface.api import GUI

        return GUI(splash_screen=self.splash_screen)
