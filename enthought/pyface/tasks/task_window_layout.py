# Enthought library imports.
from enthought.traits.api import Dict, HasStrictTraits, Instance, List, Str, \
     Tuple

# Local imports.
from task_layout import TaskLayout


class TaskWindowLayout(HasStrictTraits):
    """ A picklable object that describes the layout and state of a TaskWindow.
    """

    # The ID of the active task. If unspecified, the first task will be active.
    active_task_id = Str

    # The IDs of all the tasks attached to the window.
    task_ids = List(Str)

    # The position of the window.
    position = Tuple(-1, -1)

    # The size of the window.
    size = Tuple(800, 600)

    # A map from task IDs to their respective layouts. Set by the framework.
    layout_state = Dict(Str, Instance(TaskLayout))
