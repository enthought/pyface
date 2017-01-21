#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" A viewer for tabular data. """


# Major package imports.
import wx

# Enthought library imports.
from traits.api import Color, Event, Instance, Trait

# Local imports.
from pyface.ui.wx.image_list import ImageList
from pyface.viewer.content_viewer import ContentViewer
from pyface.viewer.table_column_provider import TableColumnProvider
from pyface.viewer.table_content_provider import TableContentProvider
from pyface.viewer.table_label_provider import TableLabelProvider


class TableViewer(ContentViewer):
    """ A viewer for tabular data. """

    # The content provider provides the actual table data.
    content_provider = Instance(TableContentProvider)

    # The label provider provides, err, the labels for the items in the table
    # (a label can have text and/or an image).
    label_provider = Instance(TableLabelProvider, factory = TableLabelProvider)

    # The column provider provides information about the columns in the table
    # (column headers, width etc).
    column_provider=Trait(TableColumnProvider(),Instance(TableColumnProvider))

    # The colours used to render odd and even numbered rows.
    even_row_background = Color("white")
    odd_row_background  = Color((245, 245, 255))

    # A row has been selected.
    row_selected = Event

    # A row has been activated.
    row_activated = Event

    # A drag operation was started on a node.
    row_begin_drag = Event


    def __init__(self, parent, image_size=(16, 16), **traits):
        """ Creates a new table viewer.

        'parent' is the toolkit-specific control that is the table's parent.

        'image_size' is a tuple in the form (int width, int height) that
        specifies the size of the images (if any) displayed in the table.

        """

        # Base-class constructor.
        super(TableViewer, self).__init__(**traits)

        # Create the toolkit-specific control.
        self.control = table = _Table(parent, image_size, self)

        # Get our actual id.
        wxid = table.GetId()

        # Table events.
        wx.EVT_LIST_ITEM_SELECTED(table, wxid, self._on_item_selected)
        wx.EVT_LIST_ITEM_ACTIVATED(table, wxid, self._on_item_activated)
        wx.EVT_LIST_BEGIN_DRAG(table, wxid, self._on_list_begin_drag)
        wx.EVT_LIST_BEGIN_RDRAG(table, wxid, self._on_list_begin_rdrag)

        wx.EVT_LIST_BEGIN_LABEL_EDIT(
            table, wxid, self._on_list_begin_label_edit
        )

        wx.EVT_LIST_END_LABEL_EDIT(
            table, wxid, self._on_list_end_label_edit
        )

        # fixme: Bug[732104] indicates that this event does not get fired
        # in a virtual list control (it *does* get fired in a regular list
        # control 8^().
        wx.EVT_LIST_ITEM_DESELECTED(table, wxid, self._on_item_deselected)

        # Create the widget!
        self._create_widget(parent)

        # We use a dynamic handler instead of a static handler here, as we
        # don't want to react if the input is set in the constructor.
        self.on_trait_change(self._on_input_changed, 'input')

        return

    ###########################################################################
    # 'TableViewer' interface.
    ###########################################################################

    def select_row(self, row):
        """ Select the specified row. """

        self.control.SetItemState(
            row, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED
        )

        self.control.SetItemState(
            row, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED
        )

        # Make sure that the selected row is visible.
        fudge = max(0, row - 5)
        self.EnsureVisible(fudge)

        # Trait event notification.
        self.row_selected = row

        return

    ###########################################################################
    # Trait event handlers.
    ###########################################################################

    def _on_input_changed(self, obj, trait_name, old, new):
        """ Called when the input is changed. """

        # Update the table contents.
        self._update_contents()

        if old is None:
            self._update_column_widths()

        return

    ###########################################################################
    # wx event handlers.
    ###########################################################################

    def _on_item_selected(self, event):
        """ Called when an item in the list is selected. """

        # Get the index of the row that was selected (nice wx interface huh?!).
        row = event.m_itemIndex

        # Trait event notification.
        self.row_selected = row

        return

    # fixme: Bug[732104] indicates that this event does not get fired in a
    # virtual list control (it *does* get fired in a regular list control 8^().
    def _on_item_deselected(self, event):
        """ Called when an item in the list is selected. """

        # Trait event notification.
        self.row_selected = -1

        return

    def _on_item_activated(self, event):
        """ Called when an item in the list is activated. """

        # Get the index of the row that was activated (nice wx interface!).
        row = event.m_itemIndex

        # Trait event notification.
        self.row_activated = row

        return

    def _on_list_begin_drag(self, event=None, is_rdrag=False):
        """ Called when a drag operation is starting on a list item. """

        # Trait notification.
        self.row_begin_drag = event.GetIndex()

        return

    def _on_list_begin_rdrag(self, event=None):
        """ Called when a drag operation is starting on a list item. """

        self._on_list_begin_drag(event, True)

        return

    def _on_list_begin_label_edit(self, event=None):
        """ Called when a label edit is started. """

        event.Veto()

        return

    def _on_list_end_label_edit(self, event=None):
        """ Called when a label edit is completed. """

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    FORMAT_MAP = {
        'left'   : wx.LIST_FORMAT_LEFT,
        'right'  : wx.LIST_FORMAT_RIGHT,
        'center' : wx.LIST_FORMAT_CENTRE,
        'centre' : wx.LIST_FORMAT_CENTRE
    }

    def _create_widget(self, parent):
        """ Creates the widget. """

        # Set up a default list item descriptor.
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT

        # Set the column headers.
        for index in range(self.column_provider.column_count):
            # Header text.
            info.m_text = self.column_provider.get_label(self, index)

            # Alignment of header text AND ALL cells in the column.
            alignment = self.column_provider.get_alignment(self, index)
            info.m_format = self.FORMAT_MAP.get(alignment, wx.LIST_FORMAT_LEFT)

            self.control.InsertColumnInfo(index, info)

        # Update the table contents and the column widths.
        self._update_contents()
        self._update_column_widths()

        return

    def _update_contents(self):
        """ Updates the table content. """

        self._elements = []
        if self.input is not None:
            # Filtering...
            for element in  self.content_provider.get_elements(self.input):
                for filter in self.filters:
                    if not filter.select(self, self.input, element):
                        break

                else:
                    self._elements.append(element)

            # Sorting...
            if self.sorter is not None:
                self.sorter.sort(self, self.input, self._elements)

        # Setting this causes a refresh!
        self.control.SetItemCount(len(self._elements))

        return

    def _update_column_widths(self):
        """ Updates the column widths. """

        # Set all columns to be the size of their largest item, or the size of
        # their header whichever is the larger.
        for column in range(self.control.GetColumnCount()):
            width = self.column_provider.get_width(self, column)
            if width == -1:
                width = self._get_column_width(column)

            self.control.SetColumnWidth(column, width)

        return

    def _get_column_width(self, column):
        """ Return an appropriate width for the specified column. """

        self.control.SetColumnWidth(column, wx.LIST_AUTOSIZE_USEHEADER)
        header_width = self.control.GetColumnWidth(column)

        if self.control.GetItemCount() == 0:
            width = header_width

        else:
            self.control.SetColumnWidth(column, wx.LIST_AUTOSIZE)
            data_width = self.control.GetColumnWidth(column)

            width = max(header_width, data_width)

        return width


class _Table(wx.ListCtrl):
    """ The wx control that we use to implement the table viewer. """

    # Default style.
    STYLE = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.STATIC_BORDER \
            | wx.LC_SINGLE_SEL | wx.LC_VIRTUAL | wx.LC_EDIT_LABELS \
            | wx.CLIP_CHILDREN

    def __init__(self, parent, image_size, viewer):
        """ Creates a new table viewer.

        'parent' is the toolkit-specific control that is the table's parent.

        'image_size' is a tuple in the form (int width, int height) that
        specifies the size of the icons (if any) displayed in the table.

        """

        # The vierer that we are providing the control for.
        self._viewer = viewer

        # Base-class constructor.
        wx.ListCtrl.__init__(self, parent, -1, style=self.STYLE)

        # Table item images.
        self._image_list = ImageList(image_size[0], image_size[1])
        self.AssignImageList(self._image_list, wx.IMAGE_LIST_SMALL)

        # Set up attributes to show alternate rows with a different background
        # colour.
        self._even_row_attribute = wx.ListItemAttr()
        self._even_row_attribute.SetBackgroundColour(
            self._viewer.even_row_background
        )

        self._odd_row_attribute = wx.ListItemAttr()
        self._odd_row_attribute.SetBackgroundColour(
            self._viewer.odd_row_background
        )

        return

    ###########################################################################
    # Virtual 'ListCtrl' interface.
    ###########################################################################

    def OnGetItemText(self, row, column_index):
        """ Returns the text for the specified CELL. """

        viewer = self._viewer
        element = viewer._elements[row]

        return viewer.label_provider.get_text(viewer, element, column_index)

    def OnGetItemImage(self, row):
        """ Returns the image for the specified ROW. """

        viewer = self._viewer
        element = viewer._elements[row]

        # Get the icon used to represent the node.
        image = viewer.label_provider.get_image(viewer, element)
        if image is not None:
            image_index = self._image_list.GetIndex(image.absolute_path)

        else:
            image_index = -1

        return image_index

    def OnGetItemAttr(self, row):
        """ Returns the attribute for the specified row. """

        if row % 2 == 0:
            attribute = self._even_row_attribute

        else:
            attribute = self._odd_row_attribute

        return attribute

#### EOF ######################################################################
