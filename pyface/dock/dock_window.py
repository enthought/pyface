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
#  Date:   10/18/2005
#
#-------------------------------------------------------------------------------

""" Pyface 'DockWindow' support.

    This package provides a Pyface 'dockable' window component that allows
    child windows to be reorganized within the DockWindow using drag and drop.
    The component also allows multiple sub-windows to occupy the same
    sub-region of the DockWindow, in which case each sub-window appears as a
    separate notebook-like tab within the region.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import shelve
import os
import wx
import sys

from pyface.api import SystemMetrics

from traits.api \
    import HasPrivateTraits, Instance, Tuple, Property, Any, Str, List, false

from traits.trait_base \
    import traits_home

from traitsui.api \
    import View, HGroup, VGroup, Item, Handler, error

from traitsui.helper \
    import user_name_for

from traitsui.menu \
    import Menu, Action, Separator

from traitsui.dockable_view_element \
    import DockableViewElement

from traitsui.dock_window_theme \
    import dock_window_theme, DockWindowTheme

from pyface.wx.drag_and_drop \
    import PythonDropTarget, clipboard

from pyface.message_dialog \
    import error as warning

from dock_sizer \
    import DockSizer, DockControl, DockRegion, DockStyle, DockSplitter, \
           no_dock_info, clear_window, features

from idockable \
    import IDockable

from idock_ui_provider \
    import IDockUIProvider

is_mac = (sys.platform == 'darwin')

#-------------------------------------------------------------------------------
#  Global data:
#-------------------------------------------------------------------------------

# Dictionary of cursors in use:
cursor_map = {}

#-------------------------------------------------------------------------------
#  DockWindow context menu:
#-------------------------------------------------------------------------------

min_max_action = Action( name   = 'Maximize',
                         action = 'on_min_max' )

undock_action  = Action( name   = 'Undock',
                         action = 'on_undock' )

lock_action    = Action( name   = 'Lock Layout',
                         action = 'on_lock_layout',
                         style  = 'toggle' )

layout_action  = Action( name   = 'Switch Layout',
                         action = 'on_switch_layout' )

save_action    = Action( name   = 'Save Layout...',
                         action = 'on_save_layout' )

#hide_action    = Action( name   = 'Hide',
#                         action = 'on_hide' )
#
#show_action    = Action( name   = 'Show',
#                         action = 'on_show' )

edit_action    = Action( name   = 'Edit Properties...',
                         action = 'on_edit' )

enable_features_action  = Action( name   = 'Show All',
                                  action = 'on_enable_all_features' )

disable_features_action = Action( name   = 'Hide All',
                                  action = 'on_disable_all_features' )

#-------------------------------------------------------------------------------
#  'DockWindowHandler' class/interface:
#-------------------------------------------------------------------------------

class DockWindowHandler ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Returns whether or not a specified object can be inserted into the view:
    #---------------------------------------------------------------------------

    def can_drop ( self, object ):
        """ Returns whether or not a specified object can be inserted into the
            view.
        """
        return True

    #---------------------------------------------------------------------------
    #  Returns the DockControl object for a specified object:
    #---------------------------------------------------------------------------

    def dock_control_for ( self, parent, object ):
        """ Returns the DockControl object for a specified object.
        """
        try:
            name = object.name
        except:
            try:
                name = object.label
            except:
                name = ''
        if name == '':
            name = user_name_for( object.__class__.__name__ )

        image  = None
        export = ''
        if isinstance( object, DockControl ):
            dock_control = object
            image        = dock_control.image
            export       = dock_control.export
            dockable     = dock_control.dockable
            close        = dockable.dockable_should_close()
            if close:
                dock_control.close( force = True )

            control = dockable.dockable_get_control( parent )

            # If DockControl was closed, then reset it to point to the new
            # control:
            if close:
                dock_control.set( control = control,
                                  style   = parent.owner.style )
                dockable.dockable_init_dockcontrol( dock_control )
                return dock_control

        elif isinstance( object, IDockable ):
            dockable = object
            control  = dockable.dockable_get_control( parent )
        else:
            ui       = object.get_dockable_ui( parent )
            dockable = DockableViewElement( ui = ui )
            export   = ui.view.export
            control  = ui.control

        dc = DockControl( control   = control,
                          name      = name,
                          export    = export,
                          style     = parent.owner.style,
                          image     = image,
                          closeable = True )

        dockable.dockable_init_dockcontrol( dc )

        return dc

    #---------------------------------------------------------------------------
    #  Creates a new view of a specified control:
    #---------------------------------------------------------------------------

    def open_view_for ( self, control, use_mouse = True ):
        """ Creates a new view of a specified control.
        """
        from dock_window_shell import DockWindowShell

        DockWindowShell( control, use_mouse = use_mouse )

    #---------------------------------------------------------------------------
    #  Handles the DockWindow becoming empty:
    #---------------------------------------------------------------------------

    def dock_window_empty ( self, dock_window ):
        """ Handles the DockWindow becoming empty.
        """
        if dock_window.auto_close:
            dock_window.control.GetParent().Destroy()

# Create a singleton handler:
dock_window_handler = DockWindowHandler()

#-------------------------------------------------------------------------------
#  'LayoutName' class:
#-------------------------------------------------------------------------------

class LayoutName ( Handler ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Name the user wants to assign to the layout:
    name = Str

    # List of currently assigned names:
    names = List( Str )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View( Item( 'name', label = 'Layout name' ),
                 title   = 'Save Layout',
                 kind    = 'modal',
                 buttons = [ 'OK', 'Cancel' ] )

    #---------------------------------------------------------------------------
    #  Handles a request to close a dialog-based user interface by the user:
    #---------------------------------------------------------------------------

    def close ( self, info, is_ok ):
        if is_ok:
            name = info.object.name.strip()
            if name == '':
                warning( info.ui.control, 'No name specified',
                         title = 'Save Layout Error' )
                return False
            if name in self.names:
                return error( message = '%s is already defined. Replace?' %
                                        name,
                              title   = 'Save Layout Warning',
                              parent  = info.ui.control )

        return True

#-------------------------------------------------------------------------------
#  'DockWindow' class:
#-------------------------------------------------------------------------------

class DockWindow ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The wx.Window being used as the DockWindow:
    control = Instance( wx.Window )

    # The handler used to determine how certain events should be processed:
    handler = Any( dock_window_handler )

    # The 'extra' arguments to be passed to each handler call:
    handler_args = Tuple

    # Close the parent window if the DockWindow becomes empty:
    auto_close = false

    # The DockWindow graphical theme style information:
    theme = Instance( DockWindowTheme, allow_none = False )

    # Default style for external objects dragged into the window:
    style = DockStyle

    # Return the sizer associated with the control (i.e. window)
    sizer = Property

    # The id used to identify this DockWindow:
    id = Str

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, parent, wid = -1, pos = wx.DefaultPosition,
                   size = wx.DefaultSize, style = wx.FULL_REPAINT_ON_RESIZE,
                   **traits ):
        super( DockWindow, self ).__init__( **traits )

        # Create the actual window:
        self.control  = control = wx.Window( parent, wid, pos, size, style )
        control.owner = self

        # Set up the 'paint' event handler:
        wx.EVT_PAINT( control, self._paint )
        wx.EVT_SIZE(  control, self._size )

        # Set up mouse event handlers:
        wx.EVT_LEFT_DOWN(    control, self._left_down )
        wx.EVT_LEFT_UP(      control, self._left_up )
        wx.EVT_LEFT_DCLICK(  control, self._left_dclick )
        wx.EVT_RIGHT_DOWN(   control, self._right_down )
        wx.EVT_RIGHT_UP(     control, self.right_up )
        wx.EVT_MOTION(       control, self._mouse_move )
        wx.EVT_LEAVE_WINDOW( control, self._mouse_leave )

        control.SetDropTarget( PythonDropTarget( self ) )

        # Initialize the window background color:
        if self.theme.use_theme_color:
            color = self.theme.tab.image_slice.bg_color
        else:
            color = SystemMetrics().dialog_background_color
            color = wx.Colour(color[0]*255, color[1]*255, color[2]*255)

        self.control.SetBackgroundColour( color )

    #-- Default Trait Values ---------------------------------------------------

    def _theme_default ( self ):
        return dock_window_theme()

    #-- Trait Event Handlers ---------------------------------------------------

    def _theme_changed ( self, theme ):
        if self.control is not None:
            if theme.use_theme_color:
                color = theme.tab.image_slice.bg_color
            else:
                color = wx.NullColour
            self.control.SetBackgroundColour( color )

            self.update_layout()

    #---------------------------------------------------------------------------
    #  Notifies the DockWindow that its contents are empty:
    #---------------------------------------------------------------------------

    def dock_window_empty ( self ):
        """ Notifies the DockWindow that its contents are empty.
        """
        self.handler.dock_window_empty( self )

    #---------------------------------------------------------------------------
    #  Sets the cursor to a specified cursor shape:
    #---------------------------------------------------------------------------

    def set_cursor ( self, cursor = None ):
        """ Sets the cursor to a specified cursor shape.
        """
        if cursor is None:
            self.control.SetCursor( wx.NullCursor )
            return

        global cursor_map

        if cursor not in cursor_map:
            cursor_map[ cursor ] = wx.StockCursor( cursor )

        self.control.SetCursor( cursor_map[ cursor ] )

    #---------------------------------------------------------------------------
    #  Releases ownership of the mouse capture:
    #---------------------------------------------------------------------------

    def release_mouse ( self ):
        """ Releases ownership of the mouse capture.
        """
        if self._owner is not None:
            self._owner = None
            self.control.ReleaseMouse()

    #---------------------------------------------------------------------------
    #  Updates the layout of the window:
    #---------------------------------------------------------------------------

    def update_layout ( self ):
        """ Updates the layout of the window.
        """
        # There are cases where a layout has been scheduled for a DockWindow,
        # but then the DockWindow is destroyed, which will cause the calls
        # below to fail. So we catch the 'PyDeadObjectError' exception and
        # ignore it:
        try:
            self.control.Layout()
            self.control.Refresh()
        except wx.PyDeadObjectError:
            pass

    #---------------------------------------------------------------------------
    #  Minimizes/Maximizes a specified DockControl:
    #---------------------------------------------------------------------------

    def min_max ( self, dock_control ):
        """ Minimizes/maximizes a specified DockControl.
        """
        sizer = self.sizer
        if sizer is not None:
            sizer.MinMax( self.control, dock_control )
            self.update_layout()

    #---------------------------------------------------------------------------
    #  Pops up the feature bar for a specified DockControl:
    #---------------------------------------------------------------------------

    def feature_bar_popup ( self, dock_control ):
        """ Pops up the feature bar for a specified DockControl.
        """
        fb = self._feature_bar
        if fb is None:
            from feature_bar import FeatureBar

            self._feature_bar = fb = FeatureBar( parent = self.control )
            fb.on_trait_change( self._feature_bar_closed, 'completed' )

        fb.dock_control = dock_control
        fb.show()

    #---------------------------------------------------------------------------
    #  Handles closing the feature bar:
    #---------------------------------------------------------------------------

    def _feature_bar_closed ( self ):
        fb = self._feature_bar
        fb.dock_control.feature_bar_closed()
        fb.hide()

    #---------------------------------------------------------------------------
    #  Perform all operations needed to close the window:
    #---------------------------------------------------------------------------

    def close ( self ):
        """ Closes the dock window.  In this case, all event handlers are
        unregistered.  Other cleanup operations go here, but at the moment Linux
        (and other non-Windows platforms?) are less forgiving when things like
        event handlers arent unregistered.
        """
        self._unregister_event_handlers()

    #---------------------------------------------------------------------------
    #  Unregister all event handlers:
    #---------------------------------------------------------------------------

    def _unregister_event_handlers ( self ):
        """ Unregister all event handlers setup in the constructor.  This is
        typically done prior to an app shutting down and is needed since Linux
        (and other non-Windows platforms?) trigger mouse, repaint, etc. events
        for controls which have already been deleted.
        """
        control = self.control
        if control is not None:
            wx.EVT_PAINT(            control, None )
            wx.EVT_SIZE(             control, None )
            wx.EVT_LEFT_DOWN(        control, None )
            wx.EVT_LEFT_UP(          control, None )
            wx.EVT_LEFT_DCLICK(      control, None )
            wx.EVT_RIGHT_DOWN(       control, None )
            wx.EVT_RIGHT_UP(         control, None )
            wx.EVT_MOTION(           control, None )
            wx.EVT_LEAVE_WINDOW(     control, None )

    #---------------------------------------------------------------------------
    #  Handles repainting the window:
    #---------------------------------------------------------------------------

    def _paint ( self, event ):
        """ Handles repainting the window.
        """
        # There is a problem on macs where we get paints when the update
        # is entirely within children.
        if is_mac and self._is_child_paint():
            return

        sizer = self.sizer
        if isinstance( sizer, DockSizer ):
            sizer.Draw( self.control )
        else:
            clear_window( self.control )

    #---------------------------------------------------------------------------
    #  Uses wx calls to determine if we really need to paint or the children will
    #  do it.
    #---------------------------------------------------------------------------

    def _is_child_paint ( self ):
        """ Returns whether or not the current update region is entirely within a child.
        """
        if self.control.Children:
            update_rect = self.control.UpdateRegion.Box
            for child in self.control.Children:
                if not child.HasTransparentBackground() and \
                        child.Rect.ContainsRect(update_rect):
                    return True
        return False

    #---------------------------------------------------------------------------
    #  Handles the window being resized:
    #---------------------------------------------------------------------------

    def _size ( self, event ):
        """ Handles the window being resized.
        """
        sizer = self.sizer
        if sizer is not None:
            try:
                dx, dy = self.control.GetSizeTuple()
                sizer.SetDimension( 0, 0, dx, dy )
            except:
                # fixme: This is temporary code to work around a problem in
                #        ProAVA2 that we are still trying to track down...
                pass

    #---------------------------------------------------------------------------
    #  Handles the left mouse button being pressed:
    #---------------------------------------------------------------------------

    def _left_down ( self, event ):
        """ Handles the left mouse button being pressed.
        """
        sizer = self.sizer
        if sizer is not None:
            object = sizer.ObjectAt( event.GetX(), event.GetY() )
            if object is not None:
                self._owner = object
                self.control.CaptureMouse()
                object.mouse_down( event )

    #---------------------------------------------------------------------------
    #  Handles the left mouse button being released:
    #---------------------------------------------------------------------------

    def _left_up ( self, event ):
        """ Handles the left mouse button being released.
        """
        window = self.control
        if self._owner is not None:
            window.ReleaseMouse()
            self._owner.mouse_up( event )
            self._owner = None

        # Check for the user requesting that the layout structure be reset:
        if event.ShiftDown():
            if event.ControlDown():
                # Check for the developer requesting a structure dump (DEBUG):
                if event.AltDown():
                    contents = self.sizer.GetContents()
                    if contents is not None:
                        contents.dump()
                        sys.stdout.flush()
                else:
                    self.sizer.ResetStructure( window )
                    self.update_layout()
            elif event.AltDown():
                self.sizer.ToggleLock()
                self.update_layout()

    #---------------------------------------------------------------------------
    #  Handles the left mouse button being double clicked:
    #---------------------------------------------------------------------------

    def _left_dclick ( self, event ):
        """ Handles the left mouse button being double clicked.
        """
        sizer = self.sizer
        if sizer is not None:
            object = sizer.ObjectAt( event.GetX(), event.GetY(), True )
            if isinstance( object, DockControl ):
                dockable = object.dockable
                if (((dockable is None) or
                     (dockable.dockable_dclick( object, event ) is False)) and
                    (object.style != 'fixed')):
                    self.min_max( object )
            elif isinstance( object, DockRegion ):
                self._owner = object
                self.control.CaptureMouse()
                object.mouse_down( event )

    #---------------------------------------------------------------------------
    #  Handles the right mouse button being pressed:
    #---------------------------------------------------------------------------

    def _right_down ( self, event ):
        """ Handles the right mouse button being pressed.
        """
        pass

    #---------------------------------------------------------------------------
    #  Handles the right mouse button being released:
    #---------------------------------------------------------------------------

    def right_up ( self, event ):
        """ Handles the right mouse button being released.
        """
        sizer = self.sizer
        if sizer is not None:
            object = sizer.ObjectAt( event.GetX(), event.GetY(), True )
            if object is not None:
                popup_menu      = None
                window          = self.control
                is_dock_control = isinstance( object, DockControl )

                if (is_dock_control and (object.dockable is not None) and
                    (event.ShiftDown() or event.ControlDown() or
                     event.AltDown())):
                    self._menu_self = object.dockable
                    popup_menu = object.dockable.dockable_menu( object, event )

                if popup_menu is None:
                    self._menu_self = self
                    section         = self.sizer.GetContents()
                    is_splitter     = isinstance( object, DockSplitter )
                    self._object    = object
                    if is_splitter:
                        self._object = object = object.parent
                    group = object
                    if is_dock_control:
                        group = group.parent
                    if sizer.IsMaximizable():
                        min_max_action.name = 'Maximize'
                    else:
                        min_max_action.name = 'Restore'
                    min_max_action.enabled  = is_dock_control
                    undock_action.enabled   = is_dock_control
                    edit_action.enabled     = (not is_splitter)
                    controls                = section.get_controls( False )
                    lock_action.checked     = ((len( controls ) > 0) and
                                               controls[0].locked)
                    save_action.enabled     = (self.id != '')

                    feature_menu = self._get_feature_menu()
                    restore_menu, delete_menu = self._get_layout_menus()
                    popup_menu = Menu( min_max_action,
                                       undock_action,
                                       Separator(),
                                       feature_menu,
                                       #Separator(),
                                       #hide_action,
                                       #show_action,
                                       Separator(),
                                       lock_action,
                                       layout_action,
                                       Separator(),
                                       save_action,
                                       restore_menu,
                                       delete_menu,
                                       Separator(),
                                       edit_action,
                                       name = 'popup' )

                window.PopupMenuXY( popup_menu.create_menu( window, self ),
                                    event.GetX() - 10, event.GetY() - 10 )
                self._object = None

    #---------------------------------------------------------------------------
    #  Handles the mouse moving over the window:
    #---------------------------------------------------------------------------

    def _mouse_move ( self, event ):
        """ Handles the mouse moving over the window.
        """
        if self._last_dock_control is not None:
            self._last_dock_control.reset_feature_popup()
            self._last_dock_control = None

        if self._owner is not None:
            self._owner.mouse_move( event )
        else:
            sizer = self.sizer
            if sizer is not None:
                object = (self._object or
                          sizer.ObjectAt( event.GetX(), event.GetY() ))
                self._set_cursor( event, object )

                if object is not self._hover:
                    if self._hover is not None:
                        self._hover.hover_exit( event )

                    if object is not None:
                        object.hover_enter( event )

                    self._hover = object

                # Handle feature related processing:
                if (isinstance( object, DockControl ) and
                    object.feature_activate( event )):
                    self._last_dock_control = object


    #---------------------------------------------------------------------------
    #  Handles the mouse leaving the window:
    #---------------------------------------------------------------------------

    def _mouse_leave ( self, event ):
        """ Handles the mouse leaving the window.
        """
        if self._hover is not None:
            self._hover.hover_exit( event )
            self._hover = None
        self._set_cursor( event )

    #---------------------------------------------------------------------------
    #  Sets the cursor for a specified object:
    #---------------------------------------------------------------------------

    def _set_cursor ( self, event, object = None ):
        """ Sets the cursor for a specified object.
        """
        if object is None:
            self.set_cursor()
        else:
            self.set_cursor( object.get_cursor( event ) )

#-- Context menu action handlers -----------------------------------------------

    #---------------------------------------------------------------------------
    #  Handles the user asking for a DockControl to be maximized/restored:
    #---------------------------------------------------------------------------

    def on_min_max ( self ):
        """ Handles the user asking for a DockControl to be maximized/restored.
        """
        self.min_max( self._object )

    #---------------------------------------------------------------------------
    #  Handles the user requesting an element to be undocked:
    #---------------------------------------------------------------------------

    def on_undock ( self ):
        """ Handles the user requesting an element to be undocked.
        """
        self.handler.open_view_for( self._object, use_mouse = False )

    #---------------------------------------------------------------------------
    #  Handles the user requesting an element to be hidden:
    #---------------------------------------------------------------------------

    def on_hide ( self ):
        """ Handles the user requesting an element to be hidden.
        """
        self._object.show( False )

    #---------------------------------------------------------------------------
    #  Handles the user requesting an element to be shown:
    #---------------------------------------------------------------------------

    def on_show ( self ):
        """ Handles the user requesting an element to be shown.
        """
        object = self._object
        if isinstance( object, DockControl ):
            object = object.parent
        self._hidden_group_for( object ).show( True )

    #---------------------------------------------------------------------------
    #  Handles the user requesting that the current layout be switched:
    #---------------------------------------------------------------------------

    def on_switch_layout ( self ):
        """ Handles the user requesting that the current layout be switched.
        """
        self.sizer.ResetStructure( self.control )
        self.update_layout()

    #---------------------------------------------------------------------------
    #  Handles the user requesting that the layout be locked/unlocked:
    #---------------------------------------------------------------------------

    def on_lock_layout ( self ):
        """ Handles the user requesting that the layout be locked/unlocked.
        """
        self.sizer.ToggleLock()
        self.update_layout()

    #---------------------------------------------------------------------------
    #  Handles the user requesting that the layout be saved:
    #---------------------------------------------------------------------------

    def on_save_layout ( self ):
        """ Handles the user requesting that the layout be saved.
        """
        layout_name = LayoutName( names = self._get_layout_names() )
        if layout_name.edit_traits( parent = self.control ).result:
            self._set_layout( layout_name.name, self.sizer.GetStructure() )

    #---------------------------------------------------------------------------
    #  Handles the user requesting a specified layout to be restored:
    #---------------------------------------------------------------------------

    def on_restore_layout ( self, name ):
        """ Handles the user requesting a specified layout to be restored.
        """
        self.sizer.SetStructure( self.control, self._get_layout( name ) )
        self.update_layout()

    #---------------------------------------------------------------------------
    #  Handles the user reqesting a specified layout to be deleted:
    #---------------------------------------------------------------------------

    def on_delete_layout ( self, name ):
        """ Handles the user reqesting a specified layout to be deleted.
        """
        if error( message = "Delete the '%s' layout?" % name,
                  title   = 'Delete Layout Warning',
                  parent  = self.control ):
            self._delete_layout( name )

    #---------------------------------------------------------------------------
    #  Handles the user requesting to edit an item:
    #---------------------------------------------------------------------------

    def on_edit ( self, object = None ):
        """ Handles the user requesting to edit an item.
        """
        if object is None:
            object = self._object
        control_info = ControlInfo( **object.get( 'name', 'user_name',
                                                  'style', 'user_style' ) )
        if control_info.edit_traits( parent = self.control ).result:
            name = control_info.name.strip()
            if name != '':
                object.name = name
            object.set( **control_info.get( 'user_name',
                                            'style', 'user_style' ) )
            self.update_layout()

    #---------------------------------------------------------------------------
    #  Enables all features:
    #---------------------------------------------------------------------------

    def on_enable_all_features ( self, action ):
        """ Enables all features.
        """
        for feature in features:
            if (feature.feature_name != '') and (feature.state != 1):
                feature.toggle_feature( action )

    #---------------------------------------------------------------------------
    #  Disables all features:
    #---------------------------------------------------------------------------

    def on_disable_all_features ( self, action ):
        """ Disables all features.
        """
        for feature in features:
            if (feature.feature_name != '') and (feature.state == 1):
                feature.toggle_feature( action )

    #---------------------------------------------------------------------------
    #  Toggles the enabled/disabled state of the action's associated feature:
    #---------------------------------------------------------------------------

    def on_toggle_feature ( self, action ):
        """ Toggles the enabled/disabled state of the action's associated
            feature.
        """
        action._feature.toggle_feature( action )

#-- DockWindow user preference database methods --------------------------------

    #---------------------------------------------------------------------------
    #  Gets the layout dictionary for the DockWindow:
    #---------------------------------------------------------------------------

    def _get_layouts ( self ):
        """ Gets the layout dictionary for the DockWindow.
        """
        id = self.id
        if id != '':
            db = self._get_dw_db()
            if db is not None:
                layouts = db.get( id )
                db.close()
                return layouts

        return None

    #---------------------------------------------------------------------------
    #  Gets the names of all current layouts defined for the DockWindow:
    #---------------------------------------------------------------------------

    def _get_layout_names ( self ):
        """ Gets the names of all current layouts defined for the DockWindow.
        """
        layouts = self._get_layouts()
        if layouts is not None:
            return layouts.keys()

        return []

    #---------------------------------------------------------------------------
    #  Gets the layout data for a specified layout name:
    #---------------------------------------------------------------------------

    def _get_layout ( self, name ):
        """ Gets the layout data for a specified layout name.
        """
        layouts = self._get_layouts()
        if layouts is not None:
            return layouts.get( name )

        return None

    #---------------------------------------------------------------------------
    #  Deletes the layout data for a specified layout name:
    #---------------------------------------------------------------------------

    def _delete_layout ( self, name ):
        """ Deletes the layout data for a specified layout name.
        """
        id = self.id
        if id != '':
            db = self._get_dw_db( mode = 'c' )
            if db is not None:
                layouts = db.get( id )
                if layouts is not None:
                    del layouts[ name ]
                    db[ id ] = layouts
                db.close()

    #---------------------------------------------------------------------------
    #  Sets the layout data for a specified layout name:
    #---------------------------------------------------------------------------

    def _set_layout ( self, name, layout ):
        """ Sets the layout data for a specified layout name.
        """
        id = self.id
        if id != '':
            db = self._get_dw_db( mode = 'c' )
            if db is not None:
                layouts = db.get( id )
                if layouts is None:
                    layouts = {}
                layouts[ name ] = layout
                db[ id ] = layouts
                db.close()

    #---------------------------------------------------------------------------
    #  Gets a reference to the DockWindow UI preference database:
    #---------------------------------------------------------------------------

    def _get_dw_db ( self, mode = 'r' ):
        try:
            return shelve.open( os.path.join( traits_home(), 'dock_window' ),
                                flag = mode, protocol = -1 )
        except:
            return None

    #---------------------------------------------------------------------------
    #  Returns the 'Features' sub_menu:
    #---------------------------------------------------------------------------

    def _get_feature_menu ( self ):
        """ Returns the 'Features' sub_menu.
        """
        enable_features_action.enabled = disable_features_action.enabled = False
        for feature in features:
            if feature.feature_name != '':
                if feature.state == 1:
                    disable_features_action.enabled = True
                    if enable_features_action.enabled:
                        break
                else:
                    enable_features_action.enabled = True
                    if disable_features_action.enabled:
                        break

        actions = []
        for feature in features:
            if feature.feature_name != '':
                actions.append( Action( name     = feature.feature_name,
                                        action   = 'on_toggle_feature',
                                        _feature = feature,
                                        style    = 'toggle',
                                        checked  = (feature.state == 1) ) )

        if len( actions ) > 0:
            actions.sort( lambda l, r: cmp( l.name, r.name ) )
            actions[0:0] = [ Separator() ]

        return Menu( name = 'Features',
                     *([ enable_features_action, disable_features_action ] +
                       actions) )

    #---------------------------------------------------------------------------
    #  Gets the sub-menus for the 'Restore layout' and 'Delete layout' menu
    #  options:
    #---------------------------------------------------------------------------

    def _get_layout_menus ( self ):
        """ Gets the sub-menus for the 'Restore layout' and 'Delete layout' menu
            options.
        """
        names = self._get_layout_names()
        if len( names ) == 0:
            restore_actions = [ Action( name = '<empty>', enabled = False ) ]
            delete_actions  = [ Action( name = '<empty>', enabled = False ) ]
        else:
            names.sort()
            restore_actions = [ Action(
                                    name   = name,
                                    action = "self.on_restore_layout(%s)" %
                                             repr( name ) )
                                for name in names ]
            delete_actions  = [ Action(
                                    name   = name,
                                    action = "self.on_delete_layout(%s)" %
                                             repr( name ) )
                                for name in names ]
        return [ Menu( name = 'Restore Layout', *restore_actions ),
                 Menu( name = 'Delete Layout',  *delete_actions ) ]

#-- Drag and drop event handlers: ----------------------------------------------

    #---------------------------------------------------------------------------
    #  Handles a Python object being dropped on the control:
    #---------------------------------------------------------------------------

    def wx_dropped_on ( self, x, y, data, drag_result ):
        """ Handles a Python object being dropped on the window.
        """
        if isinstance( data, ( IDockUIProvider, DockControl ) ):
            window    = self.control
            dock_info = self._dock_info

            # See the 'wx_drag_leave' method for an explanation of this code:
            if dock_info is None:
                dock_info = self._leave_info

            dock_info.draw( window )
            self._dock_info = None
            try:
                control = self.handler.dock_control_for(
                                       *(self.handler_args + ( window, data )) )
                # Safely check to see if the object quacks like a Binding
                binding = getattr( clipboard, 'node', None )
                if (hasattr(binding, "obj") and (binding.obj is data) and
                        hasattr(binding, "namespace_name")):
                    control.id = '@@%s' % binding.namespace_name
                dock_info.dock( control, window )
                return drag_result
            except:
                warning( window,
                         "An error occurred while attempting to add an item of "
                         "type '%s' to the window." % data.__class__.__name__,
                         title = 'Cannot add item to window' )

        return wx.DragNone

    #---------------------------------------------------------------------------
    #  Handles a Python object being dragged over the control:
    #---------------------------------------------------------------------------

    def wx_drag_any ( self, x, y, data, drag_result ):
        """ Handles a Python object being dragged over the control.
        """
        ui_provider = isinstance( data, IDockUIProvider )
        if ui_provider or isinstance( data, DockControl ):
            if (ui_provider and
               (not self.handler.can_drop( *(self.handler_args + ( data, )) ))):
                return wx.DragNone

            # Check to see if we are in 'drag mode' yet:
            cur_dock_info = self._dock_info
            if cur_dock_info is None:
                cur_dock_info = no_dock_info
                if isinstance( data, DockControl ):
                    self._dock_size = data.tab_width
                else:
                    self._dock_size = 80

            # Get the window and DockInfo object associated with the event:
            window          = self.control
            self._dock_info = dock_info = \
                              self.sizer.DockInfoAt( x, y, self._dock_size,
                                                     False )

            # If the DockInfo has changed, then update the screen:
            if ((cur_dock_info.kind != dock_info.kind)         or
                (cur_dock_info.region is not dock_info.region) or
                (cur_dock_info.bounds != dock_info.bounds)     or
                (cur_dock_info.tab_bounds != dock_info.tab_bounds)):

                # Erase the old region:
                cur_dock_info.draw( window )

                # Draw the new region:
                dock_info.draw( window )

            return drag_result

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
        if self._dock_info is not None:
            self._dock_info.draw( self.control )

            # Save the current '_dock_info' in '_leave_info' because under
            # Linux the drag and drop code sends a spurious 'drag_leave' event
            # immediately before a 'dropped_on' event, so we need to remember
            # the '_dock_info' value just in case the next event is
            # 'dropped_on':
            self._leave_info, self._dock_info = self._dock_info, None

#-- Pyface menu interface implementation ---------------------------------------

    #---------------------------------------------------------------------------
    #  Adds a menu item to the menu bar being constructed:
    #---------------------------------------------------------------------------

    def add_to_menu ( self, menu_item ):
        """ Adds a menu item to the menu bar being constructed.
        """
        pass

    #---------------------------------------------------------------------------
    #  Adds a tool bar item to the tool bar being constructed:
    #---------------------------------------------------------------------------

    def add_to_toolbar ( self, toolbar_item ):
        """ Adds a tool bar item to the tool bar being constructed.
        """
        pass

    #---------------------------------------------------------------------------
    #  Returns whether the menu action should be defined in the user interface:
    #---------------------------------------------------------------------------

    def can_add_to_menu ( self, action ):
        """ Returns whether the action should be defined in the user interface.
        """
        return True

    #---------------------------------------------------------------------------
    #  Returns whether the toolbar action should be defined in the user
    #  interface:
    #---------------------------------------------------------------------------

    def can_add_to_toolbar ( self, action ):
        """ Returns whether the toolbar action should be defined in the user
            interface.
        """
        return True

    #---------------------------------------------------------------------------
    #  Performs the action described by a specified Action object:
    #---------------------------------------------------------------------------

    def perform ( self, action_object ):
        """ Performs the action described by a specified Action object.
        """
        action = action_object.action
        if action[ : 5 ] == 'self.':
            eval( action, globals(), { 'self': self._menu_self } )
        else:
            method = getattr( self, action )
            try:
                method()
            except:
                method( action_object )

#-- Property implementations ---------------------------------------------------

    #---------------------------------------------------------------------------
    #  Implementation of the 'sizer' property:
    #---------------------------------------------------------------------------

    def _get_sizer ( self ):
        if self.control is not None:
            return self.control.GetSizer()
        return None

    def _set_sizer ( self, sizer ):
        self.control.SetSizer( sizer )

#-- Private methods ------------------------------------------------------------

    #---------------------------------------------------------------------------
    #  Finds the first group with any hidden items (if any):
    #---------------------------------------------------------------------------

    def _hidden_group_for ( self, group ):
        """ Finds the first group with any hidden items (if any).
        """
        while True:
            if group is None:
                return None
            if len( group.contents ) > len( group.visible_contents ):
                return group
            group = group.parent

    #---------------------------------------------------------------------------
    #  Returns a feature that the pointer is over and which can accept the
    #  specified data:
    #---------------------------------------------------------------------------

    def _can_drop_on_feature ( self, x, y, data ):
        """ Returns a feature that the pointer is over and which can accept the
            specified data.
        """
        if self.sizer is not None:
            object = self.sizer.ObjectAt( x, y )
            if isinstance( object, DockControl ):
                event = FakeEvent( x, y, self.control )

                if object.feature_activate( event, data ):
                    ldc = self._last_dock_control
                    if (ldc is not None) and (ldc is not object):
                        ldc.reset_feature_popup()
                    self._last_dock_control = object
                    return None

        if self._last_dock_control is not None:
            self._last_dock_control.reset_feature_popup()
            self._last_dock_control = None

        return None

#-------------------------------------------------------------------------------
#  'FakeEvent' class:
#-------------------------------------------------------------------------------

class FakeEvent ( object ):

    def __init__ ( self, x, y, object ):
        self.x, self.y, self.object = x, y, object

    def GetX ( self ): return self.x
    def GetY ( self ): return self.y
    def GetEventObject ( self ): return self.object

#-------------------------------------------------------------------------------
#  'ControlInfo' class:
#-------------------------------------------------------------------------------

class ControlInfo ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Name to be edited:
    name = Str

    # Has the user set the name of the control?
    user_name = false
    id = Str

    # Style of drag bar/tab:
    style = DockStyle

    # Has the user set the style for this control:
    user_style = false

    #---------------------------------------------------------------------------
    #  Traits view definition:
    #---------------------------------------------------------------------------

    traits_view = View( VGroup(
                            HGroup( HGroup( 'name<100>{Label}', '3' ),
                                    HGroup( 'user_name{Remember label}',
                                            show_left = False ) ),
                            HGroup( HGroup( 'style<101>', '3' ),
                                    HGroup( 'user_style{Remember style}',
                                            show_left = False ) ) ),
                        title   = 'Edit properties',
                        kind    = 'modal',
                        buttons = [ 'OK', 'Cancel' ] )

