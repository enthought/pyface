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
""" A clickable/draggable widget containing an image. """
from __future__ import absolute_import

# Major package imports.
import wx

# Enthought library imports.
from traits.api import Any, Bool, Event

# Local imports.
from .widget import Widget


class ImageWidget(Widget):
    """ A clickable/draggable widget containing an image. """

    #### 'ImageWidget' interface ##############################################

    # The bitmap.
    bitmap = Any

    # Is the widget selected?
    selected = Bool(False)

    #### Events ####

    # A key was pressed while the tree is in focus.
    key_pressed = Event

    # A node has been activated (ie. double-clicked).
    node_activated = Event

    # A drag operation was started on a node.
    node_begin_drag = Event

    # A (non-leaf) node has been collapsed.
    node_collapsed = Event

    # A (non-leaf) node has been expanded.
    node_expanded = Event

    # A left-click occurred on a node.
    node_left_clicked = Event

    # A right-click occurred on a node.
    node_right_clicked = Event

    #### Private interface ####################################################

    _selected = Any

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__ (self, parent, **traits):
        """ Creates a new widget. """

        # Base class constructors.
        super(ImageWidget, self).__init__(**traits)

        # Add some padding around the image.
        size = (self.bitmap.GetWidth() + 10, self.bitmap.GetHeight() + 10)

        # Create the toolkit-specific control.
        self.control = wx.Window(parent, -1, size=size)
        self.control.__tag__ = 'hack'

        self._mouse_over  = False
        self._button_down = False

        # Set up mouse event handlers:
        self.control.Bind(wx.EVT_ENTER_WINDOW, self._on_enter_window)
        self.control.Bind(wx.EVT_LEAVE_WINDOW, self._on_leave_window)
        self.control.Bind(wx.EVT_LEFT_DCLICK, self._on_left_dclick)
        self.control.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.control.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.control.Bind(wx.EVT_PAINT, self._on_paint)

        # Pens used to draw the 'selection' marker:
        # ZZZ: Make these class instances when moved to the wx toolkit code.
        self._selectedPenDark = wx.Pen(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW), 1,
            wx.PENSTYLE_SOLID
        )

        self._selectedPenLight = wx.Pen(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DHIGHLIGHT), 1,
            wx.PENSTYLE_SOLID
        )

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait event handlers #################################################

    def _bitmap_changed(self, bitmap):
        """ Called when the widget's bitmap is changed. """

        if self.control is not None:
            self.control.Refresh()

        return

    def _selected_changed(self, selected):
        """ Called when the selected state of the widget is changed. """

        if selected:
            for control in self.GetParent().GetChildren():
                if hasattr(control, '__tag__'):
                    if control.Selected():
                      control.Selected(False)
                      break

                self.Refresh()

        return

    #### wx event handlers ####################################################

    def _on_enter_window(self, event):
        """ Called when the mouse enters the widget. """

        if self._selected is not None:
            self._mouse_over = True
            self.Refresh()

        return

    def _on_leave_window(self, event):
        """ Called when the mouse leaves the widget. """

        if self._mouse_over:
            self._mouse_over = False
            self.Refresh()

        return

    def _on_left_dclick(self, event):
        """ Called when the left mouse button is double-clicked. """

        #print 'left dclick'

        event.Skip()

        return

    def _on_left_down ( self, event = None ):
        """ Called when the left mouse button goes down on the widget. """

        #print 'left down'

        if self._selected is not None:
            self.CaptureMouse()
            self._button_down = True
            self.Refresh()

        event.Skip()

        return

    def _on_left_up ( self, event = None ):
        """ Called when the left mouse button goes up on the widget. """

        #print 'left up'

        need_refresh = self._button_down
        if need_refresh:
            self.ReleaseMouse()
            self._button_down = False

        if self._selected is not None:
            wdx, wdy = self.GetClientSizeTuple()
            x        = event.GetX()
            y        = event.GetY()
            if (0 <= x < wdx) and (0 <= y < wdy):
                if self._selected != -1:
                    self.Selected( True )
                elif need_refresh:
                    self.Refresh()

                return

        if need_refresh:
            self.Refresh()

        event.Skip()

        return

    def _on_paint ( self, event = None ):
        """ Called when the widget needs repainting. """

        wdc      = wx.PaintDC( self.control )
        wdx, wdy = self.control.GetClientSizeTuple()
        bitmap   = self.bitmap
        bdx      = bitmap.GetWidth()
        bdy      = bitmap.GetHeight()
        wdc.DrawBitmap( bitmap, (wdx - bdx) / 2, (wdy - bdy) / 2, True )

        pens = [ self._selectedPenLight, self._selectedPenDark ]
        bd   = self._button_down
        if self._mouse_over:
            wdc.SetBrush( wx.TRANSPARENT_BRUSH )
            wdc.SetPen( pens[ bd ] )
            wdc.DrawLine( 0, 0, wdx, 0 )
            wdc.DrawLine( 0, 1, 0, wdy )
            wdc.SetPen( pens[ 1 - bd ] )
            wdc.DrawLine( wdx - 1, 1, wdx - 1, wdy )
            wdc.DrawLine( 1, wdy - 1, wdx - 1, wdy - 1 )

        if self._selected == True:
            wdc.SetBrush( wx.TRANSPARENT_BRUSH )
            wdc.SetPen( pens[ bd ] )
            wdc.DrawLine( 1, 1, wdx - 1, 1 )
            wdc.DrawLine( 1, 1, 1, wdy - 1 )
            wdc.DrawLine( 2, 2, wdx - 2, 2 )
            wdc.DrawLine( 2, 2, 2, wdy - 2 )
            wdc.SetPen( pens[ 1 - bd ] )
            wdc.DrawLine( wdx - 2, 2, wdx - 2, wdy - 1 )
            wdc.DrawLine( 2, wdy - 2, wdx - 2, wdy - 2 )
            wdc.DrawLine( wdx - 3, 3, wdx - 3, wdy - 2 )
            wdc.DrawLine( 3, wdy - 3, wdx - 3, wdy - 3 )

        return

#### EOF ######################################################################
