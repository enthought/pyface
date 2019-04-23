# Enthought library imports.
from traits.api import Either, List, Str, Tuple, Enum

# Local imports.
from pyface.tasks.task_layout import LayoutContainer, TaskLayout
import six


class TaskWindowLayout(LayoutContainer):
    """ The layout of a TaskWindow.
    """

    # The ID of the active task. If unspecified, the first task will be active.
    active_task = Str

    # The tasks contained in the window. If an ID is specified, the task will
    # use its default layout. Otherwise, it will use the specified TaskLayout.
    items = List(Either(Str, TaskLayout), pretty_skip=True)

    # The position of the window.
    position = Tuple(-1, -1)

    # The size of the window.
    size = Tuple(800, 600)

    size_state = Enum('normal', 'maximized')

    def get_active_task(self):
        """ Returns the ID of the active task in the layout, or None if there is
            no active task.
        """
        if self.active_task:
            return self.active_task
        elif self.items:
            first = self.items[0]
            return first if isinstance(first, six.string_types) else first.id
        return None

    def get_tasks(self):
        """ Returns the IDs of the tasks in the layout.
        """
        return [ (item if isinstance(item, six.string_types) else item.id)
                 for item in self.items ]

    def is_equivalent_to(self, layout):
        """ Returns whether two layouts are equivalent, i.e. whether they
            contain the same tasks.
        """
        return isinstance(layout, TaskWindowLayout) and \
            set(self.get_tasks()) == set(layout.get_tasks())
