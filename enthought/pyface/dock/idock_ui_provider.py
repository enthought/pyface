#-------------------------------------------------------------------------------
#  
#  Defines the IDockUIProvider interface which objects which support being
#  dragged and dropped into a DockWindow must implement.
#  
#  Written by: David C. Morrill
#  
#  Date: 06/17/2006
#  
#  (c) Copyright 2006 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------
#  'IDockUIProvider' class:  
#-------------------------------------------------------------------------------

class IDockUIProvider ( object ):
    
    #---------------------------------------------------------------------------
    #  Returns a Traits UI which a DockWindow can imbed:
    #---------------------------------------------------------------------------
        
    def get_dockable_ui ( self, parent ):
        """ Returns a Traits UI which a DockWindow can imbed.
        """
        return self.edit_traits( parent     = parent,
                                 kind       = 'subpanel', 
                                 scrollable = True )

