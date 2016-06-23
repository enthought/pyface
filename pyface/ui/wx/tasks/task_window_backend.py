# Standard library imports.
import logging

# System library imports.
import wx
from pyface.wx.aui import aui

# Enthought library imports.
from traits.api import Instance, List, Str

# Local imports.
from main_window_layout import MainWindowLayout
from pyface.tasks.i_task_window_backend import MTaskWindowBackend
from pyface.tasks.task_layout import PaneItem, TaskLayout

# Logging
logger = logging.getLogger(__name__)


class AUILayout(TaskLayout):
    """ The layout for a main window's dock area using AUI Perspectives
    """
    perspective = Str

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
        # No extra control needed for wx (it's all handled by the AUIManager in
        # the ApplicationWindow) but we do need to handle some events here
        self.window._aui_manager.Bind(aui.EVT_AUI_PANE_CLOSE, self._pane_close_requested)

    def destroy(self):
        """ Destroy the backend.
        """
        pass

    def hide_task(self, state):
        """ Assuming the specified TaskState is active, hide its controls.
        """
        # Save the task's layout in case it is shown again later.
        self.window._active_state.layout = self.get_layout()

        # Now hide its controls.
        self.window._aui_manager.DetachPane(state.central_pane.control)
        state.central_pane.control.Hide()
        
        for dock_pane in state.dock_panes:
            logger.debug("hiding dock pane %s" % dock_pane.id)
            self.window._aui_manager.DetachPane(dock_pane.control)
            dock_pane.control.Hide()
        
        # Remove any tabbed notebooks left over after all the panes have been
        # removed
        self.window._aui_manager.UpdateNotebook()
        
        # Remove any still-left over stuff (i.e. toolbars)
        for info in self.window._aui_manager.GetAllPanes():
            logger.debug("hiding remaining pane: %s" % info.name)
            control = info.window
            self.window._aui_manager.DetachPane(control)
            control.Hide()

    def show_task(self, state):
        """ Assuming no task is currently active, show the controls of the
            specified TaskState.
        """
        # Show the central pane.
        info = aui.AuiPaneInfo().Caption('Central').Dockable(False).Floatable(False).Name('Central').CentrePane().Maximize()
        logger.debug("adding central pane to %s" % self.window)
        self.window._aui_manager.AddPane(state.central_pane.control, info)
        self.window._aui_manager.Update()

        # Show the dock panes.
        self._layout_state(state)
    
    def get_toolbars(self, task=None):
        if task is None:
            state = self.window._active_state
        else:
            state = self.window._get_state(task)
        toolbars = []
        for tool_bar_manager in state.tool_bar_managers:
            info = self.window._aui_manager.GetPane(tool_bar_manager.id)
            toolbars.append(info)
        return toolbars
    
    def show_toolbars(self, toolbars):
        for info in toolbars:
            info.Show()
        self.window._aui_manager.Update()

    #### Methods for saving and restoring the layout ##########################

    def get_layout(self):
        """ Returns a TaskLayout for the current state of the window.
        """
        # Extract the layout from the main window.
        layout = AUILayout(id=self.window._active_state.task.id)
        self._main_window_layout.state = self.window._active_state
        self._main_window_layout.get_layout(layout, self.window)

        return layout

    def set_layout(self, layout):
        """ Applies a TaskLayout (which should be suitable for the active task)
            to the window.
        """
        self.window._active_state.layout = layout
        self._layout_state(self.window._active_state)
        self.window._aui_manager.Update()

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _layout_state(self, state):
        """ Layout the dock panes in the specified TaskState using its
            TaskLayout.
        """
#        # Assign the window's corners to the appropriate dock areas.
#        for name, corner in CORNER_MAP.iteritems():
#            area = getattr(state.layout, name + '_corner')
#            self.control.setCorner(corner, AREA_MAP[area])

        # Add all panes in the TaskLayout.
        self._main_window_layout.state = state
        self._main_window_layout.set_layout(state.layout, self.window)

    #### Trait initializers ###################################################

    def __main_window_layout_default(self):
        return TaskWindowLayout()

    #### Signal handlers ######################################################

    def _pane_close_requested(self, evt):
        pane = evt.GetPane()
        logger.debug("_pane_close_requested: pane=%s" % pane.name)
        for dock_pane in self.window.dock_panes:
            logger.debug("_pane_close_requested: checking pane=%s" % dock_pane.pane_name)
            if dock_pane.pane_name == pane.name:
                logger.debug("_pane_close_requested: FOUND PANE!!!!!!")
                dock_pane.visible = False
                break

    def _focus_changed_signal(self, old, new):
        if self.window.active_task:
            panes = [ self.window.central_pane ] + self.window.dock_panes
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
    # 'MainWindowLayout' abstract interface.
    ###########################################################################

    def _get_dock_widget(self, pane):
        """ Returns the control associated with a PaneItem.
        """
        for dock_pane in self.state.dock_panes:
            if dock_pane.id == pane.id:
                self.consumed.append(dock_pane.control)
                return dock_pane.control
        return None

    def _get_pane(self, dock_widget):
        """ Returns a PaneItem for a control.
        """
        for dock_pane in self.state.dock_panes:
            if dock_pane.control == dock_widget:
                return PaneItem(id=dock_pane.id)
        return None
