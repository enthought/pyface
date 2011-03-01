# Standard library imports.
import logging

# Enthought library imports.
from enthought.pyface.action.api import Group, MenuManager, MenuBarManager, \
    StatusBarManager, ToolBarManager
from enthought.pyface.api import ApplicationWindow
from enthought.traits.api import Bool, HasTraits, HasStrictTraits, Instance, \
    List, Property, Unicode, Vetoable

# Local imports.
from action.task_action_manager_builder import TaskActionManagerBuilder
from i_dock_pane import IDockPane
from i_task_pane import ITaskPane
from task import Task, TaskLayout
from task_window_backend import TaskWindowBackend
from task_window_layout import TaskWindowLayout

# Logging.
logger = logging.getLogger(__name__)


class TaskState(HasStrictTraits):
    """ An object used internally by TaskWindow to maintain the state associated
        with an attached Task.
    """

    task = Instance(Task)
    layout = Instance(TaskLayout)
    initialized = Bool(False)

    central_pane = Instance(ITaskPane)
    dock_panes = List(IDockPane)
    menu_bar_manager = Instance(MenuBarManager)
    status_bar_manager = Instance(StatusBarManager)
    tool_bar_managers = List(ToolBarManager)

    def get_dock_pane(self, id):
        """ Returns the dock pane with the specified id, or None if no such dock
            pane exists.
        """
        for pane in self.dock_panes:
            if pane.id == id:
                return pane
        return None


class TaskWindow(ApplicationWindow):
    """ The the top-level window to which tasks can be assigned.

    A TaskWindow is responsible for creating and the managing the controls of
    its tasks.
    """

    #### IWindow interface ####################################################

    # Unless a title is specifically assigned, delegate to the active task.
    title = Property(Unicode, depends_on='active_task, _title')

    #### IApplicationWindow interface #########################################

    menu_bar_manager = Property(Instance(MenuBarManager),
                                depends_on='_active_state')
    status_bar_manager = Property(Instance(StatusBarManager),
                                  depends_on='_active_state')
    tool_bar_managers = Property(List(ToolBarManager),
                                 depends_on='_active_state')

    #### TaskWindow interface ################################################

    # The active task for this window.
    active_task = Property(Instance(Task), depends_on='_active_state')

    # The list of all tasks currently attached to this window. All panes of the
    # inactive tasks are hidden.
    tasks = Property(List, depends_on='_states')

    # The central pane of the active task, which is always visible.
    central_pane = Property(Instance(ITaskPane), depends_on='_active_state')

    # The list of all dock panes in the active task, which may or may not be
    # visible.
    dock_panes = Property(List(IDockPane), depends_on='_activate_state')

    #### Protected traits #####################################################

    _active_state = Instance(TaskState)
    _states = List(Instance(TaskState))
    _title = Unicode
    _window_backend = Instance(TaskWindowBackend)

    ###########################################################################
    # 'Widget' interface.
    ###########################################################################

    def destroy(self):
        """ Overridden to ensure that all task panes are cleanly destroyed.
        """
        for state in self._states:
            self._destroy_state(state)
        super(TaskWindow, self).destroy()

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def open(self):
        """ Opens the window.

        Overridden to make the 'opening' event vetoable and to activate a task
        if one has not already been activated. Returns whether the window was
        opened.
        """
        # From the base class implementation.
        self.opening = event = Vetoable()
        if not event.veto:
            if self.control is None:
                self._create()
            self.show(True)
            self.opened = self

            # Activate a task, if necessary.
            if self._active_state is None and self._states:
                self.activate_task(self._states[0].task)
                
        return self.control is not None

    def close(self):
        """ Closes the window.

        Overriden to make the 'closing' event vetoable. Returns whether the
        window was closed.
        """
        if self.control is not None:
            self.closing = event = Vetoable()
            if not event.veto:
                self.destroy()
                self.closed = self
        
        return self.control is None

    ###########################################################################
    # Protected 'IApplicationWindow' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Delegate to the TaskWindowLayout.
        """
        return self._window_backend.create_contents(parent)

    ###########################################################################
    # 'TaskWindow' interface.
    ###########################################################################

    def activate_task(self, task):
        """ Activates a task that has already been added to the window.
        """
        state = self._fetch_state(task)
        if state:
            # Hide the panes of the currently active task, if necessary.
            if self._active_state is not None:
                self._window_backend.hide_task(self._active_state)

            # Display the panes of the new task.
            self._window_backend.show_task(state)

            # Activate the new task. The menus, toolbars, and status bar will be
            # replaced at this time.
            self._active_state = state

            # Notify the task that it has been activated.
            if not state.initialized:
                task.initialized()
                state.initialized = True
            task.activated()
        else:
            logger.warn("Cannot activate task %r: task does not belong to the "
                        "window." % task)

    def add_task(self, task):
        """ Adds a task to the window. The task is not activated.
        """
        if task.window is not None:
            logger.error("Cannot add task %r: task has already been added "
                         "to a window!" % task)
            return

        task.window = self
        state = TaskState(task=task,
                          layout=task.default_layout.clone_traits())
        self._states.append(state)

        # Make sure the underlying control has been created, even if it is not
        # yet visible.
        if self.control is None:
            self._create()

        # Create the central pane.
        state.central_pane = task.create_central_pane()
        state.central_pane.task = task
        state.central_pane.create(self.control)

        # Create the dock panes.
        state.dock_panes = task.create_dock_panes()
        for dock_pane_factory in task.extra_dock_pane_factories:
            state.dock_panes.append(dock_pane_factory(task=task))
        for dock_pane in state.dock_panes:
            dock_pane.task = task
            dock_pane.create(self.control)

        # Build the menu and tool bars.
        builder = TaskActionManagerBuilder(task=task)
        state.menu_bar_manager = builder.create_menu_bar_manager()
        state.status_bar_manager = task.status_bar
        state.tool_bar_managers = builder.create_tool_bar_managers()

    def remove_task(self, task):
        """ Removes a task that has already been added to the window. All the
            task's panes are destroyed.
        """
        state = self._fetch_state(task)
        if state:
            # If the task is active, make sure it is de-activated before
            # deleting its controls.
            if self._active_state == state:
                self._window_backend.hide_task(state)
                self._active_state = None

            # Destroy all controls associated with the task.
            self._destroy_state(state)

            self._states.remove(state)
        else:
            logger.warn("Cannot remove task %r: task does not belong to the "
                        "window." % task)

    def get_central_pane(self, task):
        """ Returns the central pane for the specified task.
        """
        state = self._fetch_state(task)
        return state.central_pane if state else None

    def get_dock_pane(self, id, task=None):
        """ Returns the dock pane in the task with the specified ID, or
            None if no such dock pane exists. If a task is not specified, the
            active task is used.
        """
        if task is None:
            state = self._active_state
        else:
            state = self._fetch_state(task)
        return state.get_dock_pane(id) if state else None

    def get_dock_panes(self, task):
        """ Returns the dock panes for the specified task.
        """
        state = self._fetch_state(task)
        return state.dock_panes[:] if state else []

    def get_task(self, id):
        """ Returns the task with the specified ID, or None if no such task
            exists.
        """
        for state in self._states:
            if state.task.id == id:
                return state.task
        return None

    #### Methods for saving and restoring the layout ##########################

    def get_layout(self):
        """ Returns a TaskLayout (for the active task) that reflects the state
            of the window.
        """
        if self._active_state:
            return self._window_backend.get_layout()
        return None

    def set_layout(self, layout):
        """ Applies a TaskLayout (which should be suitable for the active task)
            to the window.
        """
        if self._active_state:
            self._window_backend.set_layout(layout)

    def reset_layout(self):
        """ Restores the active task's default TaskLayout.
        """
        if self.active_task:
            self.set_layout(self.active_task.default_layout)

    def get_window_layout(self):
        """ Returns a TaskWindowLayout for the current state of the window.
        """
        result = TaskWindowLayout(position=self.position, size=self.size)
        for state in self._states:
            id = state.task.id
            result.tasks.append(id)
            if state == self._active_state:
                result.active_task = id
                result.layout_state[id] = self._window_backend.get_layout()
            else:
                result.layout_state[id] = state.layout
        return result

    def set_window_layout(self, window_layout):
        """ Applies a TaskWindowLayout to the window.
        """
        # Set window size before laying it out.
        self.position = window_layout.position
        self.size = window_layout.size

        # Attempt to activate the requested task.
        task = self.get_task(window_layout.active_task)
        if task:
            self.activate_task(task)

        # Set layouts for the tasks, including the active task.
        for state in self._states:
            layout = window_layout.layout_state.get(state.task.id)
            if layout:
                if state == self._active_state:
                    self._window_backend.set_layout(layout)
                else:
                    state.layout = layout

    ###########################################################################
    # Protected 'TaskWindow' interface.
    ###########################################################################

    def _destroy_state(self, state):
        """ Destroys all the controls associated with the specified TaskState.
        """
        for dock_pane in state.dock_panes:
            dock_pane.destroy()
        state.central_pane.destroy()
        state.task.window = None

    def _fetch_state(self, task):
        """ Returns the TaskState that contains the specified Task, or None if
            no such state exists.
        """
        for state in self._states:
            if state.task == task:
                return state
        return None

    #### Trait initializers ###################################################

    def __window_backend_default(self):
        return TaskWindowBackend(window=self)

    #### Trait property getters/setters #######################################

    def _get_title(self):
        if self._title or self.active_task is None:
            return self._title
        return self.active_task.name

    def _set_title(self, title):
        self._title = title

    def _get_menu_bar_manager(self):
        if self._active_state is not None:
            return self._active_state.menu_bar_manager
        return None

    def _get_status_bar_manager(self):
        if self._active_state is not None:
            return self._active_state.status_bar_manager
        return None

    def _get_tool_bar_managers(self):
        if self._active_state is not None:
            return self._active_state.tool_bar_managers[:]
        return []

    def _get_active_task(self):
        if self._active_state is not None:
            return self._active_state.task
        return None

    def _get_central_pane(self):
        if self._active_state is not None:
            return self._active_state.central_pane
        return None

    def _get_dock_panes(self):
        if self._active_state is not None:
            return self._active_state.dock_panes[:]
        return []

    def _get_tasks(self):
        return [ state.task for state in self._states ]
