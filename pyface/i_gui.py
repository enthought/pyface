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
""" The interface of a pyface GUI. """


# Standard library imports.
import logging
import os

# Enthought library imports.
from traits.etsconfig.api import ETSConfig
from traits.api import Bool, Interface, Unicode


# Logging.
logger = logging.getLogger(__name__)


class IGUI(Interface):
    """ The interface of a pyface GUI. """

    #### 'GUI' interface ######################################################

    # Is the GUI busy (i.e. should the busy cursor, often an hourglass, be
    # displayed)?
    busy = Bool(False)

    # Has the GUI's event loop been started?
    started = Bool(False)

    # A directory on the local file system that we can read and write to at
    # will.  This is used to persist layout information etc.  Note that
    # individual toolkits will have their own directory.
    state_location = Unicode

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, splash_screen=None):
        """ Initialise a new GUI.  splash_screen is an optional splash screen
        that will be displayed until the event loop is started.
        """

    ###########################################################################
    # 'GUI' class interface.
    ###########################################################################

    def allow_interrupt():
        """ Override the SIGINT handler to ensure the process can be
        interrupted. This prevents GUI toolkits from swallowing
        KeyboardInterrupt exceptions.

        Warning: do not call this method if you intend your application to be
        run interactively.
        """

    allow_interrupt = staticmethod(allow_interrupt)

    def invoke_after(cls, millisecs, callable, *args, **kw):
        """ Call a callable after a specific delay in the main GUI thread. """

    invoke_after = classmethod(invoke_after)

    def invoke_later(cls, callable, *args, **kw):
        """ Call a callable in the main GUI thread. """

    invoke_later = classmethod(invoke_later)

    def set_trait_after(cls, millisecs, obj, trait_name, new):
        """ Sets a trait after a specific delay in the main GUI thread. """

    set_trait_after = classmethod(set_trait_after)

    def set_trait_later(cls, obj, trait_name, new):
        """ Sets a trait in the main GUI thread. """

    set_trait_later = classmethod(set_trait_later)

    def process_events(allow_user_events=True):
        """ Process any pending GUI events. If allow_user_events is False then
        user generated events are not processed.
        """

    process_events = staticmethod(process_events)

    def set_busy(busy=True):
        """Specify if the GUI is busy.  If `True` is passed, the
        cursor is set to a 'busy' cursor.  Passing `False` will reset
        the cursor to the default.
        """

    set_busy = staticmethod(set_busy)

    ###########################################################################
    # 'GUI' interface.
    ###########################################################################

    def start_event_loop(self):
        """ Start the GUI event loop. """

    def stop_event_loop(self):
        """ Stop the GUI event loop. """


class MGUI(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IGUI interface.

    Implements: _default_state_location()
    """

    def allow_interrupt():
        """ Override the SIGINT handler to ensure the process can be
        interrupted. This prevents GUI toolkits from swallowing
        KeyboardInterrupt exceptions.
        """
        import signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    allow_interrupt = staticmethod(allow_interrupt)

    def _default_state_location(self):
        """ Return the default state location. """

        state_location = os.path.join(ETSConfig.application_home, 'pyface', ETSConfig.toolkit)

        if not os.path.exists(state_location):
            os.makedirs(state_location)

        logger.debug('GUI state location is <%s>', state_location)

        return state_location
