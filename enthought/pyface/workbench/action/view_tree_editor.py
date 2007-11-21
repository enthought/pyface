""" A UI that allows the user to select a view. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView, WorkbenchWindow
from enthought.traits.api import HasTraits, List, Str, Undefined
from enthought.traits.ui.api import TreeEditor, TreeNode


class Category(HasTraits):
    """ A view category. """

    # The name of the category.
    name = Str

    # The views in the category.
    views = List


class WorkbenchWindowTreeNode(TreeNode):
    """ A tree node for workbench windows. """

    node_for = [WorkbenchWindow]

    def get_children ( self, object ):
        """ Gets the object's children. """

        # Collate the window's views into categories.
        categories_by_name = {}
        for view in object.views:
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

        # By checking for 'is obj' here, we are *not* allowing adaptation (if
        # we were allowing adaptation it would be 'is not None'). See the class
        # doc string for details.
        return IView(obj, Undefined) is obj


view_tree_nodes = [
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
]


view_tree_editor = TreeEditor(
    nodes      = view_tree_nodes,
    editable   = False,
    hide_root  = True,
    selected   = 'selected',
    show_icons = False
)

#### EOF ######################################################################
