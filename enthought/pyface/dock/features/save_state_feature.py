#-------------------------------------------------------------------------------
#  
#  Manages saving/restoring the state of an object. Any traits with metadata
#  'save_state = True' are automatically restored when the feature is applied
#  and saved when they are changed. The traits are saved under the id 
#  specified by a trait with metadata 'save_state_id = True'. If no such trait
#  exists, an id of the form: 'unknown.plugins.?.state', where ? = the name of
#  the object's associated DockControl.
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

import shelve

from os.path \
    import join
    
from enthought.traits.api \
    import HasTraits, List, Str, on_trait_change

from enthought.traits.trait_base \
    import traits_home
    
from enthought.pyface.dock.api \
    import DockWindowFeature

#-------------------------------------------------------------------------------
#  Returns a reference to the traits UI preference database:
#-------------------------------------------------------------------------------

def get_ui_db ( mode = 'r' ):
    """ Returns a reference to the traits UI preference database.
    """
    try:
        return shelve.open( join( traits_home(), 'traits_ui' ),
                            flag = mode, protocol = -1 )
    except:
        return None
    
#-------------------------------------------------------------------------------
#  'SaveStateFeature' class:
#-------------------------------------------------------------------------------

class SaveStateFeature ( DockWindowFeature ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # The persistence id to save the data under:
    id = Str

    # List of traits to save/restore:
    names = List( Str )
    
    #---------------------------------------------------------------------------
    #  Saves the current state of the plugin:  
    #---------------------------------------------------------------------------

    @on_trait_change( 'dock_control:object:+save_state' )
    def save_state ( self ):
        """ Saves the current state of the plugin.
        """
        db = get_ui_db( mode = 'c' )
        if db is not None:
            db[ self.id ] = self.dock_control.object.get( *self.names )
            db.close()
                
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
            names = object.trait_names( save_state = True )
            if len( names ) > 0:
                
                # Get the id to save the options under:
                ids = object.trait_names( save_state_id = True )
                id  = ''
                if len( ids ) == 1:
                    id = getattr( object, ids[0] )
                if id == '':
                    id = 'unknown.plugins.%s.state' % dock_control.name
                    
                # Assign the current saved state (if any) to the object:
                db = get_ui_db()
                if db is not None:
                    try:
                        state = db.get( id )
                        if state is not None:
                            for name, value in state.items():
                                try:
                                    setattr( object, name, value )
                                except:
                                    pass
                    except:
                        pass
                    db.close()
                    
                # Create and return the feature:
                return cls( dock_control = dock_control,
                            id           = id ).set(
                            names        = names )
                            
        return None
        
    feature_for = classmethod( feature_for )

