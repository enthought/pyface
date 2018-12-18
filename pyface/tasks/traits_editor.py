# Enthought library imports.
from traits.api import HasTraits, Instance

# Local imports.
from pyface.tasks.editor import Editor


class TraitsEditor(Editor):
    """ An Editor that displays a Traits UI View.
    """

    #### TraitsEditor interface ###############################################

    # The model object to view. If not specified, the editor is used instead.
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
            return {'object': self.model, 'editor': self}
        return super(TraitsEditor, self).trait_context()

    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific contents of the editor.
        """
        self.ui = self.edit_traits(kind='subpanel', parent=parent)
        self.control = self.ui.control

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the editor.
        """
        self.control = None
        if self.ui is not None:
            self.ui.dispose()
        self.ui = None
