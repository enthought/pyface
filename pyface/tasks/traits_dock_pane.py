# Enthought library imports.
from traits.api import HasTraits, Instance

# Local imports.
from pyface.tasks.dock_pane import DockPane


class TraitsDockPane(DockPane):
    """ A DockPane that displays a Traits UI View.
    """

    #### TraitsDockPane interface #############################################

    # The model object to view. If not specified, the pane is used instead.
    model = Instance(HasTraits)

    # The UI object associated with the Traits view, if it has been constructed.
    ui = Instance('traitsui.ui.UI')

    ###########################################################################
    # 'HasTraits' interface.
    ###########################################################################

    def trait_context(self):
        """ Use the model object for the Traits UI context, if appropriate.
        """
        if self.model:
            return { 'object': self.model, 'pane': self }
        return super(TraitsDockPane, self).trait_context()

    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        # Destroy the Traits-generated control inside the dock control.
        self.ui.dispose()
        self.ui = None

        # Destroy the dock control.
        super(TraitsDockPane, self).destroy()

    ###########################################################################
    # 'IDockPane' interface.
    ###########################################################################

    def create_contents(self, parent):
        """ Create and return the toolkit-specific contents of the dock pane.
        """
        self.ui = self.edit_traits(kind='subpanel', parent=parent)
        return self.ui.control
