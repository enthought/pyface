""" A UI that allows the user to choose a view. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView
from enthought.traits.api import Any, HasTraits, Instance, TraitError
from enthought.traits.ui.api import Item, View
from enthought.traits.ui.menu import Action # fixme: Non-api import!

# Local imports.
from view_tree_editor import view_tree_editor


class ViewChooser(HasTraits):
    """ Allow the user to choose a view.

    This implementation shows views in a tree grouped by category.

    """
    
    # The window that contains the views to choose from.
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    # The currently selected tree item (at any point in time this might be
    # either None, a view category, or a view).
    selected = Any

    # The chosen view (None if no view has been chosen).
    view = Instance(IView)
    
    #### Traits UI views ######################################################
    
    traits_ui_view = View(
        Item(
            name       = 'window',
            editor     = view_tree_editor,
            show_label = False,
        ),

        buttons   = [
            Action(name='OK', enabled_when='view is not None'), 'Cancel'
        ],

        resizable = True,
        style     = 'custom',
        title     = 'Show View',

        width     = .3,
        height    = .3
    )

    ###########################################################################
    # 'ViewChooser' interface.
    ###########################################################################
    
    def _selected_changed(self, old, new):
        """ Static trait change handler. """

        # If the assignment fails then the selected object does *not* implement
        # the 'IView' interface.
        try:
            self.view = new

        except TraitError:
            self.view = None
        
        return

#### EOF ######################################################################
