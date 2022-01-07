# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A panel that is split in two either horizontally or vertically. """

import warnings

from pyface.split_widget import SplitWidget
from pyface.widget import Widget


class SplitPanel(Widget, SplitWidget):
    """ A panel that is split in two either horizontally or vertically. """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent=None, **traits):
        """ Creates a new panel. """

        create = traits.pop("create", True)

        # Base class constructor.
        super().__init__(parent=parent, **traits)

        if create:
            # Create the widget's toolkit-specific control.
            self.create()
            warnings.warn(
                "automatic widget creation is deprecated and will be removed "
                "in a future Pyface version, use create=False and explicitly "
                "call create() for future behaviour",
                PendingDeprecationWarning,
            )

    def _create_control(self, parent):
        """ Create the toolkit control """
        return self._create_splitter(parent)
