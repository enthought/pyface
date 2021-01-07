# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A panel that is split in two either horizontally or vertically. """


from pyface.split_widget import SplitWidget
from pyface.widget import Widget


class SplitPanel(Widget, SplitWidget):
    """ A panel that is split in two either horizontally or vertically. """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, **traits):
        """ Creates a new panel. """

        # Base class constructor.
        super(SplitPanel, self).__init__(**traits)

        # Create the widget's toolkit-specific control.
        self.control = self._create_splitter(parent)
