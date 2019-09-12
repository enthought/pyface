""" A UI that allows the user to choose a view. """


# Enthought library imports.
from pyface.workbench.api import IView, WorkbenchWindow
from traits.api import Any, HasTraits, Instance, List, Str
from traits.api import TraitError, Undefined
from traitsui.api import Item, TreeEditor, TreeNode, View
from traitsui.menu import Action # fixme: Non-api import!


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

        categories = list(categories_by_name.values())
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
    We could probably do with something like in the Pyface tree where there
    is a method that returns the actual object that we want to manipulate.

    """

    def is_node_for(self, obj):
        """ Returns whether this is the node that handles a specified object.

        """

        # By checking for 'is obj' here, we are *not* allowing adaptation (if
        # we were allowing adaptation it would be 'is not None'). See the class
        # doc string for details.
        return IView(obj, Undefined) is obj

    def get_icon(self, obj, is_expanded):
        """ Returns the icon for a specified object. """

        if obj.image is not None:
            icon = obj.image

        else:
            # fixme: A bit of magic here! Is there a better way to say 'use
            # the default leaf icon'?
            icon = '<item>'

        return icon


class ViewChooser(HasTraits):
    """ Allow the user to choose a view.

    This implementation shows views in a tree grouped by category.

    """

    # The window that contains the views to choose from.
    window = Instance('pyface.workbench.api.WorkbenchWindow')

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
                        auto_open = True,
                        label     = '=Views',
                        rename    = False,
                        copy      = False,
                        delete    = False,
                        insert    = False,
                        menu      = None,
                    ),

                    TreeNode(
                        node_for  = [Category],
                        auto_open = True,
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
                show_icons = True
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
