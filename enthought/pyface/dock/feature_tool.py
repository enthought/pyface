#-------------------------------------------------------------------------------
#  
#  Implements the FeatureTool feature that allows a dragged object implementing
#  the IFeatureTool interface to be dropped onto any compatible object.
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
    
from dock_window_feature \
    import DockWindowFeature
    
from enthought.pyface.image_resource \
    import ImageResource

#-------------------------------------------------------------------------------
#  'FeatureTool' class:
#-------------------------------------------------------------------------------

class FeatureTool ( DockWindowFeature ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    image = ImageResource( 'feature_tool' )
        
    #---------------------------------------------------------------------------
    #  Returns whether a specified object can be dropped on the feature image:  
    #---------------------------------------------------------------------------
 
    def can_drop ( self, object ):
        """ Returns whether a specified object can be dropped on the feature 
            image.
        """
        return True

