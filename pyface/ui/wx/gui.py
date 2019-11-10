#------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: Enthought, Inc.
#
#------------------------------------------------------------------------------

""" Enthought pyface package component
"""

# Standard library imports.
import logging
import sys

# Major package imports.
import wx

# Enthought library imports.
from traits.api import Bool, HasTraits, Property, provides, Unicode
from pyface.util.guisupport import start_event_loop_wx

# Local imports.
from pyface.i_gui import IGUI, MGUI


# Logging.
logger = logging.getLogger(__name__)


@provides(IGUI)
class GUI(MGUI, HasTraits):


    #### 'GUI' interface ######################################################

    #: A reference to the toolkit application singleton.
    app = Property

    #: Is the GUI busy (i.e. should the busy cursor, often an hourglass, be
    #: displayed)?
    busy = Bool(False)

    #: Has the GUI's event loop been started?
    started = Bool(False)

    #: Whether the GUI quits on last window close.
    quit_on_last_window_close = Property(Bool)

    #: A directory on the local file system that we can read and write to at
    #: will.  This is used to persist layout information etc.  Note that
    #: individual toolkits will have their own directory.
    state_location = Unicode

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, splash_screen=None):
        # Display the (optional) splash screen.
        self._splash_screen = splash_screen

        if self._splash_screen is not None:
            self._splash_screen.open()

    ###########################################################################
    # 'GUI' class interface.
    ###########################################################################

    @classmethod
    def invoke_after(cls, millisecs, callable, *args, **kw):
        wx.CallLater(millisecs, callable, *args, **kw)

    @classmethod
    def invoke_later(cls, callable, *args, **kw):
        wx.CallAfter(callable, *args, **kw)

    @classmethod
    def set_trait_after(cls, millisecs, obj, trait_name, new):
        wx.CallLater(millisecs, setattr, obj, trait_name, new)

    @classmethod
    def set_trait_later(cls, obj, trait_name, new):
        wx.CallAfter(setattr, obj, trait_name, new)

    @staticmethod
    def process_events(allow_user_events=True):
        if allow_user_events:
            wx.GetApp().Yield(True)
        else:
            wx.SafeYield()

    @staticmethod
    def set_busy(busy=True):
        if busy:
            GUI._cursor = wx.BusyCursor()
        else:
            GUI._cursor = None

    ###########################################################################
    # 'GUI' interface.
    ###########################################################################

    def start_event_loop(self):
        """ Start the GUI event loop. """

        if self._splash_screen is not None:
            self._splash_screen.close()

        if self.app.IsMainLoopRunning():
            raise RuntimeError('double call')

        # Make sure that we only set the 'started' trait after the main loop
        # has really started.
        self.set_trait_after(10, self, "started", True)

        # A hack to force menus to appear for applications run on Mac OS X.
        if sys.platform == 'darwin' and not self.top_level_windows():
            def _mac_os_x_hack():
                f = wx.Frame(None, -1)
                f.Show(True)
                f.Close()
            self.invoke_later(_mac_os_x_hack)

        logger.debug("---------- starting GUI event loop ----------")
        self.app.MainLoop()

        self.started = False

    def stop_event_loop(self):
        """ Stop the GUI event loop. """

        logger.debug("---------- stopping GUI event loop ----------")
        self.app.ExitMainLoop()
        # XXX this feels wrong, but seems to be needed in some cases
        self.process_events(False)

    def clear_event_queue(self):
        self.app.DeletePendingEvents()

    def top_level_windows(self):
        return wx.GetTopLevelWindows()

    def close_all(self, force=False):
        for window in self.top_level_windows():
            closed = window.Close(force)
            if not closed:
                break

    ###########################################################################
    # Trait handlers.
    ###########################################################################

    def _state_location_default(self):
        """ The default state location handler. """

        return self._default_state_location()

    def _busy_changed(self, new):
        """ The busy trait change handler. """

        if new:
            self._wx_cursor = wx.BusyCursor()
        else:
            del self._wx_cursor

        return

    # Property handlers -----------------------------------------------------

    def _get_app(self):
        app = wx.GetApp()
        if app is None:
            app = wx.App()
        return app

    def _get_quit_on_last_window_close(self):
        return self.app.GetExitOnFrameDelete()

    def _set_quit_on_last_window_close(self, value):
        return self.app.SetExitOnFrameDelete(value)
