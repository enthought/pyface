# Enthought library imports.
from enthought.pyface.action.api import StatusBarManager
from enthought.traits.api import Callable, HasTraits, Instance, List, Str, \
     Unicode

# Local imports.
from action.schema import MenuSchema, MenuBarSchema, ToolBarSchema
from action.schema_addition import SchemaAddition
from task_layout import TaskLayout


class Task(HasTraits):
    """ A collection of pane, menu, tool bar, and status bar factories.

    The central class in the Tasks plugin, a Task is responsible for
    describing a set of user interface elements, as well as mediating between
    its view (a TaskWindow) and an application-specific model.
    """

    # The task's identifier.
    id = Str

    # The task's user-visible name.
    name = Unicode

    # The default layout to use for the task. If not overridden, only the
    # central pane is displayed.
    default_layout = Instance(TaskLayout, ())

    # A list of extra IDockPane factories for the task. These dock panes are
    # used in conjunction with the dock panes returned by create_dock_panes().
    extra_dock_pane_factories = List(Callable)

    # The window to which the task is attached. Set by the framework.
    window = Instance('enthought.pyface.tasks.task_window.TaskWindow')

    #### Actions ##############################################################

    # The menu bar for the task. Note that the Tasks framework will make
    # additions to the menu bar under certain conditions:
    # - If there is a there is a top-level menu with the ID 'View', entries
    #   will be inserted for toggling the visibility of closable dock panes.
    menu_bar = Instance(MenuBarSchema)

    # The (optional) status bar for the task.
    status_bar = Instance(StatusBarManager)

    # The list of tool bars for the tasks.
    tool_bars = List(ToolBarSchema)

    # A list of extra actions, groups, and menus that are inserted into menu
    # bars and tool bars constructed from the above schemas.
    extra_actions = List(SchemaAddition)

    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def activated(self):
        """ Called after the task has been activated in a TaskWindow.
        """
        pass

    def create_central_pane(self):
        """ Create and return the central pane, which must implement ITaskPane.
        """
        raise NotImplementedError

    def create_dock_panes(self):
        """ Create and return the task's dock panes (IDockPane instances).

        This method is called *after* create_central_pane() when the task is
        added to a TaskWindow.
        """
        return []

    def initialized(self):
        """ Called after the task has been activated in a TaskWindow for the
        first time.

        Override this method to perform any initialization that requires the
        Task's panes to be instantiated. Note that this method, when called, is
        called before activated().
        """
        pass
