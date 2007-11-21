""" A UI that allows the user to choose a view. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView
from enthought.traits.api import Any, HasTraits, Instance, List, Str
from enthought.traits.api import TraitError, Undefined
from enthought.traits.ui.api import Item, View
from enthought.traits.ui.menu import Action # fixme: Non-api import!


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


# Local imports.
from view_tree_editor import view_tree_editor


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

    #### Trait initializers ###################################################

    def _view_manager_default(self):
        """ Trait initializer. """

        return ViewManager(window=self.window)
    
    #### Trait change handlers ################################################
    
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
