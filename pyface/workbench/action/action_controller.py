""" The action controller for workbench menu and tool bars. """


# Enthought library imports.
from pyface.action.api import ActionController
from pyface.workbench.api import WorkbenchWindow
from traits.api import HasTraits, Instance


class ActionController(ActionController):
    """ The action controller for workbench menu and tool bars.

    The controller is used to 'hook' the invocation of every action on the menu
    and tool bars. This is done so that additional (and workbench specific)
    information can be added to action events. Currently, we attach a reference
    to the workbench window.

    """

    #### 'ActionController' interface #########################################

    # The workbench window that this is the controller for.
    window = Instance(WorkbenchWindow)

    ###########################################################################
    # 'ActionController' interface.
    ###########################################################################

    def perform(self, action, event):
        """ Control an action invocation. """

        # Add a reference to the window and the application to the event.
        event.window = self.window

        return action.perform(event)

#### EOF ######################################################################
