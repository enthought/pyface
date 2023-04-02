# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Base class for all column providers. """


from traits.api import HasTraits, Int


class ColumnProvider(HasTraits):
    """ Base class for all column providers.

    By default a column's label is 'Column n' and is 100 pixels wide.

    """

    # The number of columns.
    column_count = Int()

    # ------------------------------------------------------------------------
    # 'TableColumnProvider' interface.
    # ------------------------------------------------------------------------

    def get_label(self, viewer, column_index):
        """ Returns the label for a column. """

        return "Column %d" % column_index

    def get_width(self, viewer, column_index):
        """ Returns the width of a column.

        Returning -1 (the default) means that the column will be sized to
        fit its longest item (or its column header if it is longer than any
        item).

        """

        return -1

    def get_alignment(self, viewer, column_index):
        """ Returns the alignment of the column header and cells.

        Returns, 'left', 'right', 'centre' or 'center' ('left' by default).

        """

        return "left"
