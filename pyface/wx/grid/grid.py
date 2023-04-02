# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A grid (spreadsheet) widget. """


import wx
from wx.grid import (
    Grid as wxGrid,
    GridTableMessage,
    GRIDTABLE_NOTIFY_ROWS_APPENDED,
    GRIDTABLE_NOTIFY_ROWS_DELETED,
    GRIDTABLE_NOTIFY_COLS_APPENDED,
    GRIDTABLE_NOTIFY_COLS_DELETED,
)


class Grid(wxGrid):
    """ A grid (spreadsheet) widget. """

    def __init__(self, parent, model):
        """ Constructor. """

        # Base class constructor.
        wxGrid.__init__(self, parent, -1)

        # The model that provides the data and row/column information.
        self.model = None

        # Don't display any extra space around the rows and columns.
        self.SetMargins(0, 0)

        # Tell the grid to get its data from the model.
        #
        # N.B The terminology used in the wxPython API is a little confusing!
        # --- The 'SetTable' method is actually setting the model used by
        #     the grid (which is the view)!
        #
        # The second parameter to 'SetTable' tells the grid to take ownership
        # of the model and to destroy it when it is done.  Otherwise you would
        # need to keep a reference to the model and manually destroy it later
        # (by calling it's Destroy method).
        #
        # fixme: We should create a default model if one is not supplied.
        self.SetTable(model._grid_table_base, True)
        model.observe(self._on_model_changed, "model_changed")

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self._on_cell_change)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self._on_select_cell)

        # This starts the cell editor on a double-click as well as on a second
        # click.
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self._on_cell_left_dclick)

        # This pops up a context menu.
        # wx.grid.EVT_GRID_CELL_RIGHT_CLICK(self, self._on_cell_right_click)

        # We handle key presses to change the behavior of the <Enter> and
        # <Tab> keys to make manual data entry smoother.
        self.Bind(wx.EVT_KEY_DOWN, self._on_key_down)

        # Initialize the row and column models.
        self._initialize_rows(model)
        self._initialize_columns(model)
        self._initialize_fonts()

    def _initialize_fonts(self):
        """ Initialize the label fonts. """

        self.SetLabelFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.SetGridLineColour("blue")
        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

    def _initialize_rows(self, model):
        """ Initialize the row headers. """

        if not model.show_row_headers:
            self.SetRowLabelSize(0)

        else:
            for index, row in enumerate(model.rows):
                if row.readonly:
                    attr = wx.grid.GridCellAttr()
                    attr.SetReadOnly()
                    attr.SetRenderer(None)
                    attr.SetBackgroundColour("linen")
                    self.SetRowAttr(index, attr)

    def _initialize_columns(self, model):
        """ Initialize the column headers. """

        if not model.show_column_headers:
            self.SetColLabelSize(0)

        else:
            for index, column in enumerate(model.columns):
                if column.readonly:
                    attr = wx.grid.GridCellAttr()
                    attr.SetReadOnly()
                    attr.SetRenderer(None)
                    attr.SetBackgroundColour("linen")
                    self.SetColAttr(index, attr)

        return

    # ------------------------------------------------------------------------
    # wx event handlers.
    # ------------------------------------------------------------------------

    def _on_cell_change(self, evt):
        """ Called when the contents of a cell have been changed. """

        evt.Skip()

    def _on_select_cell(self, evt):
        """ Called when the user has moved to another cell. """

        evt.Skip()

    def _on_cell_left_dclick(self, evt):
        """ Called when the left mouse button was double-clicked.

        From the wxPython demo code:-

        'I do this because I don't like the default behaviour of not starting
        the cell editor on double clicks, but only a second click.'

        Fair enuff!

        """

        if self.CanEnableCellControl():
            self.EnableCellEditControl()

    def _on_cell_right_click(self, evt):
        """ Called when a right click occurred in a cell. """

        row = evt.GetRow()

        # The last row in the table is not part of the actual data, it is just
        # there to allow the user to enter a new row. Hence they cannot delete
        # it!
        if row < self.GetNumberRows() - 1:
            # Complete the edit on the current cell.
            self.DisableCellEditControl()

            # Make the row the ONLY one selected.
            self.SelectRow(row)

            # Popup a context menu allowing the user to delete the row.
            menu = wx.Menu()
            menu.Append(101, "Delete Row")
            self.Bind(wx.EVT_MENU, self._on_delete_row, id=101)

            self.PopupMenu(menu, evt.GetPosition())

    def _on_key_down(self, evt):
        """ Called when a key is pressed. """

        # This changes the behaviour of the <Enter> and <Tab> keys to make
        # manual data entry smoother!
        #
        # Don't change the behavior if the <Control> key is pressed as this
        # has meaning to the edit control.
        key_code = evt.GetKeyCode()
        if key_code == wx.WXK_RETURN and not evt.ControlDown():
            self._move_to_next_cell(evt.ShiftDown())

        elif key_code == wx.WXK_TAB and not evt.ControlDown():
            if evt.ShiftDown():
                self._move_to_previous_cell()

            else:
                self._move_to_next_cell()

        else:
            evt.Skip()

    def _on_delete_row(self, evt):
        """ Called when the 'Delete Row' context menu item is selected. """

        # Get the selected row (there must be exactly one at this point!).
        selected_rows = self.GetSelectedRows()
        if len(selected_rows) == 1:
            self.DeleteRows(selected_rows[0], 1)

        return

    # ------------------------------------------------------------------------
    # Trait event handlers.
    # ------------------------------------------------------------------------

    def _on_model_changed(self, event):
        """ Called when the model has changed. """
        message = event.new
        self.BeginBatch()
        self.ProcessTableMessage(message)
        self.EndBatch()

        return

    # ------------------------------------------------------------------------
    # 'Grid' interface.
    # ------------------------------------------------------------------------

    def Reset(self):
        print("Reset")
        # attr = grid.GridCellAttr()
        # renderer = MyRenderer()
        # attr.SetRenderer(renderer)

        # self.SetColSize(0, 50)
        # self.SetColAttr(0, attr)

        self.ForceRefresh()

    def ResetView(self, grid):
        """
        (wxGrid) -> Reset the grid view.   Call this to
        update the grid if rows and columns have been added or deleted
        """
        print("*************************VirtualModel.reset_view")

        grid = self

        grid.BeginBatch()
        for current, new, delmsg, addmsg in [
            (
                self._rows,
                self.GetNumberRows(),
                GRIDTABLE_NOTIFY_ROWS_DELETED,
                GRIDTABLE_NOTIFY_ROWS_APPENDED,
            ),
            (
                self._cols,
                self.GetNumberCols(),
                GRIDTABLE_NOTIFY_COLS_DELETED,
                GRIDTABLE_NOTIFY_COLS_APPENDED,
            ),
        ]:
            if new < current:
                msg = GridTableMessage(self, delmsg, new, current - new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = GridTableMessage(self, addmsg, new - current)
                grid.ProcessTableMessage(msg)
                self.UpdateValues(grid)
        grid.EndBatch()

        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

        # update the renderers
        # self._updateColAttrs(grid)
        # self._updateRowAttrs(grid) too expensive to use on a large grid

        # update the scrollbars and the displayed part of the grid
        grid.AdjustScrollbars()
        grid.ForceRefresh()

        return

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _move_to_next_cell(self, expandSelection=False):
        """ Move to the 'next' cell. """

        # Complete the edit on the current cell.
        self.DisableCellEditControl()

        # Try to move to the next column.
        success = self.MoveCursorRight(expandSelection)

        # If the move failed then we must be at the end of a row.
        if not success:
            # Move to the first column in the next row.
            newRow = self.GetGridCursorRow() + 1
            if newRow < self.GetNumberRows():
                self.SetGridCursor(newRow, 0)
                self.MakeCellVisible(newRow, 0)

            else:
                # This would be a good place to add a new row if your app
                # needs to do that.
                pass

        return success

    def _move_to_previous_cell(self, expandSelection=False):
        """ Move to the 'previous' cell. """

        # Complete the edit on the current cell.
        self.DisableCellEditControl()

        # Try to move to the previous column (without expanding the current
        # selection).
        success = self.MoveCursorLeft(expandSelection)

        # If the move failed then we must be at the start of a row.
        if not success:
            # Move to the last column in the previous row.
            newRow = self.GetGridCursorRow() - 1
            if newRow >= 0:
                self.SetGridCursor(newRow, self.GetNumberCols() - 1)
                self.MakeCellVisible(newRow, self.GetNumberCols() - 1)

        return
