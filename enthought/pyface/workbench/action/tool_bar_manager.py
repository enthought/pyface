""" The tool bar manager for the Envisage workbench window. """


# Enthought library imports.
from enthought.pyface.action.api import ToolBarManager
from enthought.traits.api import Instance

# Local imports.
from action_controller import ActionController


class ToolBarManager(ToolBarManager):
    """ The tool bar manager for the Envisage workbench window. """

    #### 'ToolBarManager' interface ###########################################

    # The workbench window that we are the tool bar manager for.
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    ###########################################################################
    # 'ToolBarManager' interface.
    ###########################################################################

    def create_tool_bar(self, parent):
        """ Creates a tool bar representation of the manager. """

        # The controller handles the invocation of every action.
        controller = ActionController(window=self.window)

        tool_bar = super(ToolBarManager, self).create_tool_bar(
            parent, controller=controller
        )

        return tool_bar

#### EOF ######################################################################
