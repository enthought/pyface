# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Define a base Task application class to create the event loop, and launch
the creation of tasks and corresponding windows.
"""


import logging

from traits.api import (
    Callable,
    HasStrictTraits,
    List,
    Instance,
    Property,
    Str,
    cached_property,
    observe,
)
from traits.observation.api import trait

from pyface.gui_application import GUIApplication

logger = logging.getLogger(__name__)


class TaskFactory(HasStrictTraits):
    """ A factory for creating a Task with some additional metadata.
    """

    #: The task factory's unique identifier. This ID is assigned to all tasks
    #: created by the factory.
    id = Str()

    #: The task factory's user-visible name.
    name = Str()

    #: A callable with the following signature:
    #:
    #:     callable(\**traits) -> Task
    #:
    #: Often this attribute will simply be a Task subclass.
    factory = Callable

    def create(self, **traits):
        """ Creates the Task.

        The default implementation simply calls the 'factory' attribute.
        """
        return self.factory(**traits)


class TasksApplication(GUIApplication):
    """ A base class for Pyface tasks applications.
    """

    # -------------------------------------------------------------------------
    # 'TaskApplication' interface
    # -------------------------------------------------------------------------

    # Task management --------------------------------------------------------

    #: List of all running tasks
    tasks = List(Instance("pyface.tasks.task.Task"))

    #: Currently active Task if any.
    active_task = Property(
        observe=trait("active_window").trait("active_task", optional=True)
    )

    #: List of all application task factories.
    task_factories = List()

    #: The default layout for the application. If not specified, a single
    #: window will be created with the first available task factory.
    default_layout = List(
        Instance("pyface.tasks.task_window_layout.TaskWindowLayout")
    )

    #: Hook to add global schema additions to tasks/windows
    extra_actions = List(
        Instance("pyface.action.schema.schema_addition.SchemaAddition")
    )

    #: Hook to add global dock pane additions to tasks/windows
    extra_dock_pane_factories = List(Callable)

    # Window lifecycle methods -----------------------------------------------

    def create_task(self, id):
        """ Creates the Task with the specified ID.

        Parameters
        ----------
        id : str
            The id of the task factory to use.

        Returns
        -------
        The new Task, or None if there is not a suitable TaskFactory.
        """
        factory = self._get_task_factory(id)
        if factory is None:
            logger.warning("Could not find task factory {}".format(id))
            return None

        task = factory.create(id=factory.id)
        task.extra_actions.extend(self.extra_actions)
        task.extra_dock_pane_factories.extend(self.extra_dock_pane_factories)
        return task

    def create_window(self, layout=None, **kwargs):
        """ Connect task to application and open task in a new window.

        Parameters
        ----------
        layout : TaskLayout  or None
            The pane layout for the window.
        **kwargs : dict
            Additional keyword arguments to pass to the window factory.


        Returns
        -------
        window : ITaskWindow  or None
            The new TaskWindow.
        """
        from pyface.tasks.task_window_layout import TaskWindowLayout

        window = super().create_window(**kwargs)

        if layout is not None:
            for task_id in layout.get_tasks():
                task = self.create_task(task_id)
                if task is not None:
                    window.add_task(task)
                else:
                    msg = "Missing factory for task with ID %r"
                    logger.error(msg, task_id)
        else:
            # Create an empty layout to set default size and position only
            layout = TaskWindowLayout()

        window.set_window_layout(layout)

        return window

    def _create_windows(self):
        """ Create the initial windows to display from the default layout.
        """
        for layout in self.default_layout:
            window = self.create_window(layout)
            self.add_window(window)
            self.active_window = window

        # -------------------------------------------------------------------------
        # Private interface
        # -------------------------------------------------------------------------

    def _get_task_factory(self, id):
        """ Returns the TaskFactory with the specified ID, or None.
        """
        for factory in self.task_factories:
            if factory.id == id:
                return factory
        return None

    # Destruction utilities ---------------------------------------------------

    @observe("windows:items:closed")
    def _on_window_closed(self, event):
        """ Listener that ensures window handles are released when closed.
        """
        window = event.object
        if getattr(window, "active_task", None) in self.tasks:
            self.tasks.remove(window.active_task)
        super()._on_window_closed(event)

    # Trait initializers and property getters ---------------------------------

    def _window_factory_default(self):
        """ Default to TaskWindow.

        This will be sufficient in many cases as customized behaviour comes
        from the Task and the TaskWindow is just a shell.
        """
        from pyface.tasks.task_window import TaskWindow

        return TaskWindow

    def _default_layout_default(self):
        from pyface.tasks.task_window_layout import TaskWindowLayout

        window_layout = TaskWindowLayout()
        if self.task_factories:
            window_layout.items = [self.task_factories[0].id]
        return [window_layout]

    def _extra_actions_default(self):
        """ Extra application-wide menu items

        This adds a collection of standard Tasks application menu items and
        groups to a Task's set of menus.  Whether or not they actually appear
        depends on whether the appropriate menus are provided by the Task.

        These default additions assume that the window will hold an editor pane
        so that Ctrl-N and Ctrl-W will be bound to creating/closing new editors
        rather than new task windows.
        """
        from pyface.action.api import (
            AboutAction,
            CloseActiveWindowAction,
            ExitAction,
        )
        from pyface.action.schema.api import SMenu, SchemaAddition
        from pyface.tasks.action.api import (
            CreateTaskWindowAction,
            TaskWindowToggleGroup,
        )

        return [
            SchemaAddition(
                factory=CreateTaskWindowAction.factory(
                    application=self, accelerator="Ctrl+Shift+N"
                ),
                path="MenuBar/File/new_group",
            ),
            SchemaAddition(
                id="close_action",
                factory=CloseActiveWindowAction.factory(
                    application=self, accelerator="Ctrl+Shift+W"
                ),
                path="MenuBar/File/close_group",
            ),
            SchemaAddition(
                id="exit_action",
                factory=ExitAction.factory(application=self),
                path="MenuBar/File/close_group",
                absolute_position="last",
            ),
            SchemaAddition(
                # id='Window',
                factory=lambda: SMenu(
                    TaskWindowToggleGroup(application=self),
                    id="Window",
                    name="&Window",
                ),
                path="MenuBar",
                after="View",
                before="Help",
            ),
            SchemaAddition(
                id="about_action",
                factory=AboutAction.factory(application=self),
                path="MenuBar/Help",
                absolute_position="first",
            ),
        ]

    @cached_property
    def _get_active_task(self):
        if self.active_window is not None:
            return getattr(self.active_window, "active_task", None)
        else:
            return None
