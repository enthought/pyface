# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A viewer based on a tree control. """

import warnings

import wx

from traits.api import Bool, Enum, Event, Instance, Int, List, Tuple

from pyface.ui.wx.image_list import ImageList
from pyface.viewer.content_viewer import ContentViewer
from pyface.viewer.tree_content_provider import TreeContentProvider
from pyface.viewer.tree_label_provider import TreeLabelProvider
from pyface.wx.drag_and_drop import PythonDropSource


class TreeViewer(ContentViewer):
    """ A viewer based on a tree control. """

    # The default tree style.
    STYLE = wx.TR_EDIT_LABELS | wx.TR_HAS_BUTTONS | wx.CLIP_CHILDREN

    # 'TreeViewer' interface -----------------------------------------------

    # The content provider provides the actual tree data.
    content_provider = Instance(TreeContentProvider)

    # The label provider provides, err, the labels for the items in the tree
    # (a label can have text and/or an image).
    label_provider = Instance(TreeLabelProvider, ())

    # Selection mode (must be either of 'single' or 'extended').
    selection_mode = Enum("single", "extended")

    # The currently selected elements.
    selection = List()

    # Should an image be shown for each element?
    show_images = Bool(True)

    # Should the root of the tree be shown?
    show_root = Bool(True)

    # Events ----

    # An element has been activated (ie. double-clicked).
    element_activated = Event()

    # A drag operation was started on an element.
    element_begin_drag = Event()

    # An element that has children has been collapsed.
    element_collapsed = Event()

    # An element that has children has been expanded.
    element_expanded = Event()

    # A left-click occurred on an element.
    element_left_clicked = Event()

    # A right-click occurred on an element.
    element_right_clicked = Event()

    # A key was pressed while the tree is in focus.
    key_pressed = Event()

    # The size of the icons in the tree.
    _image_size = Tuple(Int, Int)

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, image_size=(16, 16), **traits):
        """ Creates a new tree viewer.

        'parent' is the toolkit-specific control that is the tree's parent.

        'image_size' is a tuple in the form (int width, int height) that
        specifies the size of the label images (if any) displayed in the tree.

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
        self.control = tree = wx.TreeCtrl(parent, -1, style=self._get_style())

        # Wire up the wx tree events.
        tree.Bind(wx.EVT_CHAR, self._on_char)
        tree.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        tree.Bind(wx.EVT_RIGHT_DOWN, self._on_right_down)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._on_tree_item_activated)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self._on_tree_item_collapsed)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self._on_tree_item_collapsing)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self._on_tree_item_expanded)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self._on_tree_item_expanding)
        tree.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self._on_tree_begin_label_edit)
        tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self._on_tree_end_label_edit)
        tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self._on_tree_begin_drag)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_tree_sel_changed)

        # The image list is a wxPython-ism that caches all images used in the
        # control.
        self._image_list = ImageList(*self._image_size)
        if self.show_images:
            tree.AssignImageList(self._image_list)

        # Mapping from element to wx tree item Ids.
        self._element_to_id_map = {}

        # Add the root item.
        if self.input is not None:
            self._add_element(None, self.input)

        return tree

    # ------------------------------------------------------------------------
    # 'TreeViewer' interface.
    # ------------------------------------------------------------------------

    def is_expanded(self, element):
        """ Returns True if the element is expanded, otherwise False. """

        key = self._get_key(element)

        if key in self._element_to_id_map:
            is_expanded = self.control.IsExpanded(self._element_to_id_map[key])

        else:
            is_expanded = False

        return is_expanded

    def is_selected(self, element):
        """ Returns True if the element is selected, otherwise False. """

        key = self._get_key(element)

        if key in self._element_to_id_map:
            is_selected = self.control.IsSelected(self._element_to_id_map[key])

        else:
            is_selected = False

        return is_selected

    def refresh(self, element):
        """ Refresh the tree starting from the specified element.

        Call this when the STRUCTURE of the content has changed.

        """

        # Has the element actually appeared in the tree yet?
        pid = self._element_to_id_map.get(self._get_key(element), None)
        if pid is not None:
            # The item data is a tuple.  The first element indicates whether or
            # not we have already populated the item with its children.  The
            # second element is the actual item data.
            populated, element = self.control.GetItemData(pid)

            # fixme: We should find a cleaner way other than deleting all of
            # the element's children and re-adding them!
            self._delete_children(pid)
            self.control.SetItemData(pid, (False, element))

            # Does the element have any children?
            has_children = self.content_provider.has_children(element)
            self.control.SetItemHasChildren(pid, has_children)

            # Expand it.
            self.control.Expand(pid)

        else:
            print("**** pid is None!!! ****")

    def update(self, element):
        """ Update the tree starting from the specified element.

        Call this when the APPEARANCE of the content has changed.

        """

        pid = self._element_to_id_map.get(self._get_key(element), None)
        if pid is not None:
            self._refresh_element(pid, element)

            for child in self.content_provider.get_children(element):
                cid = self._element_to_id_map.get(self._get_key(child), None)
                if cid is not None:
                    self._refresh_element(cid, child)

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_style(self):
        """ Returns the wx style flags for creating the tree control. """

        # Start with the default flags.
        style = self.STYLE

        if not self.show_root:
            style = style | wx.TR_HIDE_ROOT | wx.TR_LINES_AT_ROOT

        if self.selection_mode != "single":
            style = style | wx.TR_MULTIPLE | wx.TR_EXTENDED

        return style

    def _add_element(self, pid, element):
        """ Adds 'element' as a child of the element identified by 'pid'.

        If 'pid' is None then we are adding the root element.

        """

        # Get the tree item image index and text.
        image_index = self._get_image_index(element)
        text = self._get_text(element)

        # Add the element.
        if pid is None:
            wxid = self.control.AddRoot(text, image_index, image_index)

        else:
            wxid = self.control.AppendItem(pid, text, image_index, image_index)

        # If we are adding the root element but the root is hidden, get its
        # children.
        if pid is None and not self.show_root:
            children = self.content_provider.get_children(element)
            for child in children:
                self._add_element(wxid, child)

        # Does the element have any children?
        has_children = self.content_provider.has_children(element)
        self.control.SetItemHasChildren(wxid, has_children)

        # The item data is a tuple. The first element indicates whether or not
        # we have already populated the item with its children. The second
        # element is the actual item data.
        if pid is None:
            if self.show_root:
                self.control.SetItemData(wxid, (False, element))

        else:
            self.control.SetItemData(wxid, (False, element))

        # Make sure that we can find the element's Id later.
        self._element_to_id_map[self._get_key(element)] = wxid

        # If we are adding the root item then automatically expand it.
        if pid is None and self.show_root:
            self.control.Expand(wxid)

    def _get_image_index(self, element):
        """ Returns the tree item image index for an element. """

        # Get the image used to represent the element.
        image = self.label_provider.get_image(self, element)
        if image is not None:
            image_index = self._image_list.GetIndex(image.absolute_path)

        else:
            image_index = -1

        return image_index

    def _get_key(self, element):
        """ Generate the key for the element to id map. """

        try:
            key = hash(element)

        except:
            key = id(element)

        return key

    def _get_text(self, element):
        """ Returns the tree item text for an element. """

        text = self.label_provider.get_text(self, element)
        if text is None:
            text = ""

        return text

    def _refresh_element(self, wxid, element):
        """ Refreshes the image and text of the specified element. """

        # Get the tree item image index.
        image_index = self._get_image_index(element)
        self.control.SetItemImage(wxid, image_index, wx.TreeItemIcon_Normal)
        self.control.SetItemImage(wxid, image_index, wx.TreeItemIcon_Selected)

        # Get the tree item text.
        text = self._get_text(element)
        self.control.SetItemText(wxid, text)

        # Does the item have any children?
        has_children = self.content_provider.has_children(element)
        self.control.SetItemHasChildren(wxid, has_children)

    def _unpack_event(self, event):
        """ Unpacks the event to see whether a tree element was involved. """

        try:
            point = event.GetPosition()

        except:
            point = event.GetPoint()

        wxid, flags = self.control.HitTest(point)

        # Warning: On GTK we have to check the flags before we call 'GetItemData'
        # because if we call it when the hit test returns 'nowhere' it will
        # barf (on Windows it simply returns 'None' 8^()
        if flags & wx.TREE_HITTEST_NOWHERE:
            data = None

        else:
            data = self.control.GetItemData(wxid)

        return data, wxid, flags, point

    def _get_selection(self):
        """ Returns a list of the selected elements. """

        elements = []
        for wxid in self.control.GetSelections():
            data = self.control.GetItemData(wxid)
            if data is not None:
                populated, element = data
                elements.append(element)

            # 'data' can be None here if (for example) the element has been
            # deleted.
            #
            # fixme: Can we stop this happening?!?!?
            else:
                pass

        return elements

    def _delete_children(self, pid):
        """ Recursively deletes the children of the specified element. """

        cookie = 0

        (cid, cookie) = self.control.GetFirstChild(pid, cookie)
        while cid.IsOk():
            # Recursively delete the child's children.
            self._delete_children(cid)

            # Remove the reference to the item's data.
            populated, element = self.control.GetItemData(cid)
            del self._element_to_id_map[self._get_key(element)]
            self.control.SetItemData(cid, None)

            # Next!
            (cid, cookie) = self.control.GetNextChild(pid, cookie)

        self.control.DeleteChildren(pid)

        return

    # Trait event handlers -------------------------------------------------

    def _input_changed(self):
        """ Called when the tree's input has been changed. """

        # Delete everything...
        if self.control is not None:
            self.control.DeleteAllItems()

            self._element_to_id_map = {}

            # ... and then add the root item back in.
            if self.input is not None:
                self._add_element(None, self.input)

    def _element_begin_drag_changed(self, element):
        """ Called when a drag is started on a element. """

        # We ask the label provider for the actual value to drag.
        drag_value = self.label_provider.get_drag_value(self, element)

        # Start the drag.
        PythonDropSource(self.control, drag_value)

        return

    # wx event handlers ----------------------------------------------------

    def _on_right_down(self, event):
        """ Called when the right mouse button is clicked on the tree. """

        data, id, flags, point = self._unpack_event(event)

        # Did the right click occur on a tree item?
        if data is not None:
            populated, element = data

            # Trait notification.
            self.element_right_clicked = (element, point)

        # Give other event handlers a chance.
        event.Skip()

    def _on_left_down(self, event):
        """ Called when the left mouse button is clicked on the tree. """

        data, wxid, flags, point = self._unpack_event(event)

        # Save point for tree_begin_drag method to workaround a bug in ?? when
        # wx.TreeEvent.GetPoint returns only (0,0).  This happens under linux
        # when using wx-2.4.2.4, for instance.
        self._point_left_clicked = point

        # Did the left click occur on a tree item?
        if data is not None:
            populated, element = data

            # Trait notification.
            self.element_left_clicked = (element, point)

        # Give other event handlers a chance.
        event.Skip()

    def _on_tree_item_expanding(self, event):
        """ Called when a tree item is about to expand. """

        # Which item is expanding?
        wxid = event.GetItem()

        # The item data is a tuple. The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, element = self.control.GetItemData(wxid)

        # Give the label provider a chance to veto the expansion.
        if self.label_provider.is_expandable(self, element):
            # Lazily populate the item's children.
            if not populated:
                children = self.content_provider.get_children(element)

                # Sorting...
                if self.sorter is not None:
                    self.sorter.sort(self, element, children)

                # Filtering....
                for child in children:
                    for filter in self.filters:
                        if not filter.select(self, element, child):
                            break

                    else:
                        self._add_element(wxid, child)

                # The element is now populated!
                self.control.SetItemData(wxid, (True, element))

        else:
            event.Veto()

    def _on_tree_item_expanded(self, event):
        """ Called when a tree item has been expanded. """

        # Which item was expanded?
        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, element = self.control.GetItemData(wxid)

        # Make sure that the element's 'open' icon is displayed etc.
        self._refresh_element(wxid, element)

        # Trait notification.
        self.element_expanded = element

    def _on_tree_item_collapsing(self, event):
        """ Called when a tree item is about to collapse. """

        # Which item is collapsing?
        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, element = self.control.GetItemData(wxid)

        # Give the label provider a chance to veto the collapse.
        if not self.label_provider.is_collapsible(self, element):
            event.Veto()

    def _on_tree_item_collapsed(self, event):
        """ Called when a tree item has been collapsed. """

        # Which item was collapsed?
        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, element = self.control.GetItemData(wxid)

        # Make sure that the element's 'closed' icon is displayed etc.
        self._refresh_element(wxid, element)

        # Trait notification.
        self.element_collapsed = element

    def _on_tree_item_activated(self, event):
        """ Called when a tree item is activated (i.e., double clicked). """

        # Which item was activated?
        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, element = self.control.GetItemData(wxid)

        # Trait notification.
        self.element_activated = element

    def _on_tree_sel_changed(self, event):
        """ Called when the selection is changed. """

        # Trait notification.
        self.selection = self._get_selection()

    def _on_tree_begin_drag(self, event):
        """ Called when a drag operation is starting on a tree item. """

        # Get the element, its id and the point where the event occurred.
        data, wxid, flags, point = self._unpack_event(event)

        if point == (0, 0):
            # Apply workaround.
            point = self._point_left_clicked
            wxid, flags = self.control.HitTest(point)
            data = self.control.GetItemData(wxid)

        if data is not None:
            populated, element = data

            # Trait notification.
            self.element_begin_drag = element

    def _on_tree_begin_label_edit(self, event):
        """ Called when the user has started editing an item's label. """

        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children.  The second
        # element is the actual item data.
        populated, element = self.control.GetItemData(wxid)

        # Give the label provider a chance to veto the edit.
        if not self.label_provider.is_editable(self, element):
            event.Veto()

    def _on_tree_end_label_edit(self, event):
        """ Called when the user has finished editing an item's label. """

        wxid = event.GetItem()

        # The item data is a tuple.  The first element indicates whether or not
        # we have already populated the item with its children. The second
        # element is the actual item data.
        populated, element = self.control.GetItemData(wxid)

        # Give the label provider a chance to veto the edit.
        label = event.GetLabel()
        if not self.label_provider.set_text(self, element, label):
            event.Veto()

    def _on_char(self, event):
        """ Called when a key is pressed when the tree has focus. """

        # Trait notification.
        self.key_pressed = event.GetKeyCode()

        return
