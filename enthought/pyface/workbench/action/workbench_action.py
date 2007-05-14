""" Abstract base class for all workbench actions. """


# Enthought library imports.
from enthought.pyface.workbench.api import WorkbenchWindow
from enthought.pyface.action.api import Action
from enthought.traits.api import Instance


class WorkbenchAction(Action):
    """ Abstract base class for all workbench actions. """

    #### 'WorkbenchAction' interface ##########################################

    # The workbench window that the action is in.
    #
    # This is set by the framework.
    window = Instance(WorkbenchWindow)

#### EOF ######################################################################
