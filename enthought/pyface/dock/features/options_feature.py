#-------------------------------------------------------------------------------
#
#  Adds an 'options' feature to DockWindow which allows users to configure
#  a view's options if the object associated with a DockControl has an
#  'options' view.
#
#  Written by: David C. Morrill
#
#  Date: 07/04/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits

from enthought.traits.ui.api \
    import View

from enthought.pyface.dock.api \
    import DockWindowFeature

from enthought.pyface.image_resource \
    import ImageResource

#-------------------------------------------------------------------------------
#  'OptionsFeature' class:
#-------------------------------------------------------------------------------

class OptionsFeature ( DockWindowFeature ):

    #---------------------------------------------------------------------------
    #  Class variables:
    #---------------------------------------------------------------------------

    # The user interface name of the feature:
    feature_name = 'Options'

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The current image to display on the feature bar:
    image = ImageResource( 'options_feature' )

    # The tooltip to display when the mouse is hovering over the image:
    tooltip = 'Click to set view options.'

    #---------------------------------------------------------------------------
    #  Handles the user left clicking on the feature image:
    #---------------------------------------------------------------------------

    def click ( self ):
        """ Handles the user left clicking on the feature image.
        """
        self.dock_control.object.edit_traits(
            view   = 'options',
            kind   = 'livemodal',
            parent = self.dock_control.control
        )

#-- Overidable Class Methods ---------------------------------------------------

    #---------------------------------------------------------------------------
    #  Returns whether or not the DockWindowFeature is a valid feature for a
    #  specified DockControl:
    #---------------------------------------------------------------------------

    def is_feature_for ( self, dock_control ):
        """ Returns whether or not the DockWindowFeature is a valid feature for
            a specified DockControl.
        """
        object = dock_control.object
        return (isinstance( object, HasTraits ) and
                isinstance( object.trait_view( 'options' ), View ))

    is_feature_for = classmethod( is_feature_for )

