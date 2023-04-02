# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.tasks.i_task_pane import ITaskPane, MTaskPane
from traits.api import provides


import wx

# Logging
import logging

logger = logging.getLogger(__name__)


@provides(ITaskPane)
class TaskPane(MTaskPane):
    """ The toolkit-specific implementation of a TaskPane.

    See the ITaskPane interface for API documentation.
    """

    # ------------------------------------------------------------------------
    # 'ITaskPane' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        self.control = wx.Panel(parent)

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        if self.control is not None:
            logger.debug("Destroying %s" % self.control)
            self.task.window._aui_manager.DetachPane(self.control)

            self.control.Hide()
            self.control.Destroy()
            self.control = None

    def set_focus(self):
        """ Gives focus to the control that represents the pane.
        """
        if self.control is not None:
            self.control.SetFocus()
