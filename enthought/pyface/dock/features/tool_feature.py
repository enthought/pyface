#-------------------------------------------------------------------------------
#  
#  Adds a 'tool' feature to DockWindow which allows views to contribute
#  tools based on the IFeatureTool interface to their feature tab.
#  
#  Written by: David C. Morrill
#  
#  Date: 02/08/2007
#  
#  (c) Copyright 2007 by David C. Morrill
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, HasStrictTraits, Str, Instance, TraitFactory
    
from enthought.pyface.dock.api \
    import DockWindowFeature, IFeatureTool
    
from enthought.pyface.image_resource \
    import ImageResource
    
#-------------------------------------------------------------------------------
#  'ToolDescription' class:
#-------------------------------------------------------------------------------

class ToolDescription ( HasStrictTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The prefix to apply to each method in the IToolFeature interface:
    prefix = Str( 'feature' )
    
    # The tool's image:
    image = Instance( ImageResource, ( 'tool_feature', ) )
    
    # The tool's tooltip:
    tooltip = Str( 'Drag and drop this tool on a view' )
            
#-------------------------------------------------------------------------------
#  'tool' metadata filter:
#-------------------------------------------------------------------------------
        
def is_tool_description ( value ):
    return isinstance( value, ToolDescription )    
    
#-------------------------------------------------------------------------------
#  'ToolFeature' class:
#-------------------------------------------------------------------------------

class ToolFeature ( DockWindowFeature, IFeatureTool ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The prefix to apply to each method in the IToolFeature interface:
    prefix = Str( 'feature' )
    
#-- Overrides of DockWindowFeature Methods -------------------------------------

    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags the feature image
    #  with the left mouse button:
    #---------------------------------------------------------------------------
    
    def drag ( self ):
        """ Returns the object to be dragged when the user drags the feature 
            image with the left mouse button.
        """
        return self
        
#-- Implementation of the IFeatureTool Interface -------------------------------        
    
    #---------------------------------------------------------------------------
    #  Returns whether or not the object being dragged (i.e. self) can be 
    #  dropped on the specified target object:
    #---------------------------------------------------------------------------
        
    def feature_can_drop_on ( self, object ):
        """ Returns whether or not the object being dragged (i.e. self) can be 
            dropped on the specified target object.
        """
        return self._dynamic_call( 'can_drop_on', object )
    
    #---------------------------------------------------------------------------
    #  Returns whether or not the object being dragged (i.e. self) can be 
    #  dropped on the specified target object's DockControl:
    #---------------------------------------------------------------------------
        
    def feature_can_drop_on_dock_control ( self, dock_control ):
        """ Returns whether or not the object being dragged (i.e. self) can be 
            dropped on the specified target object's DockControl.
        """
        return self._dynamic_call( 'can_drop_on_dock_control', dock_control )
        
    #---------------------------------------------------------------------------
    #  Allows the dragged object (i.e. self) to handle being dropped on the
    #  specified target object:
    #---------------------------------------------------------------------------
                    
    def feature_dropped_on ( self, object ):
        """ Allows the dragged object (i.e. self) to handle being dropped on the
            specified target object.
        """
        self._dynamic_call( 'dropped_on', object )
        
    #---------------------------------------------------------------------------
    #  Allows the dragged object (i.e. self) to handle being dropped on the
    #  specified target object's DockControl:
    #---------------------------------------------------------------------------
                    
    def feature_dropped_on_dock_control ( self, dock_control ):
        """ Allows the dragged object (i.e. self) to handle being dropped on the
            specified target object's DockControl.
        """
        self._dynamic_call( 'dropped_on_dock_control', dock_control )
        
#-- Private Methods ------------------------------------------------------------

    #---------------------------------------------------------------------------
    #  Attempts to delegate the specified IToolFeature method to the associated
    #  object using the prefix specified in the trait metadata:
    #---------------------------------------------------------------------------
    
    def _dynamic_call ( self, method, data ):
        method = getattr( self.dock_control.object, 
                          '%s_%s' % ( self.prefix, method ), None )
        if method is not None:
            return method( data )
            
        return False

#-- Overridable Class Methods --------------------------------------------------

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
            for name in object.trait_names( tool = is_tool_description ): 
                td = object.trait( name ).tool
                result.append( cls( dock_control = dock_control,
                                    prefix       = td.prefix,
                                    image        = td.image,
                                    tooltip      = td.tooltip ) )
                                        
            return result
            
        return None
        
    feature_for = classmethod( feature_for )
    
#-------------------------------------------------------------------------------
#  Defines a 'Tool' trait for easily adding tools to a class definition:
#-------------------------------------------------------------------------------

def Tool ( prefix  = 'feature', 
           image   = ImageResource( 'tool_feature' ),
           tooltip = 'Drag and drop this tool on a view', 
           **metadata ):
    return Str( tool = ToolDescription( prefix  = prefix,
                                        image   = image,
                                        tooltip = tooltip ), **metadata )
                                        
Tool = TraitFactory( Tool )

