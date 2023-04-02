# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A description of a row in a grid. """


from traits.api import HasTraits


class GridRow(HasTraits):
    """ A description of a row in a grid. """

    def __init__(self, row_data):
        """ Create a new row. """

        self.__dict__.update(row_data)

        return
