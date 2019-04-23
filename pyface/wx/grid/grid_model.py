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
""" A model that provides data for a grid. """

# Major package imports.
from __future__ import print_function
import wx
from wx.grid import PyGridTableBase, GridTableMessage, GRIDTABLE_NOTIFY_ROWS_APPENDED

# Enthought library imports.
from traits.api import Any, Bool, HasTraits, Trait, Event, List

# Local imports.
from .grid_column import GridColumn
from .grid_row import GridRow


class GridModel(HasTraits):
    """ A model that provides data for a grid. """

    # fixme : factor this default model into "SimpleGridModel" or similar
    # An optional 2-dimensional list/array containing the grid data.
    data = Any

    # The rows in the model.
    rows = List(GridRow)

    # The columns in the model.
    columns = List(GridColumn)

    # Show row headers?
    show_row_headers = Bool(True)

    # Show column headers?
    show_column_headers = Bool(True)

    # Fired when the data in the model has changed.
    model_changed = Event


    def __init__(self, **traits):
        """ Create a new grid model. """

        # Base class constructors.
        HasTraits.__init__(self, **traits)

        # The wx virtual table hook.
        self._grid_table_base = _GridTableBase(self)

        if len(self.columns) == 0 and self.data is not None:
            print("Building default table column model")
            columns = []
            # Assume data is rectangular and use the length of the first row.
            for i in range(len(self.data[0])):
                columns.append(GridColumn(label=str(i)))
            self.columns = columns

        return

    ###########################################################################
    # 'wxPyGridTableBase' interface.
    ###########################################################################

    def GetNumberRows(self):
        """ Return the number of rows in the model. """

        return len(self.data)

    def GetNumberCols(self):
        """ Return the number of columns in the model. """

        return len(self.columns)

    def IsEmptyCell(self, row, col):
        """ Is the specified cell empty? """

        try:
            return not self.data[row][col]

        except IndexError:
            return True

    # Get/Set values in the table. The Python versions of these methods can
    # handle any data-type, (as long as the Editor and Renderer understands the
    # type too,) not just strings as in the C++ version.
    def GetValue(self, row, col):
        """ Get the value at the specified row and column. """

        try:
            return self.data[row][col]

        except IndexError:
            pass

        return ''

    def SetValue(self, row, col, value):
        """ Set the value at the specified row and column. """

        label = self.GetColLabelValue(col)

        try:
            self.data[row][col] = value

        except IndexError:
            # Add a new row.
            self.data.append([0] * self.GetNumberCols())
            self.data[row][col] = value

            # Tell the grid that we've added a row.
            #
            # N.B wxGridTableMessage(table, whatWeDid, howMany)
            message = GridTableMessage(
                self, GRIDTABLE_NOTIFY_ROWS_APPENDED, 1
            )

            # Trait event notification.
            self.model_changed = message

        return

    def GetRowLabelValue(self, row):
        """ Called when the grid needs to display a row label. """

        return str(row)

    def GetColLabelValue(self, col):
        """ Called when the grid needs to display a column label. """

        return self.columns[col].label

    def GetTypeName(self, row, col):
        """ Called to determine the kind of editor/renderer to use.

        This doesn't necessarily have to be the same type used natively by the
        editor/renderer if they know how to convert.

        """

        return self.columns[col].type

    def CanGetValueAs(self, row, col, type_name):
        """ Called to determine how the data can be fetched.

        This allows you to enforce some type-safety in the grid.

        """

        column_typename = self.GetTypeName(row, col)

        return type_name == column_typename

    def CanSetValueAs(self, row, col, type_name):
        """ Called to determine how the data can be stored.

        This allows you to enforce some type-safety in the grid.

        """

        return self.CanGetValueAs(row, col, type_name)

    def DeleteRows(self, pos, num_rows):
        """ Called when the view is deleting rows. """

        del self.data[pos:pos + num_rows]

        # Tell the grid that we've deleted some rows.
        #
        # N.B Because of a bug in wxPython we have to send a "rows appended"
        # --- message with a negative number, instead of the "rows deleted"
        #     message 8^() TINSTAFS!
        message = GridTableMessage(
            self, GRIDTABLE_NOTIFY_ROWS_APPENDED, -num_rows
        )

        # Trait event notification.
        self.model_changed = message

        return True


class _GridTableBase(PyGridTableBase):
    """ A model that provides data for a grid. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, model):
        """ Creates a new table base. """

        # Base class constructor.
        PyGridTableBase.__init__(self)

        # The Pyface model that provides the data.
        self.model = model

        return

    ###########################################################################
    # 'wxPyGridTableBase' interface.
    ###########################################################################

    def GetNumberRows(self):
        """ Return the number of rows in the model. """

        return self.model.GetNumberRows()

    def GetNumberCols(self):
        """ Return the number of columns in the model. """

        return self.model.GetNumberCols()

    def IsEmptyCell(self, row, col):
        """ Is the specified cell empty? """

        return self.model.IsEmptyCell(row, col)

    def GetValue(self, row, col):
        """ Get the value at the specified row and column. """

        return self.model.GetValue(row, col)

    def SetValue(self, row, col, value):
        """ Set the value at the specified row and column. """

        return self.model.SetValue(row, col, value)

    def GetRowLabelValue(self, row):
        """ Called when the grid needs to display a row label. """

        return self.model.GetRowLabelValue(row)

    def GetColLabelValue(self, col):
        """ Called when the grid needs to display a column label. """

        return self.model.GetColLabelValue(col)

    def GetTypeName(self, row, col):
        """ Called to determine the kind of editor/renderer to use.

        This doesn't necessarily have to be the same type used natively by the
        editor/renderer if they know how to convert.

        """

        return self.model.GetTypeName(row, col)

    def CanGetValueAs(self, row, col, type_name):
        """ Called to determine how the data can be fetched.

        This allows you to enforce some type-safety in the grid.

        """

        return self.model.CanGetValueAs(row, col, type_name)

    def CanSetValueAs(self, row, col, type_name):
        """ Called to determine how the data can be stored.

        This allows you to enforce some type-safety in the grid.

        """

        return self.model.CanSetValueAs(row, col, type_name)

    def DeleteRows(self, pos, num_rows):
        """ Called when the view is deleting rows. """

        return self.model.DeleteRows(pos, num_rows)

#### EOF ######################################################################
