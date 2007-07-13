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
from image_resource import ImageResource_qt4

from action.action_item import _MenuItem_qt4, _Tool_qt4
from action.menu_bar_manager import MenuBarManager_qt4
from action.menu_manager import MenuManager_qt4
from action.tool_bar_manager import ToolBarManager_qt4

from workbench.editor import Editor_qt4
from workbench.view import View_qt4
from workbench.workbench_window_layout import WorkbenchWindowLayout_qt4


class Toolkit_qt4(Toolkit):
    """ Implementation of the PyQt v4 toolkit. """

    _MenuItem = _MenuItem_qt4
    _Tool = _Tool_qt4
    Editor = Editor_qt4
    ImageResource = ImageResource_qt4
    MenuBarManager = MenuBarManager_qt4
    MenuManager = MenuManager_qt4
    ToolBarManager = ToolBarManager_qt4
    View = View_qt4
    WorkbenchWindowLayout = WorkbenchWindowLayout_qt4

    def init_toolkit(self, *args, **kw):
        pass
