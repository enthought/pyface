#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Standard library imports.
import sys

# Major package imports.
from PyQt4 import QtCore, QtGui

# Internal Enthought library imports.
from enthought.pyface.toolkit import Toolkit

# Local imports.
from about_dialog import AboutDialog_qt4
from dialog import Dialog_qt4
from directory_dialog import DirectoryDialog_qt4
from file_dialog import FileDialog_qt4
from gui import GUI_qt4
from image_cache import ImageCache_qt4
from image_resource import ImageResource_qt4
from message_dialog import MessageDialog_qt4
from python_shell import PythonShell_qt4
from resource_manager import PyfaceResourceFactory_qt4
from splash_screen import SplashScreen_qt4
from system_metrics import SystemMetrics_qt4
from widget import Widget_qt4
from window import Window_qt4

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
    AboutDialog = AboutDialog_qt4
    Dialog = Dialog_qt4
    DirectoryDialog = DirectoryDialog_qt4
    Editor = Editor_qt4
    FileDialog = FileDialog_qt4
    GUI = GUI_qt4
    ImageCache = ImageCache_qt4
    ImageResource = ImageResource_qt4
    MenuBarManager = MenuBarManager_qt4
    MenuManager = MenuManager_qt4
    MessageDialog = MessageDialog_qt4
    PyfaceResourceFactory = PyfaceResourceFactory_qt4
    PythonShell = PythonShell_qt4
    SplashScreen = SplashScreen_qt4
    SystemMetrics = SystemMetrics_qt4
    ToolBarManager = ToolBarManager_qt4
    View = View_qt4
    Widget = Widget_qt4
    Window = Window_qt4
    WorkbenchWindowLayout = WorkbenchWindowLayout_qt4

    def init_toolkit(self, *args, **kw):
        """ Initialises the toolkit. """
        if QtCore.QT_VERSION < 0x040200:
            raise RuntimeError, "Need Qt v4.2 or higher, but got v%s" \
                    % QtCore.QT_VERSION_STR

        # It's possible that it has already been initialised.
        self._app = QtGui.QApplication.instance()

        if self._app is None:
            self._app = QtGui.QApplication(sys.argv)
