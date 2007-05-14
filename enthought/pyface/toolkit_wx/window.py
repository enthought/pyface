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

# Major package imports.
import wx

# Enthought library imports.
from enthought.logger import logger
from enthought.pyface.api import KeyPressedEvent


class Window_wx(object):
    """ The Window monkey patch for wx. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create and return the toolkit specific control that represents the
        window.
        """

        control = wx.Frame(
            parent, -1, self.title, size=self.size, pos=self.position
        )
        
        return control
            
    ###########################################################################
    # 'Window' toolkit interface.
    ###########################################################################

    def _tk_window_add_event_listeners(self, control):
        """ Adds any event listeners required by the window. """

        # Frame events.  Note that the control argument is ignored.
        wx.EVT_ACTIVATE(self.control, self._wx_on_activate)
        wx.EVT_CLOSE(self.control, self._wx_on_close)
        wx.EVT_SIZE(self.control, self._wx_on_control_size)
        wx.EVT_MOVE(self.control, self._wx_on_control_move)
        wx.EVT_CHAR(self.control, self._wx_on_char)

        return
    
    def _tk_window_create_contents(self, parent):
        """ Create and return the (optional) window contents. """

        panel = wx.Panel(parent, -1)
        panel.SetSize((500, 400))
        panel.SetBackgroundColour('blue')

        return panel

    def _tk_window_layout_contents(self, content):
        """ Layout the window contents. """

        self.sizer.Add(content, 1, wx.ALL | wx.EXPAND)

        return

    def _tk_window_layout_control(self):
        """ Layout the window control. """

        self.main_sizer.Fit(self.control)

        return

    def _tk_window_refresh(self):
        """ Workaround for VTK render window sizing bug. """

        self.control.SendSizeEvent()

        return

    def _tk_window_set_position(self, position):
        """ Set the window's position. """

        self.control.SetPosition(position)

        return

    def _tk_window_set_size(self, size):
        """ Set the window's size. """

        self.control.SetSize(size)

        return

    def _tk_window_set_title(self, title):
        """ Set the window's title. """

        self.control.SetTitle(title)

        return

    def _tk_window_set_visible(self, visible):
        """ Show or hide the window. """

        self.control.Show(visible)

        return
        
    #### wx event handlers ####################################################

    def _wx_on_activate(self, event):
        """ Called when the frame is being activated or deactivated. """

        # Trait notification.
        if event.GetActive():
            self.activated = self

        else:
            self.deactivated = self

        return

    def _wx_on_close(self, event):
        """ Called when the frame is being closed. """

        logger.debug('window [%s] closed by user', self)
        
        self.close()

        return
    
    def _wx_on_control_move(self, event):
        """ Called when the window is resized. """

        # Get the real position and set the trait without performing
        # notification.

        # WXBUG - From the API documentation you would think that you could
        # call event.GetPosition directly, but that would be wrong.  The pixel
        # reported by that call is the pixel just below the window menu and
        # just right of the Windows-drawn border.
        self._position = event.GetEventObject().GetPositionTuple()
        
        event.Skip()

        return
        
    def _wx_on_control_size(self, event):
        """ Called when the window is resized. """

        # Get the new size and set the shadow trait without performing
        # notification.
        wxsize = event.GetSize()
        self._size = (wxsize.GetWidth(), wxsize.GetHeight())

        event.Skip()

        return

    def _wx_on_char(self, event):
        """ Called when a key is pressed when the tree has focus. """

        self.key_pressed = KeyPressedEvent(
            alt_down     = event.m_altDown == 1,
            control_down = event.m_controlDown == 1,
            shift_down   = event.m_shiftDown == 1,
            key_code     = event.m_keyCode,
            event        = event
        )
        
        event.Skip()
        
        return

#### EOF ######################################################################
