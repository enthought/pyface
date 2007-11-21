""" A tree node for workbench windows that displays the window's views. """


# Enthought library imports.
from enthought.pyface.workbench.api import WorkbenchWindow
from enthought.traits.api import HasTraits, List, Str
from enthought.traits.ui.api import TreeNode


class Category(HasTraits):
    """ A view category. """

    # The name of the category.
    name = Str

    # The views in the category.
    views = List


class WorkbenchWindowTreeNode(TreeNode):
    """ A tree node for workbench windows that displays the window's views.

    The views are grouped by their category.

    """

    #### 'TreeNode' interface #################################################
    
    # List of object classes that the node applies to.
    node_for = [WorkbenchWindow]

    ###########################################################################
    # 'TreeNode' interface.
    ###########################################################################

    def get_children(self, object):
        """ Get the object's children. """

        # Collate the window's views into categories.
        categories_by_name = self._get_categories_by_name(object)

        categories = categories_by_name.values()
        categories.sort(key=lambda category: category.name)
            
        return categories

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_categories_by_name(self, window):
        """ Return a dictionary containing all categories keyed by name. """

        categories_by_name = {}
        for view in window.views:
            category = categories_by_name.get(view.category)
            if category is None:
                category = Category(name=view.category)
                categories_by_name[view.category] = category

            category.views.append(view)

        return categories_by_name

#### EOF ######################################################################
