#-------------------------------------------------------------------------------
#
#  Copyright (c) 2007, Enthought, Inc.
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
#  Date:   01/04/2007
#
#-------------------------------------------------------------------------------

""" Helper function to add all standard DockWindowFeature feature classes to
    DockWindow.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from connect_feature      import ConnectFeature
from custom_feature       import ACustomFeature
from debug_feature        import DebugFeature
from dock_control_feature import DockControlFeature
from drag_drop_feature    import DragDropFeature
from drop_file_feature    import DropFileFeature
from options_feature      import OptionsFeature
from popup_menu_feature   import PopupMenuFeature
from save_feature         import SaveFeature
from save_state_feature   import SaveStateFeature
from tool_feature         import ToolFeature

from enthought.pyface.dock.api \
    import add_feature

#-------------------------------------------------------------------------------
#  Adds all of the standard DockWindowFeature feature classes to DockWindow:
#-------------------------------------------------------------------------------

def add_standard_features ( ):
    """ Adds all of the standard DockWindowFeature feature classes to
        DockWindow.
    """
    for klass in [ ConnectFeature, ACustomFeature, DebugFeature,
                   DockControlFeature, DragDropFeature, DropFileFeature,
                   OptionsFeature, PopupMenuFeature, SaveFeature,
                   SaveStateFeature, SaveStateFeature, ToolFeature ]:
        add_feature( klass )
    
