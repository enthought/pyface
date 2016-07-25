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
import os
import logging
import sys

from traits.api import Bool, Directory, Event, HasStrictTraits, Instance, Str


logger = logging.getLogger(__name__)


class ApplicationEvent(HasStrictTraits):
    """ An event associated with an application """

    #: The application that the event happened to.
    application = Instance('BaseApplication')

    #: The type of application event.
    event_type = Str


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
    company = Str('Enthought')

    # Infrastructure ----------------------------------------------------------

    # The application's globally unique identifier.
    id = Str

    #: Application home directory (for preferences, logging, etc.)
    home = Directory

    #: User data directory (for user files, projects, etc)
    user_data = Directory

    # Application lifecycle events --------------------------------------------

    #: Fired when the application is starting. Called immediately before the
    #: start method is run.
    starting = Event(ApplicationEvent)

    #: Upon successful completion of the start method.
    started = Event(ApplicationEvent)

    #: Fired after the GUI event loop has been started during the run method.
    application_initialized = Event(ApplicationEvent)

    #: Fired when the application is starting. Called immediately before the
    #: start method is run.
    stopping = Event(ApplicationEvent)

    #: Upon successful completion of the stop method.
    stopped = Event(ApplicationEvent)

    # Protected interface -----------------------------------------------------

    #: Flag if the exiting of the application was explicitely requested by user
    # An 'explicit' exit is when the 'exit' method is called.
    # An 'implicit' exit is when the user closes the last open window.
    _explicit_exit = Bool(False)

    # Application lifecycle methods -------------------------------------------

    def __init__(self, **traits):
        """ Initialize the application """
        super(BaseApplication, self).__init__(**traits)

        # perform basic initialization before we can do anything
        self.init()

    def init(self):
        """ Perform basic application configuration

        In a full application, this includes setting up the application's home
        directory, setting up basic logging, handling command-line options and
        setting user preferences.
        """
        logger.info('---- Application configuration ----')

        # install our own exception hook for unhandled exceptions
        sys.excepthook = self._excepthook
        logger.debug('Exception hook installed')

        # make sure we have a home directory
        self._initialize_application_home()

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
        """ Run the application """

        # Start up the application.
        self.starting = ApplicationEvent(application=self,
                                         event_type='starting')
        started = self.start()
        if started:
            logger.info('---- Application started ----')
            self.started = ApplicationEvent(application=self,
                                            event_type='started')

            self._run()

            # We have finished running, so shut the application down.
            self.stopping = ApplicationEvent(application=self,
                                             event_type='stopping')
            stopped = self.stop()
            if stopped:
                self.stopped = ApplicationEvent(application=self,
                                                event_type='stopped')
                logger.info('---- Application stopped ----')

                # exit normally
                sys.exit()

        # exit with an error
        sys.exit(1)

    def exit(self, force=False):
        """ Exits the application.

        This method handles a request to shut down the application by the user,
        eg. from a menu.  If force is False, the application can potentially
        veto the close event, leaving the application in the state that it was
        before the exit method was called.

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
        logger.info('---- Application exit started ----')
        self._explicit_exit = True
        try:
            if not force:
                if not self._can_exit():
                    logger.info('---- Application exit vetoed ----')
                    return False
            self._prepare_exit()
        finally:
            self._explicit_exit = False
        self._exit()
        logger.info('---- Application exit successful ----')
        return True

    # -------------------------------------------------------------------------
    # Private interface
    # -------------------------------------------------------------------------

    # Initialization methods --------------------------------------------------

    def _initialize_application_home(self):
        """ Setup the home directory for the application where logs, preference
        files and other config files will be stored.
        """
        from traits.etsconfig.etsconfig import ETSConfig

        if self.id:
            ETSConfig.application_home = os.path.join(
                ETSConfig.application_data, self.id)
            logger.debug('Set application home to {}'.format(
                repr(ETSConfig.application_home)))
        else:
            # use the application home directory as the id
            self.id = ETSConfig._get_application_dirname()
            logger.info('Set application id to {}'.format(repr(self.id)))

        # Make sure it exists!
        if not os.path.exists(ETSConfig.application_home):
            logger.info('Application home directory does not exist, creating')
            os.makedirs(ETSConfig.application_home)

    # Main method -------------------------------------------------------------

    def _run(self):
        """ Actual implementation of running the application

        This should be completely overriden by applications which want to
        actually do something.  Usually this method starts an event loop and
        blocks, but for command-line applications this could be where the
        main application logic is called from.
        """
        # Fire a notification that the app is running.  If the app has an
        # event loop (eg. a GUI, Tornado web app, etc.) then the
        # should be fired _after_ the event loop starts using an appropriate
        # callback (eg. gui.set_trait_later).
        self.application_initialized = ApplicationEvent(application=self)

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
            sys.exit(1)

    # Destruction methods -----------------------------------------------------

    def _can_exit(self):
        """ Is exit vetoed by anything?

        Returns
        -------
        can_exit : bool
            Return True if exit is OK, False if something vetoes the exit.
        """
        return True

    def _prepare_exit(self):
        """ Do any application-level state saving and clean-up """
        pass

    def _exit(self):
        """ Shut down the application

        This is where application event loops and similar should be shut down.
        """
        # invoke a normal exit from the application
        sys.exit()

    # Traits defaults ---------------------------------------------------------

    def _home_default(self):
        """ Default home comes from ETSConfig. """
        from traits.etsconfig.etsconfig import ETSConfig
        return ETSConfig.application_home
