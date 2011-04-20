# Enthought library imports.
from traits.api import Dict, HasStrictTraits, Instance, List, Str, \
     Tuple

# Local imports.
from task_layout import TaskLayout


class TaskWindowLayout(HasStrictTraits):
    """ A picklable object that describes the layout and state of a TaskWindow.
    """

    # The ID of the active task. If unspecified, the first task will be active.
    active_task = Str

    # The IDs of all the tasks attached to the window.
    tasks = List(Str)

    # The position of the window.
    position = Tuple(-1, -1)

    # The size of the window.
    size = Tuple(800, 600)

    # A map from task IDs to their respective layouts. Set by the framework.
    layout_state = Dict(Str, Instance(TaskLayout))

    def get_active_task(self):
        """ Returns the ID of the active task in the layout, or None if there is
            no active task.
        """
        if self.active_task:
            return self.active_task
        elif self.tasks:
            return self.tasks[0]
        return None

    def is_equivalent_to(self, layout):
        """ Returns whether two layouts are equivalent, i.e. whether they
            contain the same tasks.
        """
        return isinstance(layout, TaskWindowLayout) and \
            self.get_active_task() == layout.get_active_task() and \
            self.tasks == layout.tasks
