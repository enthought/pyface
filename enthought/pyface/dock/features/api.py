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
#  Date:   07/18/2006
#
#-------------------------------------------------------------------------------

""" enthought.pyface.dock.features Core API.
"""

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
    
