# Enthought library imports.
from traits.api import List, Str, Tuple

# Local imports.
from task_layout import LayoutContainer, TaskLayout


class TaskWindowLayout(LayoutContainer):
    """ The layout of a TaskWindow.
    """

    # The ID of the active task. If unspecified, the first task will be active.
    active_task = Str

    # The layouts of the tasks contained in the window.
    items = List(TaskLayout)

    # The position of the window.
    position = Tuple(-1, -1)

    # The size of the window.
    size = Tuple(800, 600)

    def get_active_task(self):
        """ Returns the ID of the active task in the layout, or None if there is
            no active task.
        """
        if self.active_task:
            return self.active_task
        elif self.tasks:
            return self.tasks[0]
        return None
