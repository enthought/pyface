""" An action that sets the active perspective. """


# Enthought library imports.
from enthought.pyface.workbench.api import IPerspective
from enthought.traits.api import Delegate, Instance, on_trait_change

# Local imports.
from workbench_action import WorkbenchAction


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
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(SetActivePerspectiveAction, self).__init__(**traits)

        # Make sure that the action is checked its perspective is already the
        # active perspective.
        self._refresh_checked()

        return
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        self.window.active_perspective = self.perspective

        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    @on_trait_change('window.active_perspective')
    def _refresh_checked(self):
        """ Refresh the checked state of the action. """

        self.checked = self.perspective.id is self.window.active_perspective.id

        return

#### EOF ######################################################################
