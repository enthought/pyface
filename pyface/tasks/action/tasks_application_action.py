from traits.api import Instance

from pyface.action.api import GUIApplicationAction
from pyface.tasks.tasks_application import TasksApplication
from pyface.tasks.task_window_layout import TaskWindowLayout


class TasksApplicationAction(GUIApplicationAction):

    #: The Tasks application the action applies to.
    application = Instance(TasksApplication)


class CreateTaskWindowAction(TasksApplicationAction):
    """ A standard 'New Window' menu action. """
    name = u'New Window'
    accelerator = 'Ctrl+N'

    #: The task window wayout to use when creating the new window.
    layout = Instance('pyface.tasks.task_window_layout.TaskWindowLayout')

    def perform(self, event=None):
        window = self.application.create_window(layout=self.layout)
        self.application.add_window(window)

    def _layout_default(self):
        if self.application.default_layout:
            layout = self.application.default_layout[0]
        else:
            layout = TaskWindowLayout()
            if self.task_factories:
                layout.items = [self.task_factories[0].id]
        return layout
