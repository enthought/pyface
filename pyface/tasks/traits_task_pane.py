# Enthought library imports.
from traits.api import HasTraits, Instance
from traitsui.api import UI, ViewElement

# Local imports.
from task_pane import TaskPane


class TraitsTaskPane(TaskPane):
    """ A TaskPane that displays a Traits UI View.
    """

    #### TraitsTaskPane interface #############################################

    # The model object to view. If not specified, the pane is used instead.
    obj = Instance(HasTraits)

    # An (optional) view for use if a model object is specfied.
    obj_view = Instance(ViewElement)

    # The UI object associated with the Traits view, if it has been constructed.
    ui = Instance(UI)

    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        obj = self.obj if self.obj else self
        view = self.obj_view if self.obj and self.obj_view else None
        self.ui = obj.edit_traits(view=view, kind='subpanel', parent=parent)
        self.control = self.ui.control

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        self.ui.dispose()
        self.control = self.ui = None
