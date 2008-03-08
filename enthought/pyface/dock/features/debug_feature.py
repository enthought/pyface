#-------------------------------------------------------------------------------
#
#  Copyright (c) 2006, Enthought, Inc.
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
#  Date:   07/04/2006
#
#-------------------------------------------------------------------------------

""" Adds a 'debug' feature to DockWindow which exposes the object associated
    with a DockControl as a draggable item. This can be used to facilitate
    debugging when used in conjunction with other plugins such as 'object
    source' and 'universal inspector'.
"""    

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import Any, Enum, Property

from enthought.traits.ui.api \
    import View, Item, ValueEditor

from enthought.traits.ui.menu \
    import NoButtons, Menu, Action

from enthought.pyface.dock.api \
    import DockWindow, DockWindowFeature, IDockUIProvider

from enthought.pyface.image_resource \
    import ImageResource

from enthought.developer.api \
    import HasPayload

#-------------------------------------------------------------------------------
#  Context menu definition:
#-------------------------------------------------------------------------------

object_action = Action(
    name   = 'Object',
    action = "self.set(mode='object')",
    style  = 'toggle'
)

dock_control_action = Action(
    name   = 'DockControl',
    action = "self.set(mode='dock_control')",
    style  = 'toggle'
)

window_action = Action(
    name   = 'Window',
    action = "self.set(mode='window')",
    style  = 'toggle'
)

ui_action = Action(
    name   = 'Traits UI',
    action = "self.set(mode='ui')",
    style  = 'toggle'
)

context_menu = Menu(
    object_action,
    dock_control_action,
    window_action,
    ui_action,
    name = 'popup'
)

#-------------------------------------------------------------------------------
#  Images:
#-------------------------------------------------------------------------------

feature_images = {
    'object':       ImageResource( 'debug_object_feature' ),
    'dock_control': ImageResource( 'debug_dock_control_feature' ),
    'window':       ImageResource( 'debug_window_feature' ),
    'ui':           ImageResource( 'debug_ui_feature' )
}

#-------------------------------------------------------------------------------
#  'DebugFeature' class:
#-------------------------------------------------------------------------------

class DebugFeature ( DockWindowFeature ):

    #---------------------------------------------------------------------------
    #  Class variables:
    #---------------------------------------------------------------------------

    # The user interface name of the feature:
    feature_name = 'Debug'

    # Current feature state (0 = uninstalled, 1 = active, 2 = disabled):
    state = 2

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The 'payload' mode:
    mode = Enum( 'object', 'dock_control', 'window', 'ui' )

    # The current payload value:
    payload = Property

    # The current image to display on the feature bar:
    image = ImageResource( 'debug_object_feature' )

    # The tooltip to display when the mouse is hovering over the image:
    tooltip = ("Drag the selected debug object.                    \n"
               "Ctrl-drag the tab's object.\n"
               "Shift-drag the tab's DockControl.\n"
               "Alt-drag the tab's window.\n"
               "Click to create a pop-up view of the object.\n"
               "Right click to set the debug options.")

    #---------------------------------------------------------------------------
    #  Implementation of the 'payload' property:
    #---------------------------------------------------------------------------

    def _get_payload ( self ):
        payload = self.dock_control

        if self.mode == 'object':
            return payload.object

        if self.mode == 'window':
            return payload.control

        if self.mode == 'ui':
            return getattr( payload.control, '_ui', None )

        return payload

    #---------------------------------------------------------------------------
    #  Handles the user left clicking on the feature image:
    #---------------------------------------------------------------------------

    def click ( self ):
        """ Handles the user left clicking on the feature image.
        """

        ObjectInspector( payload = self.payload ).edit_traits(
            parent = self.dock_control.control
        )

    #---------------------------------------------------------------------------
    #  Handles the user right clicking on the feature image:
    #---------------------------------------------------------------------------

    def right_click ( self ):
        """ Handles the user right clicking on the feature image.
        """
        object_action.checked       = (self.mode == 'object')
        dock_control_action.checked = (self.mode == 'dock_control')
        window_action.checked       = (self.mode == 'window')
        ui_action.checked           = (self.mode == 'ui')
        ui_action.enabled           = (getattr( self.dock_control.control,
                                                '_ui', None ) is not None)
        self.popup_menu( context_menu )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags feature image:
    #---------------------------------------------------------------------------

    def drag ( self ):
        """ Returns the object to be dragged when the user drags feature image.
        """
        return ObjectInspector( payload = self.payload )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  while holding down the 'Ctrl' key:
    #---------------------------------------------------------------------------

    def control_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image while holding down the 'Ctrl' key:
        """
        return ObjectInspector( payload = self.dock_control.object )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  while holding down the 'Shift' key:
    #---------------------------------------------------------------------------

    def shift_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image while holding down the 'Shift' key.
        """
        return ObjectInspector( payload = self.dock_control )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  while holding down the 'Alt' key:
    #---------------------------------------------------------------------------

    def alt_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image while holding down the 'Alt' key:
        """
        return ObjectInspector( payload = self.dock_control.control )

#-- Overidable Class Methods ---------------------------------------------------

    #---------------------------------------------------------------------------
    #  Returns whether or not the DockWindowFeature is a valid feature for a
    #  specified DockControl:
    #---------------------------------------------------------------------------

    def is_feature_for ( self, dock_control ):
        """ Returns whether or not the DockWindowFeature is a valid feature for
            a specified DockControl.
        """
        return (dock_control.object is not None)

    is_feature_for = classmethod( is_feature_for )

#-- Event Handlers -------------------------------------------------------------

    def _mode_changed ( self, mode ):
        self.image = feature_images[ mode ]
        self.refresh()

#-------------------------------------------------------------------------------
#  'ObjectInspector' class:
#-------------------------------------------------------------------------------

class ObjectInspector ( HasPayload ):

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
        Item( 'payload',
              show_label = False,
              editor     = ValueEditor()
        ),
        title     = 'Object Inspector',
        id        = 'enthought.developer.tools.debug_inspector.ObjectInspector',
        kind      = 'live',
        resizable = True,
        width     = 0.3,
        height    = 0.4,
        buttons   = NoButtons
    )

#-------------------------------------------------------------------------------
#  'DockableObjectInspector' class:
#-------------------------------------------------------------------------------

class DockableObjectInspector ( ObjectInspector, IDockUIProvider ):

    pass

