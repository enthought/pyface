#-------------------------------------------------------------------------------
#  
#  Classes and functions used to define feature metadata values or options.
#  
#  Written by: David C. Morrill
#  
#  Date: 07/21/2006
#  
#  (c) Copyright 2006 by David C. Morrill
#  
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasStrictTraits, List, Str, false
    
#-------------------------------------------------------------------------------
#  Metadata filters:  
#-------------------------------------------------------------------------------
        
def is_not_none ( value ):
    return (value is not None)
    
#-------------------------------------------------------------------------------
#  'DropFile' class:
#-------------------------------------------------------------------------------

class DropFile ( HasStrictTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # List of valid droppable file extensions:
    extensions = List( Str )
    
    # Is the trait also draggable?
    draggable = false
    
    # The tooltip to use for the feature:
    tooltip = Str

