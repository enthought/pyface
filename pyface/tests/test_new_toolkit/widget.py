# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# Dummy widget module for testing entrypoints

from traits.api import Any, Bool, provides
from pyface.i_widget import IWidget, MWidget


@provides(IWidget)
class Widget(MWidget):

    # 'IWidget' interfaces -------------------------------------------------#

    control = Any()

    parent = Any()

    #: Whether or not the control is visible
    visible = Bool(True)

    #: Whether or not the control is enabled
    enabled = Bool(True)

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def show(self, visible):
        """ Show or hide the widget.

        Parameter
        ---------
        visible : bool
            Visible should be ``True`` if the widget should be shown.
        """

    def enable(self, enabled):
        """ Enable or disable the widget.

        Parameter
        ---------
        enabled : bool
            The enabled state to set the widget to.
        """

    def destroy(self):
        self.control = None

