#-------------------------------------------------------------------------------
#  
#  Pyface 'DockWindow' support.  
#  
#  This package implements a Pyface 'dockable' window component that allows
#  child windows to be reorganized within the DockWindow using drag and drop.
#  The component also allows multiple sub-windows to occupy the same sub-region
#  of the DockWindow, in which case each sub-window appears as a separate 
#  notebook-like tab within the region.
#  
#  Written by: David C. Morrill
#  
#  Date: 10/18/2005
#  
#  (c) Copyright 2005 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:  
#-------------------------------------------------------------------------------

from dock_window \
    import DockWindow, DockWindowHandler
    
from dock_sizer \
    import DockSizer, DockSection, DockRegion, DockControl, DockStyle, \
           DOCK_LEFT, DOCK_RIGHT, DOCK_TOP, DOCK_BOTTOM, SetStructureHandler, \
           add_feature, DockGroup

from idockable \
    import IDockable
    
from idock_ui_provider \
    import IDockUIProvider
    
from ifeature_tool \
    import IFeatureTool
    
from dock_window_shell \
    import DockWindowShell
    
from dock_window_feature \
    import DockWindowFeature
    
