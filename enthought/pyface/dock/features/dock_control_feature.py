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
#  Date:   07/16/2006
#
#-------------------------------------------------------------------------------
  
"""  Initializes any trait of an object with 'dock_control = True' metadata
     to point to the object's DockControl.
"""     

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

