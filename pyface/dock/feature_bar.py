#-------------------------------------------------------------------------------
#
#  Copyright (c) 2007, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: David C. Morrill
#  Date:   02/05/2007
#
#-------------------------------------------------------------------------------

""" Pyface 'FeatureBar' support.

    Defines the 'FeatureBar' class which displays and allows the user to
    interact with a set of DockWindowFeatures for a specified DockControl.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import wx

from traits.api \
    import HasPrivateTraits, Instance, Bool, Event, Color

from pyface.wx.drag_and_drop \
    import PythonDropTarget, PythonDropSource

from dock_sizer \
    import DockControl, FEATURE_EXTERNAL_DRAG

from ifeature_tool \
    import IFeatureTool

#-------------------------------------------------------------------------------
#  'FeatureBar' class:
#-------------------------------------------------------------------------------

class FeatureBar ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The wx.Window which is the parent for the FeatureBar:
    parent = Instance( wx.Window )

    # The DockControl whose features are being displayed:
    dock_control = Instance( DockControl )

    # The wx.Window being used for the FeatureBar:
    control = Instance( wx.Window )

    # Event posted when the user has completed using the FeatureBar:
    completed = Event

    # The background color for the FeatureBar:
    bg_color = Color( 0xDBEEF7, allow_none = True )

    # The border color for the FeatureBar:
    border_color = Color( 0X2583AF, allow_none = True )

    # Should the feature bar display horizontally (or vertically)?
    horizontal = Bool( True )

    #---------------------------------------------------------------------------
    #  Hides the feature bar:
    #---------------------------------------------------------------------------

    def hide ( self ):
        """ Hides the feature bar.
        """
        if self.control is not None:
            self.control.Hide()

    #---------------------------------------------------------------------------
    #  Shows the feature bar:
    #---------------------------------------------------------------------------

    def show ( self ):
        """ Shows the feature bar.
        """
        # Make sure all prerequisites are met:
        dock_control, parent = self.dock_control, self.parent
        if (dock_control is None) or (parent is None):
            return

        # Create the actual control (if needed):
        control = self.control
        if control is None:
            self.control = control = wx.Frame( None, -1, '',
                                               style = wx.BORDER_NONE )

            # Set up the 'erase background' event handler:
            wx.EVT_ERASE_BACKGROUND( control, self._erase_background )

            # Set up the 'paint' event handler:
            wx.EVT_PAINT( control, self._paint )

            # Set up mouse event handlers:
            wx.EVT_LEFT_DOWN(    control, self._left_down )
            wx.EVT_LEFT_UP(      control, self._left_up )
            wx.EVT_RIGHT_DOWN(   control, self._right_down )
            wx.EVT_RIGHT_UP(     control, self._right_up )
            wx.EVT_MOTION(       control, self._mouse_move )
            wx.EVT_ENTER_WINDOW( control, self._mouse_enter )

            control.SetDropTarget( PythonDropTarget( self ) )

        # Calculate the best size and position for the feature bar:
        size       = wx.Size( 32, 32 )
        width      = height = 0
        horizontal = self.horizontal
        for feature in dock_control.active_features:
            bitmap = feature.bitmap
            if bitmap is not None:
                if horizontal:
                    width += (bitmap.GetWidth() + 3)
                    height = max( height, bitmap.GetHeight() )
                else:
                    width   = max( width, bitmap.GetWidth() )
                    height += (bitmap.GetHeight() + 3)

        if width > 0:
            if horizontal:
                size = wx.Size( width + 5, height + 8 )
            else:
                size = wx.Size( width + 8, height + 5 )

        control.SetSize( size )
        px, py = parent.GetScreenPosition()
        fx, fy = dock_control.feature_popup_position
        control.SetPosition( wx.Point( px + fx, py + fy ) )
        control.Show()

    #-- Window Event Handlers --------------------------------------------------

    #---------------------------------------------------------------------------
    #  Handles repainting the window:
    #---------------------------------------------------------------------------

    def _paint ( self, event ):
        """ Handles repainting the window.
        """
        window = self.control
        dx, dy = window.GetSizeTuple()
        dc     = wx.PaintDC( window )

        # Draw the feature container:
        bg_color     = self.bg_color
        border_color = self.border_color
        if (bg_color is not None) or (border_color is not None):
            if border_color is None:
                dc.SetPen( wx.TRANSPARENT_PEN )
            else:
                dc.SetPen( wx.Pen( border_color, 1, wx.SOLID ) )
            if bg_color is None:
                dc.SetBrush( wx.TRANSPARENT_PEN )
            else:
                dc.SetBrush( wx.Brush( bg_color, wx.SOLID ) )
            dc.DrawRectangle( 0, 0, dx, dy )

        # Draw the feature icons:
        if self.horizontal:
            x = 4
            for feature in self.dock_control.active_features:
                bitmap = feature.bitmap
                if bitmap is not None:
                    dc.DrawBitmap( bitmap, x, 4, True )
                    x += (bitmap.GetWidth() + 3)
        else:
            y = 4
            for feature in self.dock_control.active_features:
                bitmap = feature.bitmap
                if bitmap is not None:
                    dc.DrawBitmap( bitmap, 4, y, True )
                    y += (bitmap.GetHeight() + 3)

    #---------------------------------------------------------------------------
    #  Handles erasing the window background:
    #---------------------------------------------------------------------------

    def _erase_background ( self, event ):
        """ Handles erasing the window background.
        """
        pass

    #---------------------------------------------------------------------------
    #  Handles the left mouse button being pressed:
    #---------------------------------------------------------------------------

    def _left_down ( self, event ):
        """ Handles the left mouse button being pressed.
        """
        self._feature  = self._feature_at( event )
        self._dragging = False
        self._xy       = ( event.GetX(), event.GetY() )
        #self.control.CaptureMouse()

    #---------------------------------------------------------------------------
    #  Handles the left mouse button being released:
    #---------------------------------------------------------------------------

    def _left_up ( self, event ):
        """ Handles the left mouse button being released.
        """
        #self.control.ReleaseMouse()
        self._dragging         = None
        feature, self._feature = self._feature, None
        if feature is not None:
            if feature is self._feature_at( event ):
                self.control.ReleaseMouse()
                self.completed = True
                feature._set_event( event )
                feature.click()

    #---------------------------------------------------------------------------
    #  Handles the right mouse button being pressed:
    #---------------------------------------------------------------------------

    def _right_down ( self, event ):
        """ Handles the right mouse button being pressed.
        """
        self._feature  = self._feature_at( event )
        self._dragging = False
        self._xy       = ( event.GetX(), event.GetY() )
        #self.control.CaptureMouse()

    #---------------------------------------------------------------------------
    #  Handles the right mouse button being released:
    #---------------------------------------------------------------------------

    def _right_up ( self, event ):
        """ Handles the right mouse button being released.
        """
        #self.control.ReleaseMouse()
        self._dragging         = None
        feature, self._feature = self._feature, None
        if feature is not None:
            if feature is self._feature_at( event ):
                self.control.ReleaseMouse()
                self.completed = True
                feature._set_event( event )
                feature.right_click()

    #---------------------------------------------------------------------------
    #  Handles the mouse moving over the window:
    #---------------------------------------------------------------------------

    def _mouse_move ( self, event ):
        """ Handles the mouse moving over the window.
        """
        # Update tooltips if no mouse button is currently pressed:
        if self._dragging is None:
            feature = self._feature_at( event )
            if feature is not self._tooltip_feature:
                self._tooltip_feature = feature
                tooltip = ''
                if feature is not None:
                    tooltip = feature.tooltip
                wx.ToolTip.Enable( False )
                wx.ToolTip.Enable( True )
                self.control.SetToolTip( wx.ToolTip( tooltip ) )

            # Check to see if the mouse has left the window, and mark it
            # completed if it has:
            x, y   = event.GetX(), event.GetY()
            dx, dy = self.control.GetSizeTuple()
            if (x < 0) or (y < 0) or (x >= dx) or (y >= dy):
                self.control.ReleaseMouse()
                self._tooltip_feature = None
                self.completed        = True

            return

        # Check to see if we are in 'drag mode' yet:
        if not self._dragging:
            x, y = self._xy
            if (abs( x - event.GetX() ) + abs( y - event.GetY() )) < 3:
                return

            self._dragging = True

            # Check to see if user is trying to drag a 'feature':
            feature = self._feature
            if feature is not None:
                feature._set_event( event )

                prefix = button = ''
                if event.RightIsDown():
                    button = 'right_'
                if event.ControlDown():
                    prefix = 'control_'
                elif event.AltDown():
                    prefix = 'alt_'
                elif event.ShiftDown():
                    prefix = 'shift_'

                object = getattr( feature, '%s%sdrag' % ( prefix, button ) )()
                if object is not None:
                    self.control.ReleaseMouse()
                    self._feature  = None
                    self.completed = True
                    self.dock_control.pre_drag_all( object )
                    PythonDropSource( self.control, object )
                    self.dock_control.post_drag_all()
                    self._dragging = None

    #---------------------------------------------------------------------------
    #  Handles the mouse entering the window:
    #---------------------------------------------------------------------------

    def _mouse_enter ( self, event ):
        """ Handles the mouse entering the window.
        """
        self.control.CaptureMouse()

#-- Drag and drop event handlers: ----------------------------------------------

    #---------------------------------------------------------------------------
    #  Handles a Python object being dropped on the control:
    #---------------------------------------------------------------------------

    def wx_dropped_on ( self, x, y, data, drag_result ):
        """ Handles a Python object being dropped on the window.
        """
        # Determine what, if any, feature the object was dropped on:
        feature = self._can_drop_on_feature( x, y, data )

        # Indicate use of the feature bar is complete:
        self.completed = True

        # Reset any drag state information:
        self.dock_control.post_drag( FEATURE_EXTERNAL_DRAG )

        # Check to see if the data was dropped on a feature or not:
        if feature is not None:
            if isinstance( data, IFeatureTool ):
                # Handle an object implementing IFeatureTool being dropped:
                dock_control = feature.dock_control
                data.feature_dropped_on_dock_control( dock_control )
                data.feature_dropped_on( dock_control.object )
            else:
                # Handle a normal object being dropped:
                wx, wy = self.control.GetScreenPosition()
                feature.set( x = wx + x, y = wy + y )
                feature.drop( data )

            return drag_result

        return wx.DragNone

    #---------------------------------------------------------------------------
    #  Handles a Python object being dragged over the control:
    #---------------------------------------------------------------------------

    def wx_drag_over ( self, x, y, data, drag_result ):
        """ Handles a Python object being dragged over the control.
        """
        # Handle the case of dragging a normal object over a 'feature':
        if self._can_drop_on_feature( x, y, data ) is not None:
            return drag_result

        return wx.DragNone

    #---------------------------------------------------------------------------
    #  Handles a dragged Python object leaving the window:
    #---------------------------------------------------------------------------

    def wx_drag_leave ( self, data ):
        """ Handles a dragged Python object leaving the window.
        """
        # Indicate use of the feature bar is complete:
        self.completed = True

        # Reset any drag state information:
        self.dock_control.post_drag( FEATURE_EXTERNAL_DRAG )

    #-- Private Methods --------------------------------------------------------

    #---------------------------------------------------------------------------
    #  Returns a feature that the pointer is over and which can accept the
    #  specified data:
    #---------------------------------------------------------------------------

    def _can_drop_on_feature ( self, x, y, data ):
        """ Returns a feature that the pointer is over and which can accept the
            specified data.
        """
        feature = self._feature_at( FakeEvent( x, y ) )
        if (feature is not None) and feature.can_drop( data ):
            return feature

        return None

    #---------------------------------------------------------------------------
    #  Returns the DockWindowFeature (if any) at a specified window position:
    #---------------------------------------------------------------------------

    def _feature_at ( self, event ):
        """ Returns the DockWindowFeature (if any) at a specified window
            position.
        """
        if self.horizontal:
            x = 4
            for feature in self.dock_control.active_features:
                bitmap = feature.bitmap
                if bitmap is not None:
                    bdx = bitmap.GetWidth()
                    if self._is_in( event, x, 4, bdx, bitmap.GetHeight() ):
                        return feature

                    x += (bdx + 3)
        else:
            y = 4
            for feature in self.dock_control.active_features:
                bitmap = feature.bitmap
                if bitmap is not None:
                    bdy = bitmap.GetHeight()
                    if self._is_in( event, 4, y, bitmap.GetWidth(), bdy ):
                        return feature

                    y += (bdy + 3)

        return None

    #---------------------------------------------------------------------------
    #  Returns whether or not an event is within a specified bounds:
    #---------------------------------------------------------------------------

    def _is_in ( self, event, x, y, dx, dy ):
        """ Returns whether or not an event is within a specified bounds.
        """
        return ((x <= event.GetX() < (x + dx)) and
                (y <= event.GetY() < (y + dy)))

#-------------------------------------------------------------------------------
#  'FakeEvent' class:
#-------------------------------------------------------------------------------

class FakeEvent ( object ):

    def __init__ ( self, x, y ):
        self.x, self.y = x, y

    def GetX ( self ): return self.x
    def GetY ( self ): return self.y

