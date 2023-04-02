# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The tool bar manager for the Envisage workbench window. """


import pyface.action.api as pyface
from traits.api import Instance


from .action_controller import ActionController


class ToolBarManager(pyface.ToolBarManager):
    """ The tool bar manager for the Envisage workbench window. """

    # 'ToolBarManager' interface -------------------------------------------

    # The workbench window that we are the tool bar manager for.
    window = Instance("pyface.workbench.api.WorkbenchWindow")

    # ------------------------------------------------------------------------
    # 'ToolBarManager' interface.
    # ------------------------------------------------------------------------

    def create_tool_bar(self, parent, controller=None, **kwargs):
        """ Creates a tool bar representation of the manager. """

        # The controller handles the invocation of every action.
        if controller is None:
            controller = ActionController(window=self.window)

        tool_bar = super().create_tool_bar(
            parent, controller=controller, **kwargs
        )

        return tool_bar
