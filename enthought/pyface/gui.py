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
""" The GUI for a Pyface application. """


# Standard library imports.
import logging
from os.path import join

# Enthought library imports.
from enthought.etsconfig.api import ETSConfig
from enthought.io.api import File
from enthought.traits.api import HasTraits, Bool, Str
from enthought.util.api import deprecated

# Local imports.
from system_metrics import SystemMetrics
from toolkit import patch_toolkit, toolkit


# Logging.
logger = logging.getLogger(__name__)


class GUI(HasTraits):
    """ The GUI for a Pyface application. """

    __tko__ = 'GUI'

    #### 'GUI' interface ######################################################

    # Is the GUI busy (i.e. should the busy cursor, often an hourglass, be
    # displayed)?
    busy = Bool(False)

    # Has the GUI's event loop been started?
    started = Bool(False)

    # A directory on the local file system that we can read and write to at
    # will. This is used to persist layout information etc.
    state_location = Str

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, splash_screen=None):
        """ Initialises a new GUI. """

        patch_toolkit(self)

        # The (optional) splash screen.
        self._splash_screen = splash_screen

        if toolkit().name == 'wx':
            # fixme: For now, we have disabled splash screens on non-Windows
            # platforms as on Linux they cause the application to hang when
            # they are supposed to close (allegedly, this is for applications
            # that use the workbench plugin).
            import sys

            if sys.platform != 'win32':
                logger.warn('splash screen disabled on non-Windows platforms')
                self._splash_screen = None

        if self._splash_screen is not None:
            self._splash_screen.open()

        # The system metrics.
        self.system_metrics = SystemMetrics()

        return

    ###########################################################################
    # 'GUI' CLASS interface.
    ###########################################################################

    # fixme: This method returns a toolit dependent value. We should either:-
    #
    # a) Not return the value!
    # b) Create an abstract class to represent the value along with concrete
    #    implementations for each toolkit.
    def invoke_after(cls, millisecs, callable, *args, **kw):
        """ Call a callable after a specific delay in the main GUI thread.

        Returns an object with which the return value of the callable can be
        obtained.

        """

        return cls._tk_gui_future_call(millisecs, callable, *args, **kw)

    invoke_after = classmethod(invoke_after)

    def invoke_later(cls, callable, *args, **kw):
        """ Call a callable in the main GUI thread. """

        cls._tk_gui_call_after(callable, *args, **kw)

        return

    invoke_later = classmethod(invoke_later)

    # fixme: This method returns a toolit dependent value. We should either:-
    #
    # a) Not return the value!
    # b) Create an abstract class to represent the value along with concrete
    #    implementations for each toolkit.
    def set_trait_after(cls, millisecs, obj, trait_name, new):
        """ Sets a trait after a specific delay in the main GUI thread.

        Returns an object with which the return value of the callable can be
        obtained.

        """

        return cls._tk_gui_future_call(millisecs, setattr, obj, trait_name,new)

    set_trait_after = classmethod(set_trait_after)

    def set_trait_later(cls, obj, trait_name, new):
        """ Sets a trait in the main GUI thread. """

        cls._tk_gui_call_after(setattr, obj, trait_name, new)

        return

    set_trait_later = classmethod(set_trait_later)

    ###########################################################################
    # 'GUI' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _state_location_default(self):
        """ Trait initializer. """

        state_location = join(ETSConfig.application_home, 'pyface', toolkit().name)
        try:
            File(state_location).create_folders()

        # We get a 'ValueError' if the folders already exist.
        except ValueError:
            pass

        logger.debug('GUI state location is [%s]', state_location)

        return state_location

    #### Methods ##############################################################

    def start_event_loop(self):
        """ Start the GUI event loop. """

        if self._splash_screen is not None:
            self._splash_screen.close()

        # Make sure that we only set the 'started' trait after the main loop
        # has really started.
        self.set_trait_after(10, self, "started", True)

        logger.debug("---------- starting GUI event loop ----------")
        self._tk_gui_enter_event_loop()

        self.started = False

        return

    def stop_event_loop(self):
        """ Stop the GUI event loop. """

        logger.debug("---------- stopping GUI event loop ----------")
        self._tk_gui_exit_event_loop()

        return

    #### Deprecated ###########################################################

    # FIXME v3: Remove.
    @deprecated('use gui.start_event_loop')
    def event_loop(self):
        """ Start the GUI event loop. """

        self.start_event_loop()

        return

    ###########################################################################
    # Private 'GUI' interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _busy_changed(self, new):
        """ The busy trait change handler. """

        self._tk_gui_busy_cursor(new)

        return

    ###########################################################################
    # 'GUI' toolkit interface.
    ###########################################################################

    def _tk_gui_enter_event_loop(self):
        """ Enter the GUI event loop.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_gui_exit_event_loop(self):
        """ Exit the GUI event loop.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_gui_busy_cursor(self, show):
        """ Show or remove a busy cursor.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_gui_future_call(cls, millisecs, callable, *args, **kw):
        """ Call a callable after a specific delay in the main GUI thread.

        Returns an object with which the return value of the callable can be
        obtained.

        This must be reimplemented.
        """

        raise NotImplementedError

    _tk_gui_future_call = classmethod(_tk_gui_future_call)

    def _tk_gui_call_after(cls, callable, *args, **kw):
        """ Call a callable in the main GUI thread.

        This must be reimplemented.
        """

        raise NotImplementedError

    _tk_gui_call_after = classmethod(_tk_gui_call_after)

#### EOF ######################################################################
