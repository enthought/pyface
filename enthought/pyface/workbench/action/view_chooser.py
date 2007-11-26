""" A UI that allows the user to choose a view. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView, WorkbenchWindow
from enthought.traits.api import Any, Bool, HasTraits, Instance, List, Str
from enthought.traits.api import TraitError, Undefined
from enthought.traits.ui.api import Item, TreeEditor, TreeNode, View
from enthought.traits.ui.menu import Action # fixme: Non-api import!


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


from enthought.traits.ui.api import Handler
class ViewChooserHandler(Handler):
    """ The traits UI handler for the view chooser. """
    
    ###########################################################################
    # 'Handler' interface.
    ###########################################################################

    def close(self, info, is_ok):
        """ Close a dialog-based user interface. """

        info.object._closing = True
        
        return super(ViewChooserHandler, self).close(info, is_ok)
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _select_first_node(self, info):
        """ Select the first node in the tree (if there is one). """

        root = info.object.root
        
        if len(root.children) > 0:
            node = root.children[0]
            info.object.selected_page = node.page

        return

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

    #### Private interface ####################################################

    # Hack to get around the bug in the Qt tree editor where selection events
    # get fired *after* the 'OK' button is pressed.
    _closing = Bool
    
    #### Traits UI views ######################################################
    
    traits_ui_view = View(
        Item(
            name       = 'window',
            editor     = TreeEditor(
                nodes  = [
                    WorkbenchWindowTreeNode(
                        auto_open = False,
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

        handler   = ViewChooserHandler(),
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

        # Hack to get around the bug in the Qt tree editor where selection
        # events get fired *after* the 'OK' button is pressed.
        if self._closing:
            return
        
        # If the assignment fails then the selected object does *not* implement
        # the 'IView' interface.
        try:
            self.view = new

        except TraitError:
            self.view = None
        
        return

#### EOF ######################################################################
