# Enthought library imports.
from traits.api import Instance, on_trait_change
from enaml.widgets.constraints_widget import ConstraintsWidget

# local imports
from pyface.tasks.dock_pane import DockPane


class EnamlDockPane(DockPane):
    """ Create an Dock pane for Enaml Components.
    """

    #### EnamlDockPane interface ##############################################

    component = Instance(ConstraintsWidget)

    def create_component(self):
        raise NotImplementedError


    ###########################################################################
    # 'IDockPane' interface.
    ###########################################################################

    def create_contents(self, parent):
        self.component = self.create_component()
        self.component.setup(parent=parent)
        contents = self.component.toolkit_widget
        return contents

    def destroy(self):        
        self.component.destroy()
        # Destroy the dock control.
        super(EnamlDockPane, self).destroy()

        
