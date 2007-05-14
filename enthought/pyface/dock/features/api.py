#-------------------------------------------------------------------------------
#  
#  enthought.pyface.dock.features Core API
#  
#  Written by: David C. Morrill
#  
#  Date: 07/18/2006
#  
#  (c) Copyright 2006 by David C. Morrill
#  
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------
    
from enthought.pyface.dock.features.custom_feature \
    import CustomFeature
    
from enthought.pyface.dock.features.drag_drop_feature \
    import MultiDragDrop
    
from enthought.pyface.dock.features.feature_metadata \
    import is_not_none, DropFile
    
from enthought.pyface.dock.features.tool_feature \
    import ToolDescription, Tool
    
from enthought.pyface.dock.features.add_standard_features \
    import add_standard_features
    
