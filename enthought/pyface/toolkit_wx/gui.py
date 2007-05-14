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

# System library imports.
import sys

# Major package imports.
import wx


class GUI_wx(object):
    """ The GUI monkey patch for wx. """

    ###########################################################################
    # 'GUI' toolkit interface.
    ###########################################################################

    def _tk_gui_enter_event_loop(self):
        """ Enter the GUI event loop. """

        # A hack to force menus to appear for applications run on Mac OS X.
        if sys.platform == 'darwin':
            def _mac_os_x_hack():
                f = wx.Frame(None, -1)
                f.Show(True)
                f.Close()
            self.invoke_later(_mac_os_x_hack)

        wx.GetApp().MainLoop()

        return

    def _tk_gui_exit_event_loop(self):
        """ Exit the GUI event loop. """

        wx.GetApp().ExitMainLoop()

        return

    def _tk_gui_busy_cursor(self, show):
        """ Show or remove a busy cursor. """

        if show:
            self._wx_cursor = wx.BusyCursor()
        else:
            del self._wx_cursor

        return
    
    def _tk_gui_future_call(cls, millisecs, callable, *args, **kw):
        """ Call a callable after a specific delay in the main GUI thread.

        Returns an object with which the return value of the callable can be
        obtained.
        """

        return wx.FutureCall(millisecs, callable, *args, **kw)

    _tk_gui_future_call = classmethod(_tk_gui_future_call)

    def _tk_gui_call_after(cls, callable, *args, **kw):
        """ Call a callable in the main GUI thread. """

        wx.CallAfter(callable, *args, **kw)

        return

    _tk_gui_call_after = classmethod(_tk_gui_call_after)

#### EOF ######################################################################
