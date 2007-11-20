""" A UI that allows the user to select a view. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView
from enthought.traits.api import Any, HasTraits, Instance, List, Str
from enthought.traits.api import TraitError, Undefined
from enthought.traits.ui.api import Item, TreeEditor, TreeNode, View

# fixme: Why does this import not come from an api file like everything else?
from enthought.traits.ui.menu import Action


class Category(HasTraits):
    """ A view category. """

    # The name of the category.
    name = Str

    # The views in the category.
    views = List


class ViewManager(HasTraits):
    """ The view manager. """
    
    # All of the window's views grouped by their category.
    categories = List(Category)

    # The window that we manage the views of.
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    ###########################################################################
    # 'ViewManager' interface.
    ###########################################################################

    def _categories_default(self):
        """ Trait initializer. """

        # Collate the views into their categories.
        categories_by_name = {}
        for view in self.window.views:
            category = categories_by_name.get(view.category)
            if category is None:
                category = Category(name=view.category)
                categories_by_name[view.category] = category

            category.views.append(view)

        categories = categories_by_name.values()
        categories.sort(key=lambda x: x.name)
            
        return categories


class IViewTreeNode(TreeNode):
    """ A tree node for objects that implement the 'IView' interface.

    This node does *not* recognise objects that can be *adapted* to the 'IView'
    interface, only those that actually implement it. If we wanted to allow
    for adaptation we would have to work out a way for the rest of the
    'TreeNode' code to access the adapter, not the original object. We could,
    of course override every method, but that seems a little, errr, tedious.
    We could probably do with something like in the PyFace tree where there
    is a method that returns the actual object that we want to manipulate.

    """
    
    def is_node_for(self, obj):
        """ Returns whether this is the node that handles a specified object.
        
        """

        # By checking for 'is obj' here, we are *not* allowing adaptation. See
        # the class doc string for details.
        return IView(obj, Undefined) is obj


# A tree editor that shows views in their categories.
tree_editor = TreeEditor(
    nodes = [
        TreeNode(
            node_for  = [ViewManager],
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
        ),
    ],

    editable   = False,
    hide_root  = True,
    selected   = 'selected',
    show_icons = False
)


class ViewChooser(HasTraits):
    """ Allow the user to choose a view.

    This implementation shows views in a tree grouped by category.

    """
    
    # The view manager.
    #
    # fixme: It seems weird that we have to create this extra object so that
    # we can have a tree editor for this trait!
    view_manager = Instance(ViewManager)
    
    # The window that we manage the views of.
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    # The currently selected tree item.
    selected = Any

    # The chosen view (None if no view has been chosen).
    view = Instance(IView)
    
    #### Traits UI views ######################################################
    
    traits_ui_view = View(
        Item(
            name       = 'view_manager',
            editor     = tree_editor,
            show_label = False,
            width      = 0.1,
        ),

        buttons  = [
            Action(name='OK', enabled_when='view is not None'), 'Cancel'
        ],

        resizable = True,
        style     = 'custom',
        title     = 'Show View',

        width     = .3,
        height    = .3
    )

    ###########################################################################
    # 'ShowView' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _view_manager_default(self):
        """ Trait initializer. """

        return ViewManager(window=self.window)
    
    #### Trait change handlers ################################################
    
    def _selected_changed(self, old, new):
        """ Static trait change handler. """

        # If the assigment fails then the selected object does *not* implement
        # the 'IView' interface.
        try:
            self.view = new

        except TraitError:
            self.view = None
        
        return

#### EOF ######################################################################
