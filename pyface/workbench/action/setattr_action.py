""" An action that sets an attribute. """


# Enthought library imports.
from traits.api import Any, Str

# Local imports.
from .workbench_action import WorkbenchAction


class SetattrAction(WorkbenchAction):
    """ An action that sets an attribute. """

    #### 'SetattrAction' interface ############################################

    # The object that we set the attribute on.
    obj = Any

    # The name of the attribute that we set.
    attribute_name = Str

    # The value that we set the attribute to.
    value = Any

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """

        setattr(self.obj, self.attribute_name, self.value)

        return

#### EOF ######################################################################
