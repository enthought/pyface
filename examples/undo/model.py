# -----------------------------------------------------------------------------
# Copyright (c) 2008, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited
# Description: <Enthought undo package component>
# -----------------------------------------------------------------------------


# Enthought library imports.
from traits.api import Enum, HasTraits, Int, Str


class Label(HasTraits):
    """The Label class implements the data model for a label."""

    #### 'Label' interface ####################################################

    # The name.
    name = Str

    # The size in points.
    size = Int(18)

    # The style.
    style = Enum('normal', 'bold', 'italic')

    ###########################################################################
    # 'Label' interface.
    ###########################################################################

    def increment_size(self, by):
        """Increment the current font size."""

        self.size += by

    def decrement_size(self, by):
        """Decrement the current font size."""

        self.size -= by
