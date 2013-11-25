# Local imports.
from pyface.tasks.task_pane import TaskPane
from pyface.tasks.enaml_pane import EnamlPane


class EnamlTaskPane(EnamlPane, TaskPane):
    """ Create a Task pane for Enaml Components. """
