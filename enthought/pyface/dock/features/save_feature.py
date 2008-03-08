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
#  Date:   07/08/2006
#
#-------------------------------------------------------------------------------
  
""" Adds an 'save' feature to DockWindow which displays a 'save' image whenever
    the associated object sets its 'needs_save' trait True. Then when the user
    clicks the 'save' image, the feature calls the object's 'save' method.
"""    

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.pyface.dock.api \
    import DockWindowFeature
    
from enthought.pyface.image_resource \
    import ImageResource
    
from enthought.developer.api \
    import Saveable

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

save_feature = ImageResource( 'save_feature' )

#-------------------------------------------------------------------------------
#  'SaveFeature' class:
#-------------------------------------------------------------------------------

class SaveFeature ( DockWindowFeature ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # The tooltip to display when the mouse is hovering over the image:
    tooltip = 'Click to save.'
    
    #---------------------------------------------------------------------------
    #  Initializes the object:  
    #---------------------------------------------------------------------------

    def __init__ ( self, **traits ):
        """ Initializes the object.
        """
        super( SaveFeature, self ).__init__( **traits )
        self.dock_control.object.on_trait_change( self._needs_save_changed,
                                                  'needs_save' )
                                                  
    #---------------------------------------------------------------------------
    #  Handles the object's 'needs_save' trait being changed:  
    #---------------------------------------------------------------------------

    def _needs_save_changed ( self, needs_save ):
        """ Handles the object's 'needs_save' trait being changed.
        """
        if needs_save:
            self.image = save_feature
        else:
            self.image = None
        self.refresh()

    #---------------------------------------------------------------------------
    #  Handles the user left clicking on the feature image:    
    #---------------------------------------------------------------------------
    
    def click ( self ):
        """ Handles the user left clicking on the feature image.
        """
        self.dock_control.object.save()

#-- Overidable Class Methods ---------------------------------------------------
    
    #---------------------------------------------------------------------------
    #  Returns whether or not the DockWindowFeature is a valid feature for a 
    #  specified DockControl:  
    #---------------------------------------------------------------------------

    def is_feature_for ( self, dock_control ):
        """ Returns whether or not the DockWindowFeature is a valid feature for 
            a specified DockControl.
        """
        return isinstance( dock_control.object, Saveable )
        
    is_feature_for = classmethod( is_feature_for )

