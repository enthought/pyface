# Enthought library imports.
from traits.api import HasTraits, Instance
from traitsui.api import UI

# Local imports.
from task_pane import TaskPane


class TraitsTaskPane(TaskPane):
    """ A TaskPane that displays a Traits UI View.
    """

    #### TraitsTaskPane interface #############################################

    # The model object to view. If not specified, the pane is used instead.
    model = Instance(HasTraits)

    # The UI object associated with the Traits view, if it has been constructed.
    ui = Instance(UI)

    ###########################################################################
    # 'HasTraits' interface.
    ###########################################################################

    def trait_context(self):
        """ Use the model object for the Traits UI context, if appropriate.
        """
        if self.model:
            return { 'object': self.model, 'pane': self }
        return super(TraitsTaskPane, self).trait_context()

    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        self.ui = self.edit_traits(kind='subpanel', parent=parent)
        self.control = self.ui.control

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        self.ui.dispose()
        self.control = self.ui = None
