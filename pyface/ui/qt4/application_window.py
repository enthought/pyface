# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!



from pyface.qt import QtGui


from pyface.action.api import MenuBarManager, StatusBarManager
from pyface.action.api import ToolBarManager
from traits.api import Instance, List, provides


from pyface.i_application_window import IApplicationWindow, MApplicationWindow
from pyface.ui_traits import Image
from .window import Window


@provides(IApplicationWindow)
class ApplicationWindow(MApplicationWindow, Window):
    """ The toolkit specific implementation of an ApplicationWindow.  See the
    IApplicationWindow interface for the API documentation.
    """

    #: The icon to display in the application window title bar.
    icon = Image()

    #: The menu bar manager for the window.
    menu_bar_manager = Instance(MenuBarManager)

    #: The status bar manager for the window.
    status_bar_manager = Instance(StatusBarManager)

    #: DEPRECATED: The tool bar manager for the window.
    tool_bar_manager = Instance(ToolBarManager)

    #: The collection of tool bar managers for the window.
    tool_bar_managers = List(ToolBarManager)

    def _create(self):
        super()._create()

        contents = QtGui.QWidget(self.control)
        self.control.setCentralWidget(contents)

        self._create_trim_widgets(self.control)

    def _create_control(self, parent):
        control = super()._create_control(parent)
        return control

    def _create_menu_bar(self, parent):
        return

    def _create_status_bar(self, parent):
        return

    def _create_tool_bar(self, parent):
        return

    def _set_window_icon(self):
        return
