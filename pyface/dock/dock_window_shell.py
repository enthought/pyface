#-------------------------------------------------------------------------------
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
#  Author: David C. Morrill
#  Date:   11/04/2005
#
#-------------------------------------------------------------------------------

""" Defines the DockWindowShell class used to house drag and drag DockWindow
    items that are dropped on the desktop or on the DockWindowShell window.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import wx

# Fixme: Hack to force 'image_slice' to be added via Category to Theme class:
import traitsui.wx
from traits.api import HasPrivateTraits, Instance
from traitsui.api import View, Group

from pyface.api import SystemMetrics
from pyface.image_resource import ImageResource
from .dock_window import DockWindow
from .dock_sizer import DockSizer, DockSection, DockRegion, DockControl, \
    DOCK_RIGHT

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# DockWindowShell frame icon:
FrameIcon = ImageResource( 'shell.ico' )

#-------------------------------------------------------------------------------
#  'DockWindowShell' class:
#-------------------------------------------------------------------------------

class DockWindowShell ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The wx.Frame window which is the actual shell:
    control = Instance( wx.Frame )

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, dock_control, use_mouse = False, **traits ):
        super( DockWindowShell, self ).__init__( **traits )

        old_control = dock_control.control
        parent      = wx.GetTopLevelParent( old_control )
        while True:
            next_parent = parent.GetParent()
            if next_parent is None:
                break
            parent = next_parent

        self.control = shell = wx.Frame( parent, -1, dock_control.name,
                                         style = wx.DEFAULT_FRAME_STYLE   |
                                                 wx.FRAME_FLOAT_ON_PARENT |
                                                 wx.FRAME_NO_TASKBAR )
        shell.SetIcon( FrameIcon.create_icon() )
        shell.SetBackgroundColour( SystemMetrics().dialog_background_color )
        wx.EVT_CLOSE( shell, self._on_close )

        theme = dock_control.theme
        dw = DockWindow( shell, auto_close = True, theme = theme )
        dw.trait_set( style = 'tab' )
        self._dock_window = dw
        sizer = wx.BoxSizer( wx.VERTICAL )
        sizer.Add( dw.control, 1, wx.EXPAND )
        shell.SetSizer( sizer )

        if use_mouse:
            x, y = wx.GetMousePosition()
        else:
            x, y = old_control.GetPositionTuple()
            x, y = old_control.GetParent().ClientToScreenXY( x, y )

        dx, dy = old_control.GetSize()
        tis    = theme.tab.image_slice
        tc     = theme.tab.content
        tdy    = theme.tab_active.image_slice.dy
        dx    += (tis.xleft + tc.left + tis.xright  + tc.right)
        dy    += (tis.xtop  + tc.top  + tis.xbottom + tc.bottom + tdy)

        self.add_control( dock_control )

        # Set the correct window size and position, accounting for the tab size
        # and window borders:
        shell.SetDimensions( x, y, dx, dy )
        cdx, cdy = shell.GetClientSizeTuple()
        ex_dx    = dx - cdx
        ex_dy    = dy - cdy
        shell.SetDimensions( x - (ex_dx / 2) - tis.xleft - tc.left,
                             y - ex_dy + (ex_dx / 2) - tdy - tis.xtop - tc.top,
                             dx + ex_dx, dy + ex_dy )
        shell.Show()

    #---------------------------------------------------------------------------
    #  Adds a new DockControl to the shell window:
    #---------------------------------------------------------------------------

    def add_control ( self, dock_control ):
        """ Adds a new DockControl to the shell window.
        """
        dw       = self._dock_window.control
        dockable = dock_control.dockable

        # If the current DockControl should be closed, then do it:
        close = dockable.dockable_should_close()
        if close:
            dock_control.close( force = True )

        # Create the new control:
        control = dockable.dockable_get_control( dw )

        # If the DockControl was closed, then reset it to point to the new
        # control:
        if close:
            dock_control.trait_set( control = control, style = 'tab' )
        else:
            # Create a DockControl to describe the new control:
            dock_control = DockControl( control   = control,
                                        name      = dock_control.name,
                                        export    = dock_control.export,
                                        style     = 'tab',
                                        image     = dock_control.image,
                                        closeable = True )

        # Finish initializing the DockControl:
        dockable.dockable_init_dockcontrol( dock_control )

        # Get the current DockSizer:
        sizer = dw.GetSizer()
        if sizer is None:
            # Create the initial sizer:
            dw.SetSizer( DockSizer( DockSection( contents = [ DockRegion(
                                    contents = [ dock_control ] ) ] ) ) )
        else:
            # Sizer exists already, try to add the DockControl as a new
            # notebook tab. If the user has reorganized the layout, then just
            # dock it on the right side somewhere:
            section = sizer.GetContents()
            region  = section.contents[0]
            if isinstance( region, DockRegion ):
                region.add( dock_control )
            else:
                section.add( dock_control, region, DOCK_RIGHT )

            # Force the control to update:
            dw.Layout()
            dw.Refresh()

    #---------------------------------------------------------------------------
    #  Handles the user attempting to close the window:
    #---------------------------------------------------------------------------

    def _on_close ( self, event ):
        """ Handles the user attempting to close the window.
        """
        window  = self._dock_window.control
        section = window.GetSizer().GetContents()
        n       = len( section.contents )

        # Try to close each individual control:
        for control in section.get_controls():
            control.close( layout = False )

        # If some, but not all, were closed, make sure the window gets updated:
        if 0 < len( section.contents ) < n:
            window.Layout()
            window.Refresh()

