# Copyright (c) 2013-2016 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" Define a base Task application class to create the event loop, and launch
the creation of tasks and corresponding windows.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import logging

from traits.api import (Bool, Event, HasStrictTraits, Instance, List, Property,
                        Str, Tuple, Vetoable)
from traits.etsconfig.etsconfig import ETSConfig

from ..image_resource import ImageResource
from .task_window import TaskWindow

logger = logging.getLogger(__name__)


class ApplicationEvent(HasStrictTraits):

    #: The application that the event happened to.
    application = Instance('TaskApplication')

    #: The type of application event.
    event_type = Str


class TaskApplication(HasStrictTraits):
    """ A base class for Pyface tasks applications.

    This handles setting up logging, starting up the GUI, and other common
    features that we want when creating a GUI application.
    """

    # -------------------------------------------------------------------------
    # 'TaskGuiApplication' interface
    # -------------------------------------------------------------------------

    # Branding ----------------------------------------------------------------

    #: Application name in CamelCase. Used to set ETSConfig.application_data
    app_name = Str('DefaultApplication')

    #: The splash screen for the application. No splash screen by default
    splash_screen = Instance('pyface.i_splash_screen.ISplashScreen')

    #: Icon for the application
    icon = Instance(ImageResource)

    #: Location of the log files ($ETSConfig.application_data$/logdir)
    logdir = Str

    # Window management -------------------------------------------------------

    #: Default window size
    window_size = Tuple((800, 600))

    #: Currently active TaskWindow if any
    active_window = Instance("pyface.tasks.task_window.TaskWindow")

    #: List of all windows ever created
    windows_created = List(Instance("pyface.tasks.task_window.TaskWindow"))

    # Tasks management --------------------------------------------------------

    #: List of all tasks created
    tasks_created = List("pyface.tasks.task.Task")

    #: Currently active Task if any
    active_task = Property

    # Application lifecycle events -------------------------------------------

    #: Fired when the application is starting. Called immediately before the
    #: start method is run.
    starting = Event(ApplicationEvent)

    #: Upon successful completion of the start method.
    started = Event(ApplicationEvent)

    #: Fired after the GUI event loop has been started.
    application_initialized = Event(ApplicationEvent)

    #: Fired when the application is starting. Called immediately before the
    #: start method is run.
    stopping = Event(ApplicationEvent)

    #: Upon successful completion of the stop method.
    stopped = Event(ApplicationEvent)

    # Other -------------------------------------------------------------------

    #: The UndoManager for the application.
    undo_manager = Instance('apptools.undo.i_undo_manager.IUndoManager')

    #: The root preferences node.
    preferences = Instance('apptools.preferences.i_preferences.IPreferences')


    #: The Pyface GUI instance for the application
    gui = Instance('pyface.i_gui.IGUI')

    # Protected interface -----------------------------------------------------

    # An 'explicit' exit is when the the 'exit' method is called.
    # An 'implicit' exit is when the user closes the last open window.
    _explicit_exit = Bool(False)

    # Application lifecycle methods -------------------------------------------

    def start(self):
        """ Start the application, setting up things that are required

        Subclasses should open at least one ApplicationWindow or subclass in
        their start method, and should call the superclass start() method
        before doing any work themselves.
        """
        self._initialize_application_home()
        self._setup_logging()
        logger.info('---- Application starting ----')

        # create the GUI so that the splash screen comes up first thing
        self.gui

        return True

    def stop(self):
        """ Stop the application, cleanly releasing resources, if possible. """
        logger.info('---- Application stopping ----')
        self._reset_logger()
        return True

    def run(self):
        """ Run the application """

        # Start up the application.
        self.starting = ApplicationEvent(application=self)
        started = self.start()
        if started:
            logger.info('---- Application started ----')
            self.started = ApplicationEvent(application=self)

            self._run()

            # We have finished running, so shut the application down.
            self.stopping = ApplicationEvent(application=self)
            stopped = self.stop()
            if stopped:
                self.stopped = ApplicationEvent(application=self)
                logger.info('---- Application stopped ----')

    def exit(self, force=False):
        """ Exits the application, closing all open task windows.

        Each window is sent a veto-able closing event. If any window vetoes the
        close request, no window will be closed. Otherwise, all windows will be
        closed and the GUI event loop will terminate.

        This method is not called when the user clicks the close button on a
        window or otherwise closes a window through his or her window
        manager. It is only called via the File->Exit menu item. It can also,
        of course, be called programatically.

        Parameters:
        -----------
        force : bool, optional (default False)
            If set, windows will receive no closing events and will be
            destroyed unconditionally. This can be useful for reliably tearing
            down regression tests, but should be used with caution.

        Returns:
        --------
        A boolean indicating whether the application exited.
        """
        self._explicit_exit = True
        try:
            if not force:
                for window in reversed(self.windows_created):
                    window.closing = event = Vetoable()
                    if event.veto:
                        return False

            self._prepare_exit()
            for window in reversed(self.windows_created):
                window.destroy()
                window.closed = True
        finally:
            self._explicit_exit = False
        self.gui.stop_event_loop()
        return True

    # Window lifecycle methods -----------------------------------------------

    def create_task_window(self, task):
        """ Connect task to application and open task in a new window.
        """
        if task not in self.tasks_created:
            self.tasks_created.append(task)

        window = TaskWindow(size=self.window_size)
        if self.icon:
            window.icon = self.icon

        # Keep a handle on all windows created so that non-active windows don't
        # get garbage collected
        self.windows_created.append(window)

        # set up listener to ensure we release reference to windows
        window.on_trait_change(self._on_close_window, 'closed')

        # set up listener to ensure undo manager has correct active stack
        window.on_trait_change(self._on_activate_window, 'activated')

        window.add_task(task)
        window.open()

        return window

    def _on_close_window(self, window, trait, old, new):
        """ Listener that ensures windows are released when closed.
        """
        if window.active_task in self.tasks_created:
            self.tasks_created.remove(window.active_task)

        self.windows_created.remove(window)

    def _on_activate_window(self, window, trait, old, new):
        """ Listener that ensures active undo command stack is correct. """
        if getattr(window.active_task, 'command_stack', None) is not None:
            self.undo_manager.active_stack = window.active_task.command_stack

        self.active_window = window

    # -------------------------------------------------------------------------
    # Private interface
    # -------------------------------------------------------------------------

    def _initialize_application_home(self):
        """ Setup the home directory for the application where logs, preference
        files and other config files will be stored.
        """
        ETSConfig.application_data = os.path.join(ETSConfig.application_data,
                                                  self.app_name)
        ETSConfig.application_home = ETSConfig.application_data
        ETSConfig.user_data = ETSConfig.application_home

        self.logdir = os.path.join(ETSConfig.application_home, 'log')
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)

    def _setup_logging(self):
        """ Initialize logger. """
        pass

    def _run(self):
        """ Private shadow method that does the actual work

        Subclasses may sometimes need to override this.
        """
        # Fire a notification that the app is running.  This is guaranteed to
        # happen after all initialization has occurred and the event loop has
        # started.
        self.gui.set_trait_later(self, 'application_initialized',
                                 ApplicationEvent(application=self))

        # start the GUI - script blocks here
        self.gui.start_event_loop()

    def _prepare_exit(self):
        """ Do any application-level state saving and clean-up """
        pass

    def _reset_logger(self):
        """ Reset logger to default WARNING level and remove all handlers.
        """
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)

        def clear_handlers(logger):
            """ Remove all handlers from the given logger. """
            for handler in logger.handlers[::-1]:
                if hasattr(handler, 'close'):
                    handler.close()
                logger.removeHandler(handler)

        clear_handlers(logger)

    # Trait initializers -----------------------------------------------------

    def _gui_default(self):
        from pyface.api import GUI

        return GUI(splash_screen=self.splash_screen)

    def _undo_manager_default(self):
        from apptools.undo.api import UndoManager

        return UndoManager()

    def _get_active_task(self):
        if self.active_window is not None:
            return self.active_window.active_task
        else:
            return None
