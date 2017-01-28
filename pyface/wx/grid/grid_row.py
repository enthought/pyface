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
""" A description of a row in a grid. """


# Enthought library imports.
from traits.api import HasTraits


class GridRow(HasTraits):
    """ A description of a row in a grid. """

    def __init__(self, row_data):
        """ Create a new row. """

        self.__dict__.update(row_data)

        return

#### EOF ######################################################################
