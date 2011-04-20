#-------------------------------------------------------------------------------
#
#  Test the DockWindow.
#
#  Written by: David C. Morrill
#
#  Date: 10/20/2005
#
#  (c) Copyright 2005 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import wx
import sys

from traits.api \
    import *

from traitsui.api \
    import *

from traitsui.menu \
    import *

from pyface.dock.api \
    import *

from pyface.image_resource \
    import ImageResource

#-------------------------------------------------------------------------------
#  Global data:
#-------------------------------------------------------------------------------

# DockControl style to use:
style1 = 'horizontal'
style2 = 'vertical'

image1 = ImageResource( 'folder' )
image2 = ImageResource( 'gear' )

#-------------------------------------------------------------------------------
#  Creates a DockWindow as a Traits UI widget:
#-------------------------------------------------------------------------------

def create_dock_window ( parent, editor ):
    """ Creates a window for editing a workflow canvas.
    """
    window  = DockWindow( parent ).control
    button1 = wx.Button( window, -1, 'Button 1' )
    button2 = wx.Button( window, -1, 'Button 2' )
    button3 = wx.Button( window, -1, 'Button 3' )
    button4 = wx.Button( window, -1, 'Button 4' )
    button5 = wx.Button( window, -1, 'Button 5' )
    button6 = wx.Button( window, -1, 'Button 6' )
    sizer   = DockSizer( contents =
                  [ DockControl( name      = 'Button 1',
                                 image     = image1,
                                 closeable = True,
                                 control   = button1,
                                 style     = style1 ),
                    [ DockControl( name      = 'Button 2',
                                   image     = image1,
                                   closeable = True,
                                   height    = 400,
                                   control   = button2,
                                   style   = style1 ),
                      ( [ DockControl( name      = 'Button 3',
                                     image     = image2,
                                     resizable = False,
                                       control   = button3,
                                       style     = style2 ),
                          DockControl( name      = 'Button 4',
                                       image     = image2,
                                       resizable = False,
                                       control   = button4,
                                       style     = style2 ) ],
                        [  DockControl( name      = 'Button 5',
                                       resizable = False,
                                       control   = button5,
                                       style     = style2 ),
                          DockControl( name      = 'Button 6',
                                       resizable = False,
                                       control   = button6,
                                       style     = style2 ) ] )
                    ]
                  ] )
    window.SetSizer( sizer )
    window.SetAutoLayout( True )

    return window

#-------------------------------------------------------------------------------
#  'TestDock' class:
#-------------------------------------------------------------------------------

class TestDock ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    dummy = Int

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View( [ Item( 'dummy',
                         resizable = True,
                         editor    = CustomEditor( create_dock_window ) ),
                   '|<>' ],
                 title     = 'DockWindow Test',
                 resizable = True,
                 width     = 0.5,
                 height    = 0.5,
                 buttons   = NoButtons )

#-------------------------------------------------------------------------------
#  Run the test program:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    if len( sys.argv ) > 1:
        style1 = style2 = sys.argv[1]
        if len( sys.argv ) > 2:
            style2 = sys.argv[2]
    TestDock().configure_traits()
