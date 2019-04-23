#------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#  Thanks for using Enthought open source!
#
#  Author: David C. Morrill
#
#  Description: Image and text-based pyface button/toolbar/radio button control.
#
#------------------------------------------------------------------------------
""" An image and text-based control that can be used as a normal, radio or
    toolbar button.
"""
from __future__ import absolute_import

import wx
from numpy import array, fromstring, reshape, ravel, dtype

from traits.api import Str, Range, Enum, Instance, Event, false

from .widget import Widget
from .image_resource import ImageResource

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Text color used when a button is disabled:
DisabledTextColor = wx.Colour( 128, 128, 128 )

#-------------------------------------------------------------------------------
#  'ImageButton' class:
#-------------------------------------------------------------------------------

class ImageButton ( Widget ):
    """ An image and text-based control that can be used as a normal, radio or
        toolbar button.
    """

    # Pens used to draw the 'selection' marker:
    _selectedPenDark = wx.Pen(
        wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DSHADOW ), 1,
        wx.PENSTYLE_SOLID
    )

    _selectedPenLight = wx.Pen(
        wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DHIGHLIGHT ), 1,
        wx.PENSTYLE_SOLID
    )

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The image:
    image = Instance( ImageResource, allow_none = True )

    # The (optional) label:
    label = Str

    # Extra padding to add to both the left and right sides:
    width_padding = Range( 0, 31, 7 )

    # Extra padding to add to both the top and bottom sides:
    height_padding = Range( 0, 31, 5 )

    # Presentation style:
    style = Enum( 'button', 'radio', 'toolbar', 'checkbox' )

    # Orientation of the text relative to the image:
    orientation = Enum( 'vertical', 'horizontal' )

    # Is the control selected ('radio' or 'checkbox' style)?
    selected = false

    # Fired when a 'button' or 'toolbar' style control is clicked:
    clicked = Event

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, parent, **traits ):
        """ Creates a new image control.
        """
        self._image = None

        super( ImageButton, self ).__init__( **traits )

        # Calculate the size of the button:
        idx = idy = tdx = tdy = 0
        if self._image is not None:
            idx = self._image.GetWidth()
            idy = self._image.GetHeight()

        if self.label != '':
            dc = wx.ScreenDC()
            dc.SetFont( wx.NORMAL_FONT )
            tdx, tdy = dc.GetTextExtent( self.label )

        wp2 = self.width_padding  + 2
        hp2 = self.height_padding + 2
        if self.orientation == 'horizontal':
            self._ix = wp2
            spacing  = (idx > 0) * (tdx > 0) * 4
            self._tx = self._ix + idx + spacing
            dx       = idx + tdx + spacing
            dy       = max( idy, tdy )
            self._iy = hp2 + ((dy - idy) / 2)
            self._ty = hp2 + ((dy - tdy) / 2)
        else:
            self._iy = hp2
            spacing  = (idy > 0) * (tdy > 0) * 2
            self._ty = self._iy + idy + spacing
            dx       = max( idx, tdx )
            dy       = idy + tdy + spacing
            self._ix = wp2 + ((dx - idx) / 2)
            self._tx = wp2 + ((dx - tdx) / 2)

        # Create the toolkit-specific control:
        self._dx     = dx + wp2 + wp2
        self._dy     = dy + hp2 + hp2
        self.control = wx.Window( parent, -1,
                                  size = wx.Size( self._dx, self._dy ) )
        self.control._owner = self
        self._mouse_over    = self._button_down = False

        # Set up mouse event handlers:
        wx.EVT_ENTER_WINDOW( self.control, self._on_enter_window )
        wx.EVT_LEAVE_WINDOW( self.control, self._on_leave_window )
        wx.EVT_LEFT_DOWN(    self.control, self._on_left_down )
        wx.EVT_LEFT_UP(      self.control, self._on_left_up )
        wx.EVT_PAINT(        self.control, self._on_paint )

    #---------------------------------------------------------------------------
    #  Handles the 'image' trait being changed:
    #---------------------------------------------------------------------------

    def _image_changed ( self, image ):
        self._image = self._mono_image = None
        if image is not None:
            self._img   = image.create_image()
            self._image = self._img.ConvertToBitmap()

        if self.control is not None:
            self.control.Refresh()

    #---------------------------------------------------------------------------
    #  Handles the 'selected' trait being changed:
    #---------------------------------------------------------------------------

    def _selected_changed ( self, selected ):
        """ Handles the 'selected' trait being changed.
        """
        if selected and (self.style == 'radio'):
            for control in self.control.GetParent().GetChildren():
                owner = getattr( control, '_owner', None )
                if (isinstance( owner, ImageButton ) and owner.selected and
                    (owner is not self)):
                    owner.selected = False
                    break

        self.control.Refresh()

#-- wx event handlers ----------------------------------------------------------

    def _on_enter_window ( self, event ):
        """ Called when the mouse enters the widget. """

        if self.style != 'button':
            self._mouse_over = True
            self.control.Refresh()

    def _on_leave_window ( self, event ):
        """ Called when the mouse leaves the widget. """

        if self._mouse_over:
            self._mouse_over = False
            self.control.Refresh()

    def _on_left_down ( self, event ):
        """ Called when the left mouse button goes down on the widget. """
        self._button_down = True
        self.control.CaptureMouse()
        self.control.Refresh()

    def _on_left_up ( self, event ):
        """ Called when the left mouse button goes up on the widget. """
        control = self.control
        control.ReleaseMouse()
        self._button_down = False
        wdx, wdy          = control.GetClientSizeTuple()
        x, y              = event.GetX(), event.GetY()
        control.Refresh()
        if (0 <= x < wdx) and (0 <= y < wdy):
            if self.style == 'radio':
                self.selected = True
            elif self.style == 'checkbox':
                self.selected = not self.selected
            else:
                self.clicked = True

    def _on_paint ( self, event ):
        """ Called when the widget needs repainting.
        """
        wdc      = wx.PaintDC( self.control )
        wdx, wdy = self.control.GetClientSizeTuple()
        ox       = (wdx - self._dx) / 2
        oy       = (wdy - self._dy) / 2

        disabled = (not self.control.IsEnabled())
        if self._image is not None:
            image = self._image
            if disabled:
                if self._mono_image is None:
                    img  = self._img
                    data = reshape(fromstring(img.GetData(), dtype('uint8')),
                                   (-1, 3)) * array([[ 0.297, 0.589, 0.114 ]])
                    g = data[ :, 0 ] + data[ :, 1 ] + data[ :, 2 ]
                    data[ :, 0 ] = data[ :, 1 ] = data[ :, 2 ] = g
                    img.SetData(ravel(data.astype(dtype('uint8'))).tostring())
                    img.SetMaskColour(0, 0, 0)
                    self._mono_image = img.ConvertToBitmap()
                    self._img        = None
                image = self._mono_image
            wdc.DrawBitmap( image, ox + self._ix, oy + self._iy, True )

        if self.label != '':
            if disabled:
                wdc.SetTextForeground( DisabledTextColor )
            wdc.SetFont( wx.NORMAL_FONT )
            wdc.DrawText( self.label, ox + self._tx, oy + self._ty )

        pens  = [ self._selectedPenLight, self._selectedPenDark ]
        bd    = self._button_down
        style = self.style
        is_rc = (style in ( 'radio', 'checkbox' ))
        if bd or (style == 'button') or (is_rc and self.selected):
            if is_rc:
                bd = 1 - bd
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

        elif self._mouse_over and (not self.selected):
            wdc.SetBrush( wx.TRANSPARENT_BRUSH )
            wdc.SetPen( pens[ bd ] )
            wdc.DrawLine( 0, 0, wdx, 0 )
            wdc.DrawLine( 0, 1, 0, wdy )
            wdc.SetPen( pens[ 1 - bd ] )
            wdc.DrawLine( wdx - 1, 1, wdx - 1, wdy )
            wdc.DrawLine( 1, wdy - 1, wdx - 1, wdy - 1 )
