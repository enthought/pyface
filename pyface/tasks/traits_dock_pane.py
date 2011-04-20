# Enthought library imports.
from traits.api import HasTraits, Instance
from traitsui.api import UI, ViewElement

# Local imports.
from dock_pane import DockPane


class TraitsDockPane(DockPane):
    """ A DockPane that displays a Traits UI View.
    """

    #### TraitsDockPane interface #############################################

    # The model object to view. If not specified, the pane is used instead.
    obj = Instance(HasTraits)

    # An (optional) view for use if a model object is specfied.
    obj_view = Instance(ViewElement)

    # The UI object associated with the Traits view, if it has been constructed.
    ui = Instance(UI)

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
        obj = self.obj if self.obj else self
        view = self.obj_view if self.obj and self.obj_view else None
        self.ui = obj.edit_traits(view=view, kind='subpanel', parent=parent)
        return self.ui.control
