""" A UI that allows the user to select a view. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView
from enthought.traits.api import Undefined
from enthought.traits.ui.api import TreeEditor, TreeNode

# Local imports.
from view_chooser import Category, ViewManager


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
