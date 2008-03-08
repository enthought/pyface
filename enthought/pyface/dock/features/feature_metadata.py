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
#  Date:   07/21/2006
#
#-------------------------------------------------------------------------------
  
""" Classes and functions used to define feature metadata values or options.
"""

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

