# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import wx
from wx.grid import Grid
from wx.grid import GridCellFloatRenderer, GridCellFloatEditor


class AbstractGridView(Grid):
    """ Enthought's default spreadsheet view.

    Uses a virtual data source.

    THIS CLASS IS NOT LIMITED TO ONLY DISPLAYING LOG DATA!
    """

    def __init__(self, parent, ID=-1, **kw):

        Grid.__init__(self, parent, ID, **kw)

        # We have things set up to edit on a single click - so we have to select
        # an initial cursor location that is off of the screen otherwise a cell
        # will be in edit mode as soon as the grid fires up.
        self.moveTo = [1000, 1]
        self.edit = False

        # this seems like a busy idle ...
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        # Enthought specific display controls ...
        self.init_labels()
        self.init_data_types()
        self.init_handlers()

        self.Bind(wx.grid.EVT_GRID_EDITOR_CREATED, self._on_editor_created)

    def init_labels(self):
        self.SetLabelFont(
            wx.Font(
                self.GetFont().GetPointSize(), wx.SWISS, wx.NORMAL, wx.BOLD
            )
        )
        self.SetGridLineColour("blue")
        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

    def init_data_types(self):
        """ If the model says a cell is of a specified type, the grid uses
        the specific renderer and editor set in this method.
        """
        self.RegisterDataType(
            "LogData",
            GridCellFloatRenderer(precision=3),
            GridCellFloatEditor(),
        )

    def init_handlers(self):

        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)

        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)

        self.Bind(wx.grid.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(wx.grid.EVT_GRID_COL_SIZE, self.OnColSize)

        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnSelectCell)

        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        self.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        self.Bind(wx.grid.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)

    def SetColLabelsVisible(self, show=True):
        """ This only works if you 'hide' then 'show' the labels.
        """
        if not show:
            self._default_col_label_size = self.GetColLabelSize()
            self.SetColLabelSize(0)
        else:
            self.SetColLabelSize(self._default_col_label_size)

    def SetRowLabelsVisible(self, show=True):
        """ This only works if you 'hide' then 'show' the labels.
        """
        if not show:
            self._default_row_label_size = self.GetRowLabelSize()
            self.SetRowLabelSize(0)
        else:
            self.SetRowLabelSize(self._default_row_label_size)

    def SetTable(self, table, *args):
        """ Some versions of wxPython do not return the correct
        table - hence we store our own copy here - weak ref?
        todo - does this apply to Enthought?
        """
        self._table = table
        return Grid.SetTable(self, table, *args)

    def GetTable(self):
        # Terminate editing of the current cell to force an update of the table
        self.DisableCellEditControl()
        return self._table

    def Reset(self):
        """ Resets the view based on the data in the table.

        Call this when rows are added or destroyed.
        """
        self._table.ResetView(self)

    def OnCellLeftClick(self, evt):
        evt.Skip()

    def OnCellRightClick(self, evt):
        # print self.GetDefaultRendererForCell(evt.GetRow(), evt.GetCol())
        evt.Skip()

    def OnCellLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
        evt.Skip()

    def OnCellRightDClick(self, evt):
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        evt.Skip()

    def OnLabelRightClick(self, evt):
        evt.Skip()

    def OnLabelLeftDClick(self, evt):
        evt.Skip()

    def OnLabelRightDClick(self, evt):
        evt.Skip()

    def OnRowSize(self, evt):
        evt.Skip()

    def OnColSize(self, evt):
        evt.Skip()

    def OnRangeSelect(self, evt):
        # if evt.Selecting():
        #    print "OnRangeSelect: top-left %s, bottom-right %s\n" % (evt.GetTopLeftCoords(), evt.GetBottomRightCoords())
        evt.Skip()

    def OnCellChange(self, evt):
        evt.Skip()

    def OnIdle(self, evt):
        """ Immediately jumps into editing mode, bypassing the usual select mode
        of a spreadsheet. See also self.OnSelectCell().
        """

        if self.edit:
            if self.CanEnableCellControl():
                self.EnableCellEditControl()
            self.edit = False

        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()

    def OnSelectCell(self, evt):

        """ Immediately jumps into editing mode, bypassing the usual select mode
        of a spreadsheet. See also self.OnIdle().
        """
        self.edit = True
        evt.Skip()

    def OnEditorShown(self, evt):
        evt.Skip()

    def OnEditorHidden(self, evt):
        evt.Skip()

    def OnEditorCreated(self, evt):
        evt.Skip()
