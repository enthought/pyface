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

from traits.api \
    import *

from traitsui.api \
    import *

from traitsui.menu \
    import *

from traitsui.dockable_view_element \
    import DockableViewElement

from pyface.image_resource \
    import ImageResource

from pyface.dock.api \
    import *

#-------------------------------------------------------------------------------
#  Global data:
#-------------------------------------------------------------------------------

# DockControl style to use:
style = 'tab'

image1 = ImageResource( 'folder' )
image2 = ImageResource( 'gear' )

#-------------------------------------------------------------------------------
#  'AnEditor' class:
#-------------------------------------------------------------------------------

class AnEditor ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    code1   = Code
    code2   = Code
    name    = Str( 'Mike Noggins' )
    address = Str( '1313 Drury Lane' )
    shell   = PythonValue

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View( VSplit( VGroup( 'code1@', '|<>' ),
                                VGroup( 'code2@', '|<>' ),
                                VGroup( 'name', 'address' ),
                                VGroup( 'shell', '|{Python Shell}<>' ),
                                export      = 'editor',
                                show_labels = False ),
                        kind      = 'subpanel',
                        resizable = True,
                        buttons   = NoButtons,
                        dock      = 'horizontal' )

#-------------------------------------------------------------------------------
#  'AView' class:
#-------------------------------------------------------------------------------

class AView ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    code1 = Code
    code2 = Code

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View( VSplit( 'code1@', 'code2@',
                                show_labels = False ),
                        imports = [ 'editor' ],
                        dock    = 'horizontal',
                        kind    = 'subpanel' )

#-------------------------------------------------------------------------------
#  Creates a DockWindow as a Traits UI widget:
#-------------------------------------------------------------------------------

def create_dock_window ( parent, editor ):
    """ Creates a window for editing a workflow canvas.
    """
    try:
     main     = DockWindow( parent ).control
     view_uis = [ AView().edit_traits( parent = main ) for i in range( 6 ) ]
     views    = [ ui.control for ui in view_uis ]
     edit     = DockWindow( main ).control
     editors  = [ AnEditor().edit_traits( parent = edit ) for i in range( 6 ) ]
     controls = []
     for i in range( 6 ):
         dockable = DockableViewElement( ui = editors[i] )
         controls.append( DockControl(
                              name      = 'Editor %d' % (i + 1),
                              image     = image1,
                              closeable = True,
                              on_close  = dockable.close_dock_control,
                              control   = editors[i].control,
                              export    = 'editor',
                              dockable  = dockable,
                              style     = style ) )
     edit_sizer = DockSizer( contents = [ tuple( controls ) ] )
     dve0 = DockableViewElement( ui = view_uis[0] )
     dve1 = DockableViewElement( ui = view_uis[1] )
     main_sizer = DockSizer( contents =
                   [ [ DockControl( name      = 'View 1',
                                    image     = image1,
                                    closeable = True,
                                    on_close  = dve0.close_dock_control,
                                    dockable  = dve0,
                                    control   = views[0],
                                    style     = style ),
                       DockControl( name      = 'View 2',
                                    image     = image1,
                                    closeable = True,
                                    on_close  = dve1.close_dock_control,
                                    dockable  = dve1,
                                    height    = 400,
                                    control   = views[1],
                                    style     = style ) ],
                     [ DockControl( name      = 'Editors',
                                    image     = image1,
                                    control   = edit,
                                    style     = 'fixed' ),
                       [ DockControl( name    = 'View 3',
                                      image   = image2,
                                      control = views[2],
                                      style   = style ),
                         DockControl( name    = 'View 4',
                                      image   = image2,
                                      control = views[3],
                                      style   = style ) ] ],
                     [ DockControl( name      = 'View 5',
                                    control   = views[4],
                                    style     = style ),
                       DockControl( name      = 'View 6',
                                    control   = views[5],
                                    style     = style ) ] ] )
     edit.SetSizer( edit_sizer )
     main.SetSizer( main_sizer )

     return main
    except:
        import traceback
        traceback.print_exc()
        raise

#-------------------------------------------------------------------------------
#  'EnvisageDock' class:
#-------------------------------------------------------------------------------

class EnvisageDock ( HasPrivateTraits ):

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
                 title     = 'Envisage DockWindow Mock-up',
                 resizable = True,
                 width     = 1.00,
                 height    = 1.00,
                 buttons   = NoButtons )

#-------------------------------------------------------------------------------
#  Run the test program:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    EnvisageDock().configure_traits()
