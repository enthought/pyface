#-------------------------------------------------------------------------------
#  
#  Initializes any trait of an object with 'dock_control = True' metadata
#  to point to the object's DockControl.
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
    import HasTraits
    
from enthought.pyface.dock.api \
    import DockWindowFeature
    
#-------------------------------------------------------------------------------
#  'DockControlFeature' class:
#-------------------------------------------------------------------------------

class DockControlFeature ( DockWindowFeature ):

#-- Overidable Class Methods ---------------------------------------------------

    #---------------------------------------------------------------------------
    #  Returns a feature object for use with the specified DockControl (or None 
    #  if the feature does not apply to the DockControl object):   
    #---------------------------------------------------------------------------

    def feature_for ( cls, dock_control ):
        """ Returns a feature object for use with the specified DockControl (or
            None if the feature does not apply to the DockControl object).
        """
        object = dock_control.object
        if isinstance( object, HasTraits ):
            for name in object.trait_names( dock_control = True ):
                try:
                    setattr( object, name, dock_control )
                except:
                    pass
            
        return None
        
    feature_for = classmethod( feature_for )

