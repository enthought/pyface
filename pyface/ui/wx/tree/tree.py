# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A tree control with a model/ui architecture. """


import logging
import os
import warnings

import wx


from traits.api import (
    Any, Bool, Callable, Enum, Event, Instance, Int, List, Property, Str,
    Tuple,
)


from pyface.filter import Filter
from pyface.key_pressed_event import KeyPressedEvent
from pyface.sorter import Sorter
from pyface.tree.tree_model import TreeModel
from pyface.ui.wx.gui import GUI
from pyface.ui.wx.image_list import ImageList
from pyface.ui.wx.layout_widget import LayoutWidget
from pyface.wx.drag_and_drop import PythonDropSource, PythonDropTarget


# Create a logger for this module.
logger = logging.getLogger(__name__)


class _Tree(wx.TreeCtrl):
    """ The wx tree control that we delegate to.

    We use this derived class so that we can detect the destruction of the
    tree and remove model listeners etc.

    """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, tree, parent, wxid, style):
        """ Creates a new tree. """

        # Base class constructor.
        super().__init__(parent, wxid, style=style)

        # The tree that we are the toolkit-specific delegate for.
        self._tree = tree

    def Destroy(self):
        """ Destructor. """

        # Stop listenting to the model!
        self._tree._remove_model_listeners(self._tree.model)

        super().Destroy()


class Tree(LayoutWidget):
    """ A tree control with a model/ui architecture. """

    # The default tree style.
    STYLE = wx.TR_EDIT_LABELS | wx.TR_HAS_BUTTONS | wx.CLIP_CHILDREN

    # 'Tree' interface -----------------------------------------------------

    # The tree's filters (empty if no filtering is required).
    filters = List(Instance(Filter))

    # Mode for lines connecting tree nodes which emphasize hierarchy:
    # 'appearance' - only on when lines look good,
    # 'on' - always on, 'off' - always off
    # NOTE: on and off are ignored in favor of show_lines for now
    lines_mode = Enum("appearance", "on", "off")

    # The model that provides the data for the tree.
    model = Instance(TreeModel, ())

    # The root of the tree (this is for convenience, it just delegates to
    # the tree's model).
    root = Property(Any)

    # The objects currently selected in the tree.
    selection = List(Any)

    # Selection mode.
    selection_mode = Enum("single", "extended")

    # Should an image be shown for each node?
    show_images = Bool(True)

    # Should lines be drawn between levels in the tree.
    show_lines = Bool(True)

    # Should the root of the tree be shown?
    show_root = Bool(True)

    # The tree's sorter (None if no sorting is required).
    sorter = Instance(Sorter)

    # Events ----

    # A right-click occurred on the control (not a node!).
    control_right_clicked = Event  # (Point)

    # A key was pressed while the tree has focus.
    key_pressed = Event(Instance(KeyPressedEvent))

    # A node has been activated (ie. double-clicked).
    node_activated = Event  # (Any)

    # A drag operation was started on a node.
    node_begin_drag = Event  # (Any)

    # A (non-leaf) node has been collapsed.
    node_collapsed = Event  # (Any)

    # A (non-leaf) node has been expanded.
    node_expanded = Event  # (Any)

    # A left-click occurred on a node.
    #
    # Tuple(node, point).
    node_left_clicked = Event  # (Tuple)

    # A right-click occurred on a node.
    #
    # Tuple(node, point)
    node_right_clicked = Event  # (Tuple)

    # Private interface ----------------------------------------------------

    # A name to distinguish the tree for debugging!
    #
    # fixme: This turns out to be kinda useful... Should 'Widget' have a name
    # trait?
    _name = Str("Anonymous tree")

    # An optional callback to detect the end of a label edit.  This is
    # useful because the callback will be invoked even if the node label was
    # not actually changed.
    _label_edit_callback = Callable

    # Flag for allowing selection events to be ignored
    _ignore_selection_events = Bool(False)

    # The size of the icons in the tree.
    _image_size = Tuple(Int, Int)

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, image_size=(16, 16), **traits):
        """ Creates a new tree.

        'parent' is the toolkit-specific control that is the tree's parent.

        'image_size' is a tuple in the form (int width, int height) that
        specifies the size of the images (if required) displayed in the tree.

        """
        create = traits.pop('create', None)

        # Base class constructors.
        super().__init__(parent=parent, _image_size=image_size, **traits)

        if create:
            # Create the widget's toolkit-specific control.
            self.create()
            warnings.warn(
                "automatic widget creation is deprecated and will be removed "
                "in a future Pyface version, code should not pass the create "
                "parameter and should instead call create() explicitly",
                DeprecationWarning,
                stacklevel=2,
            )
        elif create is not None:
            warnings.warn(
                "setting create=False is no longer required",
                DeprecationWarning,
                stacklevel=2,
            )

    def _create_control(self, parent):
        # Create the toolkit-specific control.
        self.control = tree = _Tree(
            self, parent, wxid=wx.ID_ANY, style=self._get_style()
        )

        # Wire up the wx tree events.
        tree.Bind(wx.EVT_CHAR, self._on_char)
        tree.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        # fixme: This is not technically correct as context menus etc should
        # appear on a right up (or right click).  Unfortunately,  if we
        # change this to 'EVT_RIGHT_UP' wx does not fire the event unless the
        # right mouse button is double clicked 8^()  Sad,  but true!
        tree.Bind(wx.EVT_RIGHT_DOWN, self._on_right_down)
        # fixme: This is not technically correct as we would really like to use
        # 'EVT_TREE_ITEM_ACTIVATED'. Unfortunately, (in 2.6 at least), it
        # throws an exception when the 'Enter' key is pressed as the wx tree
        # item Id in the event seems to be invalid. It also seems to cause
        # any child frames that my be created in response to the event to
        # appear *behind* the parent window, which is, errrr, not great ;^)
        tree.Bind(wx.EVT_LEFT_DCLICK, self._on_tree_item_activated)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self._on_tree_item_collapsing)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self._on_tree_item_collapsed)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self._on_tree_item_expanding)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self._on_tree_item_expanded)
        tree.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self._on_tree_begin_label_edit)
        tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self._on_tree_end_label_edit)
        tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self._on_tree_begin_drag)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_tree_sel_changed)
        tree.Bind(wx.EVT_TREE_DELETE_ITEM, self._on_tree_delete_item)

        # Enable the tree as a drag and drop target.
        tree.SetDropTarget(PythonDropTarget(self))

        # The image list is a wxPython-ism that caches all images used in the
        # control.
        self._image_list = ImageList(*self._image_size)
        if self.show_images:
            tree.AssignImageList(self._image_list)

        # Mapping from node to wx tree item Ids.
        self._node_to_id_map = {}

        # Add the root node.
        if self.root is not None:
            self._add_root_node(self.root)

        # Listen for changes to the model.
        self._add_model_listeners(self.model)
        return tree

    # ------------------------------------------------------------------------
    # 'Tree' interface.
    # ------------------------------------------------------------------------

    # Properties -----------------------------------------------------------

    def _get_root(self):
        """ Returns the root node of the tree. """

        return self.model.root

    def _set_root(self, root):
        """ Sets the root node of the tree. """

        self.model.root = root

        return

    # Methods -------------------------------------------------------------#

    def collapse(self, node):
        """ Collapses the specified node. """

        wxid = self._get_wxid(node)
        if wxid is not None:
            self.control.Collapse(wxid)

    def edit_label(self, node, callback=None):
        """ Edits the label of the specified node.

        If a callback is specified it will be called when the label edit
        completes WHETHER OR NOT the label was actually changed.

        The callback must take exactly 3 arguments:- (tree, node, label)

        """

        wxid = self._get_wxid(node)
        if wxid is not None:
            self._label_edit_callback = callback
            self.control.EditLabel(wxid)

    def expand(self, node):
        """ Expands the specified node. """

        wxid = self._get_wxid(node)
        if wxid is not None:
            self.control.Expand(wxid)

    def expand_all(self):
        """ Expands every node in the tree. """

        if self.show_root:
            self._expand_item(self._get_wxid(self.root))

        else:
            for child in self._get_children(self.root):
                self._expand_item(self._get_wxid(child))

    def get_parent(self, node):
        """ Returns the parent of a node.

        This will only work iff the node has been displayed in the tree.  If it
        hasn't then None is returned.

        """

        # Has the node actually appeared in the tree yet?
        wxid = self._get_wxid(node)
        if wxid is not None:
            pid = self.control.GetItemParent(wxid)

            # The item data is a tuple.  The first element indicates whether or
            # not we have already populated the item with its children.  The
            # second element is the actual item data.
            populated, parent = self.control.GetItemData(pid)

        else:
            parent = None

        return parent

    def is_expanded(self, node):
        """ Returns True if the node is expanded, otherwise False. """

        wxid = self._get_wxid(node)
        if wxid is not None:
            # If the root node is hidden then it is always expanded!
            if node is self.root and not self.show_root:
                is_expanded = True

            else:
                is_expanded = self.control.IsExpanded(wxid)

        else:
            is_expanded = False

        return is_expanded

    def is_selected(self, node):
        """ Returns True if the node is selected, otherwise False. """

        wxid = self._get_wxid(node)
        if wxid is not None:
            is_selected = self.control.IsSelected(wxid)

        else:
            is_selected = False

        return is_selected

    def refresh(self, node):
        """ Refresh the tree starting from the specified node.

        Call this when the structure of the content has changed DRAMATICALLY.

        """

        # Has the node actually appeared in the tree yet?
        pid = self._get_wxid(node)
        if pid is not None:
            # Delete all of the node's children and re-add them.
            self.control.DeleteChildren(pid)
            self.control.SetItemData(pid, (False, node))

            # Does the node have any children?
            has_children = self._has_children(node)
            self.control.SetItemHasChildren(pid, has_children)

            # fixme: At least on Windows, wx does not fire an expanding
            # event for a hidden root node, so we have to populate the node
            # manually.
            if node is self.root and not self.show_root:
                # Add the child nodes.
                for child in self._get_children(node):
                    self._add_node(pid, child)

            else:
                # Expand it.
                if self.control.IsExpanded(pid):
                    self.control.Collapse(pid)

                self.control.Expand(pid)

    def select(self, node):
        """ Selects the specified node. """

        wxid = self._get_wxid(node)
        if wxid is not None:
            self.control.SelectItem(wxid)

    def set_selection(self, list):
        """ Selects the specified list of nodes. """
        logger.debug("Setting selection to [%s] within Tree [%s]", list, self)

        # Update the control to reflect the target list by unselecting
        # everything and then selecting each item in the list.  During this
        # process, we want to avoid changing our own selection.
        self._ignore_selection_events = True
        self.control.UnselectAll()
        for node in list:
            try:
                self.select(node)
            except:
                logger.exception("Unable to select node [%s]", node)

        self._ignore_selection_events = False

        # Update our selection to reflect the final selection state.
        self.selection = self._get_selection()

    # ------------------------------------------------------------------------
    # 'PythonDropTarget' interface.
    # ------------------------------------------------------------------------

    def on_drag_over(self, x, y, obj, default_drag_result):
        """ Called when a node is dragged over the tree. """

        result = wx.DragNone

        # Find the node that we are dragging over...
        node = self._get_drag_drop_node(x, y)
        if node is not None:
            # Ask the model if the node allows the object to be dropped onto
            # it.
            if self.model.can_drop(node, obj):
                result = default_drag_result

        return result

    def on_drop(self, x, y, obj, default_drag_result):
        """ Called when a node is dropped on the tree. """

        # Find the node that we are dragging over...
        node = self._get_drag_drop_node(x, y)
        if node is not None:
            self.model.drop(node, obj)

        return default_drag_result

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_wxid(self, node):
        """ Returns the wxid for the specified node.

        Returns None if the node has not yet appeared in the tree.

        """

        # The model must generate a unique key for each node (unique within the
        # model).
        key = self.model.get_key(node)

        return self._node_to_id_map.get(key, None)

    def _set_wxid(self, node, wxid):
        """ Sets the wxid for the specified node. """

        # The model must generate a unique key for each node (unique within the
        # model).
        key = self.model.get_key(node)

        self._node_to_id_map[key] = wxid

    def _remove_wxid(self, node):
        """ Removes the wxid for the specified node. """

        # The model must generate a unique key for each node (unique within the
        # model).
        key = self.model.get_key(node)

        try:
            del self._node_to_id_map[key]

        except KeyError:
            # fixme: No, really, this is a serious one... How do we get in this
            # situation.  It came up when using the canvas stuff...
            logger.warning("removing node: %s" % str(node))

    def _get_style(self):
        """ Returns the wx style flags for creating the tree control. """

        # Start with the default flags.
        style = self.STYLE

        # Turn lines off for appearance on *nix.
        # ...for now, show_lines determines if lines are on or off, but
        # eventually lines_mode may eliminate the need for show_lines
        if self.lines_mode == "appearance" and os.name == "posix":
            self.show_lines = False

        if not self.show_lines:
            style = style | wx.TR_NO_LINES

        if not self.show_root:
            # fixme: It looks a little weird, but it we don't have the
            # 'lines at root' style then wx won't draw the expand/collapse
            # image on non-leaf nodes at the root level 8^()
            style = style | wx.TR_HIDE_ROOT | wx.TR_LINES_AT_ROOT

        if self.selection_mode != "single":
            style = style | wx.TR_MULTIPLE | wx.TR_EXTENDED

        return style

    def _add_model_listeners(self, model):
        """ Adds listeners for model changes. """

        # Listen for changes to the model.
        model.observe(self._on_root_changed, "root")
        model.observe(self._on_nodes_changed, "nodes_changed")
        model.observe(self._on_nodes_inserted, "nodes_inserted")
        model.observe(self._on_nodes_removed, "nodes_removed")
        model.observe(self._on_nodes_replaced, "nodes_replaced")
        model.observe(self._on_structure_changed, "structure_changed")

    def _remove_model_listeners(self, model):
        """ Removes listeners for model changes. """

        # Unhook the model event listeners.
        model.observe(self._on_root_changed, "root", remove=True)

        model.observe(self._on_nodes_changed, "nodes_changed", remove=True)

        model.observe(self._on_nodes_inserted, "nodes_inserted", remove=True)

        model.observe(self._on_nodes_removed, "nodes_removed", remove=True)

        model.observe(self._on_nodes_replaced, "nodes_replaced", remove=True)

        model.observe(
            self._on_structure_changed, "structure_changed", remove=True
        )

        # unwire the wx tree events.
        tree = self.control
        tree.Unbind(wx.EVT_CHAR)
        tree.Unbind(wx.EVT_LEFT_DOWN)
        # fixme: This is not technically correct as context menus etc should
        # appear on a right up (or right click).  Unfortunately,  if we
        # change this to 'EVT_RIGHT_UP' wx does not fire the event unless the
        # right mouse button is double clicked 8^()  Sad,  but true!
        tree.Unbind(wx.EVT_RIGHT_DOWN)
        # fixme: This is not technically correct as we would really like to use
        # 'EVT_TREE_ITEM_ACTIVATED'. Unfortunately, (in 2.6 at least), it
        # throws an exception when the 'Enter' key is pressed as the wx tree
        # item Id in the event seems to be invalid. It also seems to cause
        # any child frames that my be created in response to the event to
        # appear *behind* the parent window, which is, errrr, not great ;^)
        tree.Unbind(wx.EVT_LEFT_DCLICK)
        tree.Unbind(wx.EVT_TREE_ITEM_ACTIVATED)
        tree.Unbind(wx.EVT_TREE_ITEM_COLLAPSING)
        tree.Unbind(wx.EVT_TREE_ITEM_COLLAPSED)
        tree.Unbind(wx.EVT_TREE_ITEM_EXPANDING)
        tree.Unbind(wx.EVT_TREE_ITEM_EXPANDED)
        tree.Unbind(wx.EVT_TREE_BEGIN_LABEL_EDIT)
        tree.Unbind(wx.EVT_TREE_END_LABEL_EDIT)
        tree.Unbind(wx.EVT_TREE_BEGIN_DRAG)
        tree.Unbind(wx.EVT_TREE_SEL_CHANGED)
        tree.Unbind(wx.EVT_TREE_DELETE_ITEM)

    def _add_root_node(self, node):
        """ Adds the root node. """

        # Get the tree item image index and the label text.
        image_index = self._get_image_index(node)
        text = self._get_text(node)

        # Add the node.
        wxid = self.control.AddRoot(text, image_index, image_index)

        # This gives the model a chance to wire up trait handlers etc.
        self.model.add_listener(node)

        # If the root node is hidden, get its children.
        if not self.show_root:
            # Add the child nodes.
            for child in self._get_children(node):
                self._add_node(wxid, child)

        # Does the node have any children?
        has_children = self._has_children(node)
        self.control.SetItemHasChildren(wxid, has_children)

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data (which in our case is an arbitrary
        # Python object provided by the tree model).
        if self.show_root:
            self.control.SetItemData(wxid, (not self.show_root, node))

        # Make sure that we can find the node's Id.
        self._set_wxid(node, wxid)

        # Automatically expand the root.
        if self.show_root:
            self.control.Expand(wxid)

    def _add_node(self, pid, node):
        """ Adds 'node' as a child of the node identified by 'pid'.

        If 'pid' is None then we are adding the root node.

        """

        # Get the tree item image index and the label text.
        image_index = self._get_image_index(node)
        text = self._get_text(node)

        # Add the node.
        wxid = self.control.AppendItem(pid, text, image_index, image_index)

        # This gives the model a chance to wire up trait handlers etc.
        self.model.add_listener(node)

        # Does the node have any children?
        has_children = self._has_children(node)
        self.control.SetItemHasChildren(wxid, has_children)

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data (which in our case is an arbitrary
        # Python object provided by the tree model).
        self.control.SetItemData(wxid, (False, node))

        # Make sure that we can find the node's Id.
        self._set_wxid(node, wxid)

    def _insert_node(self, pid, node, index):
        """ Inserts 'node' as a child of the node identified by 'pid'.

        If 'pid' is None then we are adding the root node.

        """

        # Get the tree item image index and the label text.
        image_index = self._get_image_index(node)
        text = self._get_text(node)

        # Add the node.
        wxid = self.control.Sizer.InsertBefore(
            pid, index, text, image_index, image_index
        )

        # This gives the model a chance to wire up trait handlers etc.
        self.model.add_listener(node)

        # Does the node have any children?
        has_children = self._has_children(node)
        self.control.SetItemHasChildren(wxid, has_children)

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data (which in our case is an arbitrary
        # Python object provided by the tree model).
        self.control.SetItemData(wxid, (False, node))

        # Make sure that we can find the node's Id.
        self._set_wxid(node, wxid)

    def _remove_node(self, wxid, node):
        """ Removes a node from the tree. """

        # This gives the model a chance to remove trait handlers etc.
        self.model.remove_listener(node)

        # Remove the reference to the item's data.
        self._remove_wxid(node)
        self.control.SetItemData(wxid, None)

    def _update_node(self, wxid, node):
        """ Updates the image and text of the specified node. """

        # Get the tree item image index.
        image_index = self._get_image_index(node)
        self.control.SetItemImage(wxid, image_index, wx.TreeItemIcon_Normal)
        self.control.SetItemImage(wxid, image_index, wx.TreeItemIcon_Selected)

        # Get the tree item text.
        text = self._get_text(node)
        self.control.SetItemText(wxid, text)

    def _has_children(self, node):
        """ Returns True if a node has children. """

        # fixme: To be correct we *should* apply filtering here, but that
        # seems to blow a hole throught models that have some efficient
        # mechanism for determining whether or not they have children.  There
        # is also a precedent for doing it this way in Windoze, where a node
        # gets marked as though it can be expanded, even thought when the
        # expansion occurs, no children are present!
        return self.model.has_children(node)

    def _get_children(self, node):
        """ Get the children of a node. """

        children = self.model.get_children(node)

        # Filtering....
        filtered_children = []
        for child in children:
            for filter in self.filters:
                if not filter.select(self, node, child):
                    break

            else:
                filtered_children.append(child)

        # Sorting...
        if self.sorter is not None:
            self.sorter.sort(self, node, filtered_children)

        return filtered_children

    def _get_image_index(self, node):
        """ Returns the tree item image index for a node. """

        expanded = self.is_expanded(node)
        selected = self.is_selected(node)

        # Get the image used to represent the node.
        image = self.model.get_image(node, selected, expanded)
        if image is not None:
            image_index = self._image_list.GetIndex(image)

        else:
            image_index = -1

        return image_index

    def _get_drag_drop_node(self, x, y):
        """ Returns the node that is being dragged/dropped on.

        Returns None if the cursor is not over the icon or label of a node.

        """

        data, wxid, flags, point = self._hit_test((x, y))
        if data is not None:
            populated, node = data

        else:
            node = None

        return node

    def _get_text(self, node):
        """ Returns the tree item text for a node. """

        text = self.model.get_text(node)
        if text is None:
            text = ""

        return text

    def _unpack_event(self, event, wxid=None):
        """ Unpacks the event to see whether a tree item was involved. """

        try:
            point = event.GetPosition()

        except:
            point = event.GetPoint()

        return self._hit_test(point, wxid)

    def _hit_test(self, point, wxid=None):
        """ Determines whether a point is within a node's label or icon. """

        flags = wx.TREE_HITTEST_ONITEMLABEL
        if (wxid is None) or (not wxid.IsOk()):
            wxid, flags = self.control.HitTest(point)

        # Warning: On GTK we have to check the flags before we call 'GetItemData'
        # because if we call it when the hit test returns 'nowhere' it will
        # barf (on Windows it simply returns 'None' 8^()
        if flags & wx.TREE_HITTEST_NOWHERE:
            data = None

        elif (
            flags & wx.TREE_HITTEST_ONITEMICON
            or flags & wx.TREE_HITTEST_ONITEMLABEL
        ):

            data = self.control.GetItemData(wxid)

        # fixme: Not sure why 'TREE_HITTEST_NOWHERE' doesn't catch everything!
        else:
            data = None

        return data, wxid, flags, point

    def _get_selection(self):
        """ Returns a list of the selected nodes """

        selection = []
        for wxid in self.control.GetSelections():
            data = self.control.GetItemData(wxid)
            if data is not None:
                populated, node = data
                selection.append(self.model.get_selection_value(node))

        return selection

    def _expand_item(self, wxid):
        """ Recursively expand a tree item. """

        self.control.Expand(wxid)

        cid, cookie = self.control.GetFirstChild(wxid)
        while cid.IsOk():
            self._expand_item(cid)
            cid, cookie = self.control.GetNextChild(wxid, cookie)

        return

    # Trait event handlers -------------------------------------------------

    def _on_root_changed(self, event):
        """ Called when the root of the model has changed. """
        root = event.new
        # Delete everything...
        if self.control is not None:
            self.control.DeleteAllItems()

            self._node_to_id_map = {}

            # ... and then add the root item back in.
            if root is not None:
                self._add_root_node(root)

    def _on_nodes_changed(self, event):
        """ Called when nodes have been changed. """
        node_event = event.new
        self._update_node(self._get_wxid(node_event.node), node_event.node)
        for child in node_event.children:
            cid = self._get_wxid(child)
            if cid is not None:
                self._update_node(cid, child)

    def _on_nodes_inserted(self, event):
        """ Called when nodes have been inserted. """
        node_event = event.new
        parent = node_event.node
        children = node_event.children
        index = node_event.index

        # Has the node actually appeared in the tree yet?
        pid = self._get_wxid(parent)
        if pid is not None:
            # The item data is a tuple.  The first element indicates whether or
            # not we have already populated the item with its children.  The
            # second element is the actual item data.
            if self.show_root or parent is not self.root:
                populated, node = self.control.GetItemData(pid)

            else:
                populated = True

            # If the node is not yet populated then just get the children and
            # add them.
            if not populated:
                for child in self._get_children(parent):
                    self._add_node(pid, child)

            # Otherwise, insert them.
            else:
                # An index of -1 means append!
                if index == -1:
                    index = self.control.GetChildrenCount(pid, False)

                for child in children:
                    self._insert_node(pid, child, index)
                    index += 1

            # The element is now populated!
            if self.show_root or parent is not self.root:
                self.control.SetItemData(pid, (True, parent))

            # Does the node have any children now?
            has_children = self.control.GetChildrenCount(pid) > 0
            self.control.SetItemHasChildren(pid, has_children)

            # If the node is not expanded then expand it.
            if not self.is_expanded(parent):
                self.expand(parent)

    def _on_nodes_removed(self, event):
        """ Called when nodes have been removed. """
        node_event = event.new
        parent = node_event.node

        # Has the node actually appeared in the tree yet?
        pid = self._get_wxid(parent)
        if pid is not None:
            for child in node_event.children:
                cid = self._get_wxid(child)
                if cid is not None:
                    self.control.Delete(cid)

            # Does the node have any children left?
            has_children = self.control.GetChildrenCount(pid) > 0
            self.control.SetItemHasChildren(pid, has_children)

    def _on_nodes_replaced(self, event):
        """ Called when nodes have been replaced. """
        node_event = event.new
        old_new_children = zip(node_event.old_children, node_event.children)
        for old_child, new_child in old_new_children:
            cid = self._get_wxid(old_child)
            if cid is not None:
                # Remove listeners from the old node.
                self.model.remove_listener(old_child)

                # Delete all of the node's children.
                self.control.DeleteChildren(cid)

                # Update the visual appearance of the node.
                self._update_node(cid, new_child)

                # Update the node data.
                #
                # The item data is a tuple.  The first element indicates
                # whether or not we have already populated the item with its
                # children. The second element is the actual item data (which
                # in our case is an arbitrary Python object provided by the
                # tree model).
                self.control.SetItemData(cid, (False, new_child))

                # Remove the old node from the node to Id map.
                self._remove_wxid(old_child)

                # Add the new node to the node to Id map.
                self._set_wxid(new_child, cid)

                # Add listeners to the new node.
                self.model.add_listener(new_child)

                # Does the new node have any children?
                has_children = self._has_children(new_child)
                self.control.SetItemHasChildren(cid, has_children)

        # Update the tree's selection (in case the old node that was replaced
        # was selected, the selection should now include the new node).
        self.selection = self._get_selection()

    def _on_structure_changed(self, event):
        """ Called when the structure of a node has changed drastically. """
        node_event = event.new
        self.refresh(node_event.node)

        return

    # wx event handlers ----------------------------------------------------

    def _on_char(self, event):
        """ Called when a key is pressed when the tree has focus. """

        self.key_pressed = KeyPressedEvent(
            alt_down=event.altDown,
            control_down=event.controlDown,
            shift_down=event.shiftDown,
            key_code=event.KeyCode,
        )

        event.Skip()

    def _on_left_down(self, event):
        """ Called when the left mouse button is clicked on the tree. """

        data, id, flags, point = self._unpack_event(event)

        # Save point for tree_begin_drag method to workaround a bug in ?? when
        # wx.TreeEvent.GetPoint returns only (0,0).  This happens under linux
        # when using wx-2.4.2.4, for instance.
        self._point_left_clicked = point

        # Did the left click occur on a tree item?
        if data is not None:
            populated, node = data

            # Trait event notification.
            self.node_left_clicked = node, point

        # Give other event handlers a chance.
        event.Skip()

    def _on_right_down(self, event):
        """ Called when the right mouse button is clicked on the tree. """

        data, id, flags, point = self._unpack_event(event)

        # Did the right click occur on a tree item?
        if data is not None:
            populated, node = data

            # Trait event notification.
            self.node_right_clicked = node, point

        # Otherwise notify that the control itself was clicked
        else:
            self.control_right_clicked = point

        # Give other event handlers a chance.
        event.Skip()

    def _on_tree_item_activated(self, event):
        """ Called when a tree item is activated (i.e., double clicked). """

        # fixme: See the comment where the events are wired up for more
        # information.

        ##         # Which item was activated?
        ##         wxid = event.GetItem()

        # Which item was activated.
        point = event.GetPosition()
        wxid, flags = self.control.HitTest(point)

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, node = self.control.GetItemData(wxid)

        # Trait event notiification.
        self.node_activated = node

    def _on_tree_item_collapsing(self, event):
        """ Called when a tree item is about to collapse. """

        # Which item is collapsing?
        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, node = self.control.GetItemData(wxid)

        # Give the model a chance to veto the collapse.
        if not self.model.is_collapsible(node):
            event.Veto()

    def _on_tree_item_collapsed(self, event):
        """ Called when a tree item has been collapsed. """

        # Which item was collapsed?
        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, node = self.control.GetItemData(wxid)

        # Make sure that the item's 'closed' icon is displayed etc.
        self._update_node(wxid, node)

        # Trait event notification.
        self.node_collapsed = node

    def _on_tree_item_expanding(self, event):
        """ Called when a tree item is about to expand. """

        # Which item is expanding?
        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, node = self.control.GetItemData(wxid)

        # Give the model a chance to veto the expansion.
        if self.model.is_expandable(node):
            # Lazily populate the item's children.
            if not populated:
                # Add the child nodes.
                for child in self._get_children(node):
                    self._add_node(wxid, child)

                # The element is now populated!
                self.control.SetItemData(wxid, (True, node))

        else:
            event.Veto()

    def _on_tree_item_expanded(self, event):
        """ Called when a tree item has been expanded. """

        # Which item was expanded?
        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, node = self.control.GetItemData(wxid)

        # Make sure that the node's 'open' icon is displayed etc.
        self._update_node(wxid, node)

        # Trait event notification.
        self.node_expanded = node

    def _on_tree_begin_label_edit(self, event):
        """ Called when the user has started editing an item's label. """

        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, node = self.control.GetItemData(wxid)

        # Give the model a chance to veto the edit.
        if not self.model.is_editable(node):
            event.Veto()

    def _on_tree_end_label_edit(self, event):
        """ Called when the user has finished editing am item's label. """

        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, node = self.control.GetItemData(wxid)

        # Give the model a chance to veto the edit.
        label = event.GetLabel()

        # Making sure the new label is not an empty string

        if (
            label is not None
            and len(label) > 0
            and self.model.can_set_text(node, label)
        ):

            def end_label_edit():
                """ Called to complete the label edit. """

                # Set the node's text.
                self.model.set_text(node, label)

                # If a label edit callback was specified (in the call to
                # 'edit_label'), then call it).
                if self._label_edit_callback is not None:
                    self._label_edit_callback(self, node, label)

                return

            # We use a deffered call here, because a name change can trigger
            # the structure of a node to change, and hence the actual tree
            # nodes might get moved/deleted before the label edit operation has
            # completed.  When this happens wx gets very confused!  By using
            # 'invoke_later' we allow the label edit to complete.
            GUI.invoke_later(end_label_edit)

        else:
            event.Veto()

            # If a label edit callback was specified (in the call to
            # 'edit_label'), then call it).
            if self._label_edit_callback is not None:
                self._label_edit_callback(self, node, label)

    def _on_tree_begin_drag(self, event):
        """ Called when a drag operation is starting on a tree item. """

        # Get the node, its id and the point where the event occurred.
        data, wxid, flags, point = self._unpack_event(event, event.GetItem())

        if point == (0, 0):
            # Apply workaround for GTK.
            point = self.point_left_clicked
            wxid, flags = self.HitTest(point)
            data = self.control.GetItemData(wxid)

        if data is not None:
            populated, node = data

            # Give the model a chance to veto the drag.
            if self.model.is_draggable(node):
                # We ask the model for the actual value to drag.
                drag_value = self.model.get_drag_value(node)

                # fixme: This is a terrible hack to get the binding x passed
                # during a drag operation.  Bindings should probably *always*
                # be dragged and our drag and drop mechanism should allow
                # extendable ways to extract the actual data.
                from pyface.wx.drag_and_drop import clipboard

                clipboard.node = [node]

                # Make sure that the tree selection is updated before we start
                # the drag. If we don't do this then if the first thing a
                # user does is drag a tree item (i.e., without a separate click
                # to select it first) then the selection appears empty.
                self.selection = self._get_selection()

                # Start the drag.
                PythonDropSource(self.control, drag_value, self)

                # Trait event notification.
                self.node_begin_drag = node

            else:
                event.Veto()

        return

    # fixme: This is part of the drag and drop hack...
    def on_dropped(self):
        """ Callback invoked when a drag/drop operation has completed. """

        from pyface.wx.drag_and_drop import clipboard

        clipboard.node = None

    def _on_tree_sel_changed(self, event):
        """ Called when the selection is changed. """

        # Update our record of the selection to whatever was selected in the
        # tree UNLESS we are ignoring selection events.
        if not self._ignore_selection_events:

            # Trait notification.
            self.selection = self._get_selection()

    def _on_tree_delete_item(self, event):
        """ Called when a tree item is being been deleted. """

        # Which item is being deleted?
        wxid = event.GetItem()

        # Check if GetItemData() returned a valid to tuple to unpack
        # ...if so, remove the node from the tree, otherwise just return
        #
        # fixme: Whoever addeed this code (and the comment above) didn't say
        # when this was occurring. This is method is called in response to a wx
        # event to delete an item and hence the item data should never be None
        # surely?!? Was it happening just on one platform?!?
        if self.control is None:
            return
        try:
            data = self.control.GetItemData(wxid)
        except Exception:
            # most likely control is in the process of being destroyed
            data = None

        if data is not None:
            # The item data is a tuple.  The first element indicates whether or
            # not we have already populated the item with its children.  The
            # second element is the actual item data.
            populated, node = data

            # Remove the node.
            self._remove_node(wxid, node)
