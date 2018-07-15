# Copyright (c) 2014-2017 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

"""
This module defines the :py:class:`BaseApplication` class for Pyface, Tasks
and similar applications.  Although the primary use cases are for GUI
applications, the :py:class:`BaseApplication` class does not have any explicit
dependency on GUI code, and can be used for CLI or server applications.

Usual usage is to subclass :py:class:`BaseApplication` overriding at least the
:py:method:`BaseApplication._run` method, but usually the
:py:method:`BaseApplication.start` and :py:method:`BaseApplication.stop`
methods as well.

However the class can be used as-is by listening to the
:py:attr:`BaseApplication.application_initialized` event and performing
appropriate work there::

    def do_work():
        print("Hello world")

    app = BaseApplication()
    app.on_trait_change(do_work, 'application_initialized')

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging
import os
import sys

from traits.api import (
    Callable, Directory, Event, HasStrictTraits, Instance, List,
    ReadOnly, Str, Vetoable, VetoableEvent
)

logger = logging.getLogger(__name__)


class ApplicationException(Exception):
    """ Exception subclass for Application-centric exceptions """
    pass


class ApplicationExit(ApplicationException):
    """ Exception which indicates application should try to exit.

    If no arguments, then assumed to be a normal exit, otherwise the arguments
    give information about the problem.
    """
    pass


class ApplicationEvent(HasStrictTraits):
    """ An event associated with an application """

    #: The application that the event happened to.
    application = ReadOnly

    #: The type of application event.
    event_type = ReadOnly


class BaseApplication(HasStrictTraits):
    """ A base class for applications.

    This class handles the basic lifecycle of an application and a few
    fundamental facilities.  It is suitable as a base for any application,
    not just GUI applications.
    """

    # -------------------------------------------------------------------------
    # 'BaseApplication' interface
    # -------------------------------------------------------------------------

    # Branding ----------------------------------------------------------------

    #: Human-readable application name
    name = Str('Default Application')

    #: Human-readable company name
    company = Str

    # Infrastructure ----------------------------------------------------------

    # The application's globally unique identifier.
    id = Str

    #: Application home directory (for preferences, logging, etc.)
    home = Directory

    #: User data directory (for user files, projects, etc)
    user_data = Directory

    # Application lifecycle --------------------------------------------------

    #: Fired when the application is starting. Called immediately before the
    #: start method is run.
    starting = Event(Instance(ApplicationEvent))

    #: Upon successful completion of the start method.
    started = Event(Instance(ApplicationEvent))

    #: Fired after the GUI event loop has been started during the run method.
    application_initialized = Event(Instance(ApplicationEvent))

    #: Fired when the application is starting. Called immediately before the
    #: stop method is run.
    exiting = VetoableEvent

    #: Fired when the application is starting. Called immediately before the
    #: stop method is run.
    stopping = Event(Instance(ApplicationEvent))

    #: Upon successful completion of the stop method.
    stopped = Event(Instance(ApplicationEvent))

    # Private interface ------------------------------------------------------

    _old_excepthook = Callable

    # Application lifecycle methods -------------------------------------------

    def start(self):
        """ Start the application, setting up things that are required

        Subclasses should open at least one ApplicationWindow or subclass in
        their start method, and should call the superclass start() method
        before doing any work themselves.
        """
        logger.info('---- Application starting ----')
        return True

    def stop(self):
        """ Stop the application, cleanly releasing resources if possible. """
        logger.info('---- Application stopping ----')
        return True

    def run(self):
        """ Run the application

        Return
        ------
        status : bool
            Whether or not the application ran normally
        """
        run = stopped = False

        # Start up the application.
        self._fire_application_event('starting')
        started = self.start()
        if started:

            logger.info('---- Application started ----')
            self._fire_application_event('started')

            try:
                run = self._run()
            except ApplicationExit as exc:
                if exc.args == ():
                    logger.info("---- ApplicationExit raised ----")
                else:
                    logger.exception("---- ApplicationExit raised ----")
                run = (exc.args == ())
            finally:
                # Try to shut the application down.
                self._fire_application_event('stopping')
                stopped = self.stop()
                if stopped:
                    self._fire_application_event('stopped')
                    logger.info('---- Application stopped ----')

        return started and run and stopped

    def exit(self, force=False):
        """ Exits the application.

        This method handles a request to shut down the application by the user,
        eg. from a menu.  If force is False, the application can potentially
        veto the close event, leaving the application in the state that it was
        before the exit method was called.

        Parameters
        ----------
        force : bool, optional (default False)
            If set, windows will receive no closing events and will be
            destroyed unconditionally. This can be useful for reliably tearing
            down regression tests, but should be used with caution.

        Raises
        ------
        ApplicationExit
            Some subclasses may trigger the exit by raising ApplicationExit.
        """
        logger.info('---- Application exit started ----')
        if force or self._can_exit():
            try:
                self._prepare_exit()
            except Exception:
                logger.exception("Error preparing for application exit")
            finally:
                logger.info('---- Application exit ----')
                self._exit()
        else:
            logger.info('---- Application exit vetoed ----')

    # Initialization utilities -----------------------------------------------

    def initialize_application_home(self):
        """ Set up the home directory for the application

        This is where logs, preference files and other config files will be
        stored.
        """
        if not os.path.exists(self.home):
            logger.info('Application home directory does not exist, creating')
            os.makedirs(self.home)

    def install_excepthook(self):
        """ Install an exception hook to catch unhandled exceptions

        This permits applications to do things like catch and display an error
        dialog when something unexpectedly goes wrong.
        """
        self._old_excepthook = sys.excepthook
        sys.excepthook = self._excepthook
        logger.debug('Exception hook installed')

    # Teardown utilities ------------------------------------------------------

    def reset_excepthook(self):
        """ Install an exception hook to catch unhandled exceptions

        This permits applications to do things like catch and display an error
        dialog when something unexpectedly goes wrong.
        """
        sys.excepthook = self._old_excepthook
        self._old_excepthook = None
        logger.debug('Exception hook reset')

    # -------------------------------------------------------------------------
    # Private interface
    # -------------------------------------------------------------------------

    # Main method -------------------------------------------------------------

    def _run(self):
        """ Actual implementation of running the application

        This should be completely overriden by applications which want to
        actually do something.  Usually this method starts an event loop and
        blocks, but for command-line applications this could be where the
        main application logic is called from.
        """
        # Fire a notification that the app is running.  If the app has an
        # event loop (eg. a GUI, Tornado web app, etc.) then this should be
        # fired _after_ the event loop starts using an appropriate callback
        # (eg. gui.set_trait_later).
        self._fire_application_event('application_initialized')
        return True

    # Utilities ---------------------------------------------------------------

    def _fire_application_event(self, event_type):
        event = ApplicationEvent(application=self, event_type=event_type)
        setattr(self, event_type, event)

    # Exception handling ------------------------------------------------------

    def _excepthook(self, type, value, traceback):
        """ Handle any exceptions not explicitly caught

        This can be overridden by GUI applications to display an appropriate
        error dialog, if possible.  Keep in mind that the application can be
        in an arbitrary state when this is called, so anything provided by the
        user should fail over to the standard excepthook.
        """
        try:
            # try to log the exception, could fail eg. if disk full
            logger.exception(value)
        finally:
            # just use standard excepthook in this app
            sys.__excepthook__(type, value, traceback)
            # die, in an error state
            raise SystemExit("Can't log exception in application excepthook.")

    # Destruction methods -----------------------------------------------------

    def _can_exit(self):
        """ Is exit vetoed by anything?

        The default behaviour is to fire the :py:attr:`exiting` event and check
        to see if any listeners veto.  Subclasses may wish to override to
        perform additional checks.

        Returns
        -------
        can_exit : bool
            Return True if exit is OK, False if something vetoes the exit.
        """
        self.exiting = event = Vetoable()
        return not event.veto

    def _prepare_exit(self):
        """ Do any application-level state saving and clean-up

        Subclasses should override this method.
        """
        pass

    def _exit(self):
        """ Shut down the application

        This is where application event loops and similar should be shut down.
        """
        # invoke a normal exit from the application
        raise ApplicationExit()

    # Traits defaults ---------------------------------------------------------

    def _id_default(self):
        """ Use the application's directory as the id """
        from traits.etsconfig.etsconfig import ETSConfig
        return ETSConfig._get_application_dirname()

    def _home_default(self):
        """ Default home comes from ETSConfig. """
        from traits.etsconfig.etsconfig import ETSConfig
        return os.path.join(ETSConfig.application_data, self.id)

    def _user_data_default(self):
        """ Default user_data comes from ETSConfig. """
        from traits.etsconfig.etsconfig import ETSConfig
        return ETSConfig.user_data

    def _company_default(self):
        """ Default company comes from ETSConfig. """
        from traits.etsconfig.etsconfig import ETSConfig
        return ETSConfig.company
