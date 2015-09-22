""" The tool bar manager for the Envisage workbench window. """


# Enthought library imports.
import pyface.action.api as pyface
from traits.api import Instance

# Local imports.
from .action_controller import ActionController


class ToolBarManager(pyface.ToolBarManager):
    """ The tool bar manager for the Envisage workbench window. """

    #### 'ToolBarManager' interface ###########################################

    # The workbench window that we are the tool bar manager for.
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    ###########################################################################
    # 'ToolBarManager' interface.
    ###########################################################################

    def create_tool_bar(self, parent, controller=None):
        """ Creates a tool bar representation of the manager. """

        # The controller handles the invocation of every action.
        if controller is None:
            controller = ActionController(window=self.window)

        tool_bar = super(ToolBarManager, self).create_tool_bar(
            parent, controller=controller
        )

        return tool_bar

#### EOF ######################################################################
