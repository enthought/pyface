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


import sys

from traits.api import observe, provides, Str

from pyface.qt import QtGui
from pyface.i_application_window import IApplicationWindow, MApplicationWindow
from .image_resource import ImageResource
from .window import Window


@provides(IApplicationWindow)
class ApplicationWindow(MApplicationWindow, Window):
    """ The toolkit specific implementation of an ApplicationWindow.  See the
    IApplicationWindow interface for the API documentation.
    """

    # 'IWindow' interface -------------------------------------------------#

    #: The window title.
    title = Str("Pyface")

    # ------------------------------------------------------------------------
    # Protected 'IApplicationWindow' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        panel = QtGui.QWidget(parent)

        palette = QtGui.QPalette(panel.palette())
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("blue"))
        panel.setPalette(palette)
        panel.setAutoFillBackground(True)

        return panel

    def _create_menu_bar(self, parent):
        if self.menu_bar_manager is not None:
            menu_bar = self.menu_bar_manager.create_menu_bar(parent)
            self.control.setMenuBar(menu_bar)

    def _create_status_bar(self, parent):
        if self.status_bar_manager is not None:
            status_bar = self.status_bar_manager.create_status_bar(parent)

            # QMainWindow automatically makes the status bar visible, but we
            # have delegated this responsibility to the status bar manager.
            self.control.setStatusBar(status_bar)
            status_bar.setVisible(self.status_bar_manager.visible)

    def _create_tool_bar(self, parent):
        tool_bar_managers = self.tool_bar_managers
        visible = self.control.isVisible()
        for tool_bar_manager in tool_bar_managers:
            # Add the tool bar and make sure it is visible.
            tool_bar = tool_bar_manager.create_tool_bar(parent)
            self.control.addToolBar(tool_bar)
            tool_bar.show()

            # Make sure that the tool bar has a name so its state can be saved.
            if len(tool_bar.objectName()) == 0:
                tool_bar.setObjectName(tool_bar_manager.name)

        if sys.platform == "darwin":
            # Work around bug in Qt on OS X where creating a tool bar with a
            # QMainWindow parent hides the window. See
            # http://bugreports.qt.nokia.com/browse/QTBUG-5069 for more info.
            self.control.setVisible(visible)

    def _set_window_icon(self):
        if self.icon is None:
            icon = ImageResource("application.png")
        else:
            icon = self.icon
        if self.control is not None:
            self.control.setWindowIcon(icon.create_icon())

    # ------------------------------------------------------------------------
    # 'Window' interface.
    # ------------------------------------------------------------------------

    def _size_default(self):
        """ Trait initialiser. """

        return (800, 600)

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def create(self, parent=None):
        super().create(parent=parent)

        contents = self._create_contents(self.control)
        self.control.setCentralWidget(contents)

        self._create_trim_widgets(self.control)

    def _create_control(self, parent):
        control = super()._create_control(parent)
        control.setObjectName("ApplicationWindow")

        control.setAnimated(False)
        control.setDockNestingEnabled(True)

        return control

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    # Trait change handlers ------------------------------------------------

    # QMainWindow takes ownership of the menu bar and the status bar upon
    # assignment. For this reason, it is unnecessary to delete the old controls
    # in the following two handlers.

    @observe("menu_bar_manager")
    def _menu_bar_manager_updated(self, event):
        if self.control is not None:
            self._create_menu_bar(self.control)

    @observe("status_bar_manager")
    def _status_bar_manager_updated(self, event):
        if self.control is not None:
            if event.old is not None:
                self.control.setStatusBar(None)
                event.old.destroy()
            self._create_status_bar(self.control)

    @observe("tool_bar_managers.items")
    def _update_tool_bar_managers(self, event):
        if self.control is not None:
            # Remove the old toolbars.
            for child in self.control.children():
                if isinstance(child, QtGui.QToolBar):
                    self.control.removeToolBar(child)
                    child.deleteLater()

            # Add the new toolbars.
            if event.new is not None:
                self._create_status_bar(self.control)

    @observe("icon")
    def _icon_updated(self, event):
        self._set_window_icon()
