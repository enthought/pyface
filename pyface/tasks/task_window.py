# Standard library imports.
import logging

# Enthought library imports.
from pyface.action.api import MenuBarManager, StatusBarManager, ToolBarManager
from pyface.api import ApplicationWindow
from traits.api import Bool, Callable, HasTraits, HasStrictTraits, Instance, \
    List, Property, Unicode, Vetoable, on_trait_change

# Local imports.
from pyface.tasks.action.task_action_manager_builder import TaskActionManagerBuilder
from pyface.tasks.i_dock_pane import IDockPane
from pyface.tasks.i_task_pane import ITaskPane
from pyface.tasks.task import Task, TaskLayout
from pyface.tasks.task_window_backend import TaskWindowBackend
from pyface.tasks.task_window_layout import TaskWindowLayout

# Logging.
logger = logging.getLogger(__name__)


class TaskWindow(ApplicationWindow):
    """ The the top-level window to which tasks can be assigned.

    A TaskWindow is responsible for creating and the managing the controls of
    its tasks.
    """

    #### IWindow interface ####################################################

    # Unless a title is specifically assigned, delegate to the active task.
    title = Property(Unicode, depends_on='active_task, _title')

    #### TaskWindow interface ################################################

    # The pane (central or dock) in the active task that currently has focus.
    active_pane = Instance(ITaskPane)

    # The active task for this window.
    active_task = Instance(Task)

    # The list of all tasks currently attached to this window. All panes of the
    # inactive tasks are hidden.
    tasks = List(Task)

    # The central pane of the active task, which is always visible.
    central_pane = Instance(ITaskPane)

    # The list of all dock panes in the active task, which may or may not be
    # visible.
    dock_panes = List(IDockPane)

    # The factory for the window's TaskActionManagerBuilder, which is
    # instantiated to translate menu and tool bar schemas into Pyface action
    # managers. This attribute can overridden to introduce custom logic into
    # the translation process, although this is not usually necessary.
    action_manager_builder_factory = Callable(TaskActionManagerBuilder)

    #### Protected traits #####################################################

    _active_state = Instance('pyface.tasks.task_window.TaskState')
    _states = List(Instance('pyface.tasks.task_window.TaskState'))
    _title = Unicode
    _window_backend = Instance(TaskWindowBackend)

    ###########################################################################
    # 'Widget' interface.
    ###########################################################################

    def destroy(self):
        """ Overridden to ensure that all task panes are cleanly destroyed.
        """
        # Allow the TaskWindowBackend to clean up first.
        self._window_backend.destroy()

        # Don't use 'remove_task' here to avoid changing the active state and
        # thereby removing the window's menus and toolbars. This can lead to
        # undesirable animations when the window is being closed.
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
        self.opening = event = Vetoable()
        if not event.veto:
            # Create the control, if necessary.
            if self.control is None:
                self._create()

            # Activate a task, if necessary.
            if self._active_state is None and self._states:
                self.activate_task(self._states[0].task)

            self.show(True)
            self.opened = self

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
        """ Delegate to the TaskWindowBackend.
        """
        return self._window_backend.create_contents(parent)

    ###########################################################################
    # 'TaskWindow' interface.
    ###########################################################################

    def activate_task(self, task):
        """ Activates a task that has already been added to the window.
        """
        state = self._get_state(task)
        if state and state != self._active_state:
            # Hide the panes of the currently active task, if necessary.
            if self._active_state is not None:
                self._window_backend.hide_task(self._active_state)

            # Initialize the new task, if necessary.
            if not state.initialized:
                task.initialized()
                state.initialized = True

            # Display the panes of the new task.
            self._window_backend.show_task(state)

            # Activate the new task. The menus, toolbars, and status bar will be
            # replaced at this time.
            self._active_state = state
            task.activated()

        elif not state:
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
        state = TaskState(task=task, layout=task.default_layout)
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
        builder = self.action_manager_builder_factory(task=task)
        state.menu_bar_manager = builder.create_menu_bar_manager()
        state.status_bar_manager = task.status_bar
        state.tool_bar_managers = builder.create_tool_bar_managers()

    def remove_task(self, task):
        """ Removes a task that has already been added to the window. All the
            task's panes are destroyed.
        """
        state = self._get_state(task)
        if state:
            # If the task is active, make sure it is de-activated before
            # deleting its controls.
            if self._active_state == state:
                self._window_backend.hide_task(state)
                self._active_state = None

            self._destroy_state(state)
            self._states.remove(state)
        else:
            logger.warn("Cannot remove task %r: task does not belong to the "
                        "window." % task)

    def focus_next_pane(self):
        """ Shifts focus to the "next" pane, taking into account the active pane
            and the pane geometry.
        """
        if self._active_state:
            panes = self._get_pane_ring()
            index = 0
            if self.active_pane:
                index = (panes.index(self.active_pane) + 1) % len(panes)
            panes[index].set_focus()

    def focus_previous_pane(self):
        """ Shifts focus to the "previous" pane, taking into account the active
            pane and the pane geometry.
        """
        if self._active_state:
            panes = self._get_pane_ring()
            index = -1
            if self.active_pane:
                index = panes.index(self.active_pane) - 1
            panes[index].set_focus()

    def get_central_pane(self, task):
        """ Returns the central pane for the specified task.
        """
        state = self._get_state(task)
        return state.central_pane if state else None

    def get_dock_pane(self, id, task=None):
        """ Returns the dock pane in the task with the specified ID, or
            None if no such dock pane exists. If a task is not specified, the
            active task is used.
        """
        if task is None:
            state = self._active_state
        else:
            state = self._get_state(task)
        return state.get_dock_pane(id) if state else None

    def get_dock_panes(self, task):
        """ Returns the dock panes for the specified task.
        """
        state = self._get_state(task)
        return state.dock_panes[:] if state else []

    def get_task(self, id):
        """ Returns the task with the specified ID, or None if no such task
            exists.
        """
        state = self._get_state(id)
        return state.task if state else None

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
        result = TaskWindowLayout(position=self.position, size=self.size,
                                  size_state=self.size_state)
        for state in self._states:
            if state == self._active_state:
                result.active_task = state.task.id
                layout = self._window_backend.get_layout()
            else:
                layout = state.layout.clone_traits()
            layout.id = state.task.id
            result.items.append(layout)
        return result

    def set_window_layout(self, window_layout):
        """ Applies a TaskWindowLayout to the window.
        """
        # Set window size before laying it out.
        self.position = window_layout.position
        self.size = window_layout.size
        self.size_state = window_layout.size_state

        # Store layouts for the tasks, including the active task.
        for layout in window_layout.items:
            if isinstance(layout, basestring):
                continue
            state = self._get_state(layout.id)
            if state:
                state.layout = layout
            else:
                logger.warn("Cannot apply layout for task %r: task does not "
                            "belong to the window." % layout.id)

        # Attempt to activate the requested task.
        state = self._get_state(window_layout.get_active_task())
        if state:
            # If the requested active task is already active, calling
            # ``activate`` is a no-op, so we must force a re-layout.
            if state == self._active_state:
                self._window_backend.set_layout(state.layout)
            else:
                self.activate_task(state.task)

    ###########################################################################
    # Protected 'TaskWindow' interface.
    ###########################################################################

    def _destroy_state(self, state):
        """ Destroy all controls associated with a Task state.
        """
        # Notify the task that it is about to be destroyed.
        state.task.prepare_destroy()

        # Destroy action managers associated with the task, unless the task is
        # active, in which case this will be handled by our superclass.
        if state != self._active_state:
            if state.menu_bar_manager:
                state.menu_bar_manager.destroy()
            for tool_bar_manager in state.tool_bar_managers:
                tool_bar_manager.destroy()

        # Destroy all controls associated with the task.
        for dock_pane in state.dock_panes:
            dock_pane.destroy()
        state.central_pane.destroy()
        state.task.window = None

    def _get_pane_ring(self):
        """ Returns a list of visible panes ordered for focus switching.
        """
        # Proceed clockwise through the dock areas.
        # TODO: Also take into account ordering within dock areas.
        panes = []
        if self._active_state:
            layout = self.get_layout()
            panes.append(self.central_pane)
            for area in ('top', 'right', 'bottom', 'left'):
                item = getattr(layout, area)
                if item:
                    panes.extend([ self.get_dock_pane(pane_item.id)
                                   for pane_item in item.iterleaves() ])
        return panes

    def _get_state(self, id_or_task):
        """ Returns the TaskState that contains the specified Task, or None if
            no such state exists.
        """
        for state in self._states:
            if state.task == id_or_task or state.task.id == id_or_task:
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

    #### Trait change handlers ################################################

    def __active_state_changed(self, state):
        if state is None:
            self.active_task = self.central_pane = None
            self.dock_panes = []
            self.menu_bar_manager = self.status_bar_manager = None
            self.tool_bar_managers = []
        else:
            self.active_task = state.task
            self.central_pane = state.central_pane
            self.dock_panes = state.dock_panes
            self.menu_bar_manager = state.menu_bar_manager
            self.status_bar_manager = state.status_bar_manager
            self.tool_bar_managers = state.tool_bar_managers

    @on_trait_change('central_pane.has_focus, dock_panes.has_focus')
    def _focus_updated(self, obj, name, old, new):
        if name == 'has_focus' and new:
            self.active_pane = obj

    @on_trait_change('_states[]')
    def _states_updated(self):
        self.tasks = [ state.task for state in self._states ]


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
