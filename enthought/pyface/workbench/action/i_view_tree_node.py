""" A tree node for objects that implement the 'IView' interface. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView
from enthought.traits.api import Undefined
from enthought.traits.ui.api import TreeNode


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

#### EOF ######################################################################
