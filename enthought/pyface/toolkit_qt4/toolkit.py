#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Internal Enthought library imports.
from enthought.pyface.toolkit import Toolkit

# Local imports.
from action.menu_manager import MenuManager_qt4
from action.tool_bar_manager import ToolBarManager_qt4


class Toolkit_qt4(Toolkit):
    """ Implementation of the PyQt v4 toolkit. """

    MenuManager = MenuManager_qt4
    ToolBarManager = ToolBarManager_qt4

    def init_toolkit(self, *args, **kw):
        pass
