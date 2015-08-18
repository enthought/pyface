""" An action that sets the active perspective. """


# Enthought library imports.
from pyface.workbench.api import IPerspective
from traits.api import Delegate, Instance, on_trait_change

# Local imports.
from .workbench_action import WorkbenchAction


class SetActivePerspectiveAction(WorkbenchAction):
    """ An action that sets the active perspective. """

    #### 'Action' interface ###################################################

    # Is the action enabled?
    enabled = Delegate('perspective')

    # The action's unique identifier (may be None).
    id = Delegate('perspective')

    # The action's name (displayed on menus/tool bar tools etc).
    name = Delegate('perspective')

    # The action's style.
    style = 'radio'

    #### 'SetActivePerspectiveAction' interface ###############################

    # The perspective that we set the active perspective to.
    perspective = Instance(IPerspective)

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def destroy(self):
        """ Destroy the action. """

        self.window = None

        return

    def perform(self, event):
        """ Perform the action. """

        self.window.active_perspective = self.perspective

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    @on_trait_change('perspective,window.active_perspective')
    def _refresh_checked(self):
        """ Refresh the checked state of the action. """

        self.checked = self.perspective is not None \
          and self.window is not None \
          and self.window.active_perspective is not None \
          and self.perspective.id is self.window.active_perspective.id

        return

#### EOF ######################################################################
