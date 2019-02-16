# System library imports.
from pyface.qt import QtCore, QtGui

# Enthought library imports.
from traits.api import Instance, List

# Local imports.
from pyface.tasks.i_task_window_backend import MTaskWindowBackend
from pyface.tasks.task_layout import PaneItem, TaskLayout
from .dock_pane import AREA_MAP, INVERSE_AREA_MAP
from .main_window_layout import MainWindowLayout

# Constants.
CORNER_MAP = {
    'top_left': QtCore.Qt.TopLeftCorner,
    'top_right': QtCore.Qt.TopRightCorner,
    'bottom_left': QtCore.Qt.BottomLeftCorner,
    'bottom_right': QtCore.Qt.BottomRightCorner
}


class TaskWindowBackend(MTaskWindowBackend):
    """ The toolkit-specific implementation of a TaskWindowBackend.

    See the ITaskWindowBackend interface for API documentation.
    """

    #### Private interface ####################################################

    _main_window_layout = Instance(MainWindowLayout)

    ###########################################################################
    # 'ITaskWindowBackend' interface.
    ###########################################################################

    def create_contents(self, parent):
        """ Create and return the TaskWindow's contents.
        """
        app = QtGui.QApplication.instance()
        app.focusChanged.connect(self._focus_changed_signal)
        return QtGui.QStackedWidget(parent)

    def destroy(self):
        """ Destroy the backend.
        """
        app = QtGui.QApplication.instance()
        app.focusChanged.disconnect(self._focus_changed_signal)
        # signal to layout we don't need it any more
        self._main_window_layout.control = None

    def hide_task(self, state):
        """ Assuming the specified TaskState is active, hide its controls.
        """
        # Save the task's layout in case it is shown again later.
        self.window._active_state.layout = self.get_layout()

        # Now hide its controls.
        self.control.centralWidget().removeWidget(state.central_pane.control)
        for dock_pane in state.dock_panes:
            # Warning: The layout behavior is subtly different (and wrong!) if
            # the order of these two statement is switched.
            dock_pane.control.hide()
            self.control.removeDockWidget(dock_pane.control)

    def show_task(self, state):
        """ Assuming no task is currently active, show the controls of the
            specified TaskState.
        """
        # Show the central pane.
        self.control.centralWidget().addWidget(state.central_pane.control)

        # Show the dock panes.
        self._layout_state(state)

    #### Methods for saving and restoring the layout ##########################

    def get_layout(self):
        """ Returns a TaskLayout for the current state of the window.
        """
        # Extract the layout from the main window.
        layout = TaskLayout(id=self.window._active_state.task.id)
        self._main_window_layout.state = self.window._active_state
        self._main_window_layout.get_layout(layout)

        # Extract the window's corner configuration.
        for name, corner in CORNER_MAP.items():
            area = INVERSE_AREA_MAP[int(self.control.corner(corner))]
            setattr(layout, name + '_corner', area)

        return layout

    def set_layout(self, layout):
        """ Applies a TaskLayout (which should be suitable for the active task)
            to the window.
        """
        self.window._active_state.layout = layout
        self._layout_state(self.window._active_state)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _layout_state(self, state):
        """ Layout the dock panes in the specified TaskState using its
            TaskLayout.
        """
        # Assign the window's corners to the appropriate dock areas.
        for name, corner in CORNER_MAP.items():
            area = getattr(state.layout, name + '_corner')
            self.control.setCorner(corner, AREA_MAP[area])

        # Add all panes in the TaskLayout.
        self._main_window_layout.state = state
        self._main_window_layout.set_layout(state.layout)

        # Add all panes not assigned an area by the TaskLayout.
        for dock_pane in state.dock_panes:
            if dock_pane.control not in self._main_window_layout.consumed:
                dock_area = AREA_MAP[dock_pane.dock_area]
                self.control.addDockWidget(dock_area, dock_pane.control)
                # By default, these panes are not visible. However, if a pane
                # has been explicitly set as visible, honor that setting.
                if dock_pane.visible:
                    dock_pane.control.show()

    #### Trait initializers ###################################################

    def __main_window_layout_default(self):
        return TaskWindowLayout(control=self.control)

    #### Signal handlers ######################################################

    def _focus_changed_signal(self, old, new):
        if self.window.active_task:
            panes = [self.window.central_pane] + self.window.dock_panes
            for pane in panes:
                if new and pane.control.isAncestorOf(new):
                    pane.has_focus = True
                elif old and pane.control.isAncestorOf(old):
                    pane.has_focus = False


class TaskWindowLayout(MainWindowLayout):
    """ A MainWindowLayout for a TaskWindow.
    """

    #### 'TaskWindowLayout' interface #########################################

    consumed = List
    state = Instance('pyface.tasks.task_window.TaskState')

    ###########################################################################
    # 'MainWindowLayout' interface.
    ###########################################################################

    def set_layout(self, layout):
        """ Applies a DockLayout to the window.
        """
        self.consumed = []
        super(TaskWindowLayout, self).set_layout(layout)

    ###########################################################################
    # 'MainWindowLayout' abstract interface.
    ###########################################################################

    def _get_dock_widget(self, pane):
        """ Returns the QDockWidget associated with a PaneItem.
        """
        for dock_pane in self.state.dock_panes:
            if dock_pane.id == pane.id:
                self.consumed.append(dock_pane.control)
                return dock_pane.control
        return None

    def _get_pane(self, dock_widget):
        """ Returns a PaneItem for a QDockWidget.
        """
        for dock_pane in self.state.dock_panes:
            if dock_pane.control == dock_widget:
                return PaneItem(id=dock_pane.id)
        return None
