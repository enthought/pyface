# Enthought library imports.
from traits.api import Instance, on_trait_change
from enaml.components.constraints_widget import ConstraintsWidget

# local imports
from pyface.tasks.editor import Editor


class EnamlEditor(Editor):
    """ Create an Editor for Enaml Components.
    """

    #### EnamlEditor interface ##############################################

    component = Instance(ConstraintsWidget)

    def create_component(self):
        raise NotImplementedError

    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################

    def create(self, parent):
        self.component = self.create_component()
        self.component.setup(parent=parent)
        self.control = self.component.toolkit_widget
        self.component.on_trait_change(self.size_hint_changed, 'size_hint_updated')

    def destroy(self):
        self.control = None
        self.component.destroy()
        
