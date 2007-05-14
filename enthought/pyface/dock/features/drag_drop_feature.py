#-------------------------------------------------------------------------------
#  
#  Adds a 'drag and drop' feature to DockWindow which exposes traits on the 
#  object associated with a DockControl as draggable or droppable items. If the
#  object contains one or more traits with 'draggable' metadata, then the value
#  of those traits will be draggable. If the object contains one or more traits
#  with 'droppable' metadata, then each trait that will accept a specified item
#  will receive that item when it is dropped on the feature.
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
    import HasStrictTraits, HasTraits, List, Str
    
from enthought.pyface.dock.api \
    import DockWindowFeature
    
from enthought.pyface.image_resource \
    import ImageResource
    
#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Feature settings:
settings = (
    ImageResource( 'drag_feature' ),
    ImageResource( 'drop_feature' ),
    ImageResource( 'dragdrop_feature' )
)
    
#-------------------------------------------------------------------------------
#  'MultiDragDrop' class:
#-------------------------------------------------------------------------------

class MultiDragDrop ( HasStrictTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # LIst of object being dragged:
    objects = List

#-------------------------------------------------------------------------------
#  'DragDropFeature' class:
#-------------------------------------------------------------------------------

class DragDropFeature ( DockWindowFeature ):
    
    #---------------------------------------------------------------------------
    #  Class variables:  
    #---------------------------------------------------------------------------

    # The user interface name of the feature:
    feature_name = 'Drag and Drop'
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The names of the object traits to drag from:
    drag_traits = List( Str )
    
    # The names of the object traits that can be dropped on:
    drop_traits = List( Str )
    
    #---------------------------------------------------------------------------
    #  Returns the object to be dragged when the user drags feature image:
    #---------------------------------------------------------------------------
    
    def drag ( self ):
        """ Returns the object to be dragged when the user drags feature image.
        """
        item = self.dock_control.object
        n    = len( self.drag_traits )
        
        if n == 1:
            return getattr( item, self.drag_traits[0], None )
            
        if n > 1:
            objects = []
            for trait in self.drag_traits:
                object = getattr( item, trait, None )
                if object is not None:
                    objects.append( object )
            if len( objects ) == 1:
                return objects[0]
            if len( objects ) > 1:
                return MultiDragDrop( objects = objects )
            
        return None
        
    #---------------------------------------------------------------------------
    #  Handles the user dropping a specified object on the feature image:  
    #---------------------------------------------------------------------------

    def drop ( self, object ):
        """ Handles the user dropping a specified object on the feature image.
        """
        item        = self.dock_control.object
        drop_traits = self.drop_traits
            
        if isinstance( object, MultiDragDrop ):
            for drag in object.objects:
                 for drop_trait in drop_traits:
                     try:
                         setattr( item, drop_trait, drag )
                     except:
                         pass
        else:
             for drop_trait in drop_traits:
                 try:
                     setattr( item, drop_trait, object )
                 except:
                     pass
        
    #---------------------------------------------------------------------------
    #  Returns whether a specified object can be dropped on the feature image:  
    #---------------------------------------------------------------------------
 
    def can_drop ( self, object ):
        """ Returns whether a specified object can be dropped on the feature 
            image.
        """
        item        = self.dock_control.object
        drop_traits = self.drop_traits
        
        if isinstance( object, MultiDragDrop ):
            for drag in object.objects:
                for drop_trait in drop_traits:
                    try:
                        item.base_trait( drop_trait ).validate( item,
                                                              drop_trait, drag )
                        return True
                    except:
                        pass
        else:
            for drop_trait in drop_traits:
                try:
                    item.base_trait( drop_trait ).validate( item, drop_trait, 
                                                            object )
                    return True
                except:
                    pass
            
        return False

#-- Overidable Class Methods ---------------------------------------------------

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
            drag_tooltip = drop_tooltip = ''
            drag_traits  = []
            drop_traits  = []
            
            traits = object.traits( draggable = is_not_none )
            if len( traits ) >= 1:
                drag_traits = traits.keys()
                drag_traits.sort()
                drag_tooltips = [ trait.draggable for trait in traits.values()
                                  if isinstance( trait.draggable, str ) ]
                if len( drag_tooltips ) > 0:
                    drag_tooltip = '\n'.join( drag_tooltips )
                if drag_tooltip == '':
                    drag_tooltip = 'Drag this item.'
                drag_tooltip += '\n'
                
            traits = object.traits( droppable = is_not_none )
            if len( traits ) >= 1:
                drop_traits = traits.keys()
                drop_traits.sort()
                drop_tooltips = [ trait.droppable for trait in traits.values()
                                  if isinstance( trait.droppable, str ) ]
                if len( drop_tooltips ) > 0:
                    drop_tooltip = '\n'.join( drop_tooltips )
                if drop_tooltip == '':
                    drop_tooltip = 'Drop an item here.'
                
            if (drag_tooltip != '') or (drop_tooltip != ''):
                i = 1
                if drag_tooltip != '':
                    i = 0
                    if drop_tooltip != '':
                        i = 2
            
                return cls( dock_control = dock_control,
                            image        = settings[i],
                            tooltip      = (drag_tooltip+drop_tooltip).strip(),
                            drag_traits  = drag_traits,
                            drop_traits  = drop_traits )
            
        return None
        
    feature_for = classmethod( feature_for )

