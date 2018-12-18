# Copyright (c) 2014-2018 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
This module defines the :py:class:`Application` class for Pyface, Tasks
and similar applications.  Although the primary use cases are for GUI
applications, the :py:class:`Application` class does not have any explicit
dependency on GUI code, and can be used for CLI or server applications.

Usual usage is to subclass :py:class:`Application`, overriding at least the
:py:method:`Application._run` method, but usually the
:py:method:`Application.start` and :py:method:`Application.stop`
methods as well.

However the class can be used as-is by listening to the
:py:attr:`Application.application_initialized` event and performing
appropriate work there::

    def do_work():
        print("Hello world")

    app = Application()
    app.on_trait_change(do_work, 'application_initialized')

"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
import logging
import os

from traits.api import (
    Directory, Event, HasStrictTraits, Instance, ReadOnly, Unicode, Vetoable,
    VetoableEvent
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


class Application(HasStrictTraits):
    """ A base class for applications.

    This class handles the basic lifecycle of an application and a few
    fundamental facilities.  It is suitable as a base for any application,
    not just GUI applications.
    """

    # 'Application' traits ----------------------------------------------------

    # Branding ----------------------------------------------------------------

    #: Human-readable application name
    name = Unicode('Pyface Application')

    #: Human-readable company name
    company = Unicode

    #: Human-readable description of the application
    description = Unicode

    # Infrastructure ---------------------------------------------------------

    #: The application's globally unique identifier.
    id = Unicode

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

    # -------------------------------------------------------------------------
    # Application interface
    # -------------------------------------------------------------------------

    # Application lifecycle methods ------------------------------------------

    def start(self):
        """ Start the application, setting up things that are required

        Subclasses should call the superclass start() method before doing any
        work themselves.
        """
        return True

    def stop(self):
        """ Stop the application, cleanly releasing resources if possible.

        Subclasses should call the superclass stop() method after doing any
        work themselves.
        """
        return True

    def run(self):
        """ Run the application.

        Return
        ------
        status : bool
            Whether or not the application ran normally
        """
        run = stopped = False

        # Start up the application.
        logger.info('---- Application starting ----')
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
                logger.info('---- Application stopping ----')
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

    def _description_default(self):
        """ Default description is the docstring of the application class. """
        from inspect import getdoc
        text = getdoc(self)
        return text
