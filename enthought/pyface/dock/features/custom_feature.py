#-------------------------------------------------------------------------------
#
#  Adds a 'custom' feature to DockWindow which allows views to contribute
#  custom features to their own tab.
#
#  Written by: David C. Morrill
#
#  Date: 07/16/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Property, Instance, Str, true

from enthought.traits.ui.api \
    import View

from enthought.pyface.dock.api \
    import DockWindowFeature

from enthought.pyface.image_resource \
    import ImageResource

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Standard sequence types:
SequenceTypes = ( list, tuple )

#-------------------------------------------------------------------------------
#  'CustomFeature' class:
#-------------------------------------------------------------------------------

class CustomFeature ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The current image to display on the feature bar:
    image = Instance( ImageResource, allow_none = True )

    # The tooltip to display when the mouse is hovering over the image:
    tooltip = Str

    # Is the feature currently enabled?
    enabled = true

    # Name of the method to invoke on a left click:
    click = Str

    # Name of the method to invoke on a right click:
    right_click = Str

    # Name of the method to invoke when the user starts to drag with the left
    # mouse button:
    drag = Str

    # Name of the method to invoke when the user starts to ctrl-drag with the
    # left mouse button:
    control_drag = Str

    # Name of the method to invoke when the user starts to shift-drag with the
    # left mouse button:
    shift_drag = Str

    # Name of the method to invoke when the user starts to alt-drag with the
    # left mouse button:
    alt_drag = Str

    # Name of the method to invoke when the user starts to drag with the right
    # mouse button:
    right_drag = Str

    # Name of the method to invoke when the user starts to ctrl-drag with the
    # right mouse button:
    control_right_drag = Str

    # Name of the method to invoke when the user starts to shift-drag with the
    # right mouse button:
    shift_right_drag = Str

    # Name of the method to invoke when the user starts to alt-drag with the
    # right mouse button:
    alt_right_drag = Str

    # Name of the method to invoke when the user drops an object:
    drop = Str

    # Name of the method to invoke to see if the user can drop an object:
    can_drop = Str

#-------------------------------------------------------------------------------
#  'ACustomFeature' class:
#-------------------------------------------------------------------------------

class ACustomFeature ( DockWindowFeature ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The CustomFeature associated with this feature:
    custom_feature = Instance( CustomFeature )

    # The current image to display on the feature bar:
    image = Property

    # The tooltip to display when the mouse is hovering over the image:
    tooltip = Property

#-- Property Implementations ---------------------------------------------------

    def _get_image ( self ):
        if self.custom_feature.enabled:
            return self.custom_feature.image

        return None

    def _get_tooltip ( self ):
        return self.custom_feature.tooltip

#-- Overrides of DockWindowFeature Methods -------------------------------------

    #---------------------------------------------------------------------------
    #  Handles the user left clicking on the feature image:
    #---------------------------------------------------------------------------

    def click ( self ):
        """ Handles the user left clicking on the feature image.
        """
        self.dynamic_call( 'click' )

    #---------------------------------------------------------------------------
    #  Handles the user right clicking on the feature image:
    #---------------------------------------------------------------------------

    def right_click ( self ):
        """ Handles the user right clicking on the feature image.
        """
        self.dynamic_call( 'right_click' )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the left mouse button:
    #---------------------------------------------------------------------------

    def drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image with the left mouse button.
        """
        return self.dynamic_call( 'drag', None )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the left mouse button while holding down the 'Ctrl' key:
    #---------------------------------------------------------------------------

    def control_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image with the left mouse button while holding down the 'Ctrl' key:
        """
        return self.dynamic_call( 'control_drag', None )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the left mouse button while holding down the 'Shift' key:
    #---------------------------------------------------------------------------

    def shift_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image with the left mouse button while holding down the 'Shift' key.
        """
        return self.dynamic_call( 'shift_drag', None )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the left mouse button while holding down the 'Alt' key:
    #---------------------------------------------------------------------------

    def alt_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image with the left mouse button while holding down the 'Alt' key:
        """
        return self.dynamic_call( 'alt_drag', None )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the right mouse button:
    #---------------------------------------------------------------------------

    def right_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image with the right mouse button.
        """
        return self.dynamic_call( 'right_drag', None )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the right mouse button while holding down the 'Ctrl' key:
    #---------------------------------------------------------------------------

    def control_right_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image with the right mouse button while holding down the 'Ctrl' key:
        """
        return self.dynamic_call( 'control_right_drag', None )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the right mouse button while holding down the 'Shift' key:
    #---------------------------------------------------------------------------

    def shift_right_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image with the right mouse button while holding down the 'Shift'
            key.
        """
        return self.dynamic_call( 'shift_right_drag', None )

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the right mouse button while holding down the 'Alt' key:
    #---------------------------------------------------------------------------

    def alt_right_drag ( self ):
        """ Returns the object to be dragged when the user drags the feature
            image with the right mouse button while holding down the 'Alt' key:
        """
        return self.dynamic_call( 'alt_right_drag', None )

    #---------------------------------------------------------------------------
    #  Handles the user dropping a specified object on the feature image:
    #---------------------------------------------------------------------------

    def drop ( self, object ):
        """ Handles the user dropping a specified object on the feature image.
        """
        return self.dynamic_call( 'drop', args = ( object, ) )

    #---------------------------------------------------------------------------
    #  Returns whether a specified object can be dropped on the feature image:
    #---------------------------------------------------------------------------

    def can_drop ( self, object ):
        """ Returns whether a specified object can be dropped on the feature
            image.
        """
        return self.dynamic_call( 'can_drop', False, args = ( object, ) )

    #---------------------------------------------------------------------------
    #  Performs any clean-up needed when the feature is being removed:
    #---------------------------------------------------------------------------

    def dispose ( self ):
        """ Performs any clean-up needed when the feature is being removed.
        """
        self.custom_feature.on_trait_change( self._custom_feature_updated,
                                             remove = True )

#-- ACustomFeature Methods ------------------------------------------------------

    #---------------------------------------------------------------------------
    #  Performs a method invocation using the associated CustomFeature:
    #---------------------------------------------------------------------------

    def dynamic_call ( self, method, default = None, args = () ):
        """ Performs a method invocation using the associated CustomFeature.
        """
        method = getattr( self.custom_feature, method )
        if method == '':
            return default

        return getattr( self.dock_control.object, method )( *args )

    #---------------------------------------------------------------------------
    #  Handles the 'custom_feature' trait being changed:
    #---------------------------------------------------------------------------

    def _custom_feature_changed ( self, custom_feature ):
        """ Handles the 'custom_feature' trait being changed.
        """
        custom_feature.on_trait_change( self._custom_feature_updated )

    #---------------------------------------------------------------------------
    #  Handles any trait on the associated dynamic feature being changed:
    #---------------------------------------------------------------------------

    def _custom_feature_updated ( self, object, name, old, new ):
        """ Handles any trait on the associated dynamic feature being changed.
        """
        self._bitmap = None
        self.refresh()

#-- Overidable Class Methods ---------------------------------------------------

    #---------------------------------------------------------------------------
    #  Returns a feature object for use with the specified DockControl (or None
    #  if the feature does not apply to the DockControl object):
    #---------------------------------------------------------------------------

    def feature_for ( cls, dock_control ):
        """ Returns a feature object for use with the specified DockControl (or
            None if the feature does not apply to the DockControl object).
        """
        from enthought.pyface.dock.features.api import is_not_none

        object = dock_control.object
        if isinstance( object, HasTraits ):
            result = []
            for name in object.trait_names( custom_feature = is_not_none ):
                custom_feature = getattr( object, name, None )
                if isinstance( custom_feature, CustomFeature ):
                    result.append( cls( dock_control   = dock_control,
                                        custom_feature = custom_feature ) )
                elif isinstance( custom_feature, SequenceTypes ):
                    for feature in custom_feature:
                        if isinstance( feature, CustomFeature ):
                            result.append( cls( dock_control   = dock_control,
                                                custom_feature = feature ) )

            return result

        return None

    feature_for = classmethod( feature_for )

