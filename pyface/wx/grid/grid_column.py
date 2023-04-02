# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A description of a column in a grid. """


from traits.api import Bool, HasTraits, Str


class GridColumn(HasTraits):
    """ A description of a column in a grid. """

    # Column header.
    label = Str()

    # Type name of data allowed in the column.
    type = Str()

    # Is the column read-only?
    readonly = Bool(False)
