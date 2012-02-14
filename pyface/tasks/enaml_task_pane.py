# Enthought library imports.
from traits.api import Instance, on_trait_change
from enaml.components.constraints_widget import ConstraintsWidget

# local imports
from pyface.tasks.task_pane import TaskPane


class EnamlTaskPane(TaskPane):
    """ Create a Task pane for Enaml Components.
    """

    #### EnamlTaskPane interface ##############################################

    component = Instance(ConstraintsWidget)

    def create_component(self):
        raise NotImplementedError


    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def create(self, parent):
        self.component = self.create_component()
        self.component.setup(parent=parent)
        self.control = self.component.toolkit_widget

    def destroy(self):
        self.control = None
        self.component.destroy()
        
