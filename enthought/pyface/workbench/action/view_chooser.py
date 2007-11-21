""" A UI that allows the user to choose a view. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView
from enthought.traits.api import Any, HasTraits, Instance, TraitError
from enthought.traits.ui.api import Item, TreeEditor, TreeNode, View
from enthought.traits.ui.menu import Action # fixme: Non-api import!

# Local imports.
from i_view_tree_node import IViewTreeNode
from workbench_window_tree_node import Category, WorkbenchWindowTreeNode


class ViewChooser(HasTraits):
    """ Allow the user to choose a view.

    This implementation shows views in a tree grouped by category.

    """
    
    # The window that contains the views to choose from.
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    # The currently selected tree item (at any point in time this might be
    # either None, a view category, or a view).
    selected = Any

    # The selected view (None if the selected item is not a view).
    view = Instance(IView)
    
    #### Traits UI views ######################################################
    
    traits_ui_view = View(
        Item(
            name       = 'window',
            editor     = TreeEditor(
                nodes  = [
                    WorkbenchWindowTreeNode(
                        auto_open = False,
                        children  = 'categories',
                        label     = '=Views',
                        rename    = False,
                        copy      = False,
                        delete    = False,
                        insert    = False,
                        menu      = None,
                    ),

                    TreeNode(
                        node_for  = [Category],
                        auto_open = False,
                        children  = 'views',
                        label     = 'name',
                        rename    = False,
                        copy      = False,
                        delete    = False,
                        insert    = False,
                        menu      = None,
                    ),
                    
                    IViewTreeNode(
                        auto_open = False,
                        label     = 'name',
                        rename    = False,
                        copy      = False,
                        delete    = False,
                        insert    = False,
                        menu      = None,
                    )
                ],

                editable   = False,
                hide_root  = True,
                selected   = 'selected',
                show_icons = False
            ),
            show_label = False
        ),

        buttons   = [
            Action(name='OK', enabled_when='view is not None'), 'Cancel'
        ],

        resizable = True,
        style     = 'custom',
        title     = 'Show View',

        width     = .2,
        height    = .4
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
