# Enthought library imports.
from traits.api import HasTraits, Instance
from traitsui.api import UI, ViewElement

# Local imports.
from editor import Editor


class TraitsEditor(Editor):
    """ An Editor that displays a Traits UI View.
    """

    #### TraitsEditor interface ###############################################

    # The model object to view. If not specified, the editor is used instead.
    obj = Instance(HasTraits)

    # An (optional) view for use if a model object is specfied.
    obj_view = Instance(ViewElement)

    # The UI object associated with the Traits view, if it has been constructed.
    ui = Instance(UI)

    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific contents of the editor.
        """
        obj = self.obj if self.obj else self
        view = self.obj_view if self.obj and self.obj_view else None
        self.ui = obj.edit_traits(view=view, kind='subpanel', parent=parent)
        self.control = self.ui.control

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the editor.
        """
        self.control = None
        self.ui.dispose()
        self.ui = None
