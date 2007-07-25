""" An action that toggles a view's visibility (ie. hides/shows it). """


# Enthought library imports.
from enthought.pyface.workbench.api import IView
from enthought.traits.api import Delegate, Instance, on_trait_change

# Local imports.
from workbench_action import WorkbenchAction


class ToggleViewVisibilityAction(WorkbenchAction):
    """ An action that toggles a view's visibility (ie. hides/shows it). """

    #### 'Action' interface ###################################################

    # The action's unique identifier (may be None).
    id = Delegate('view')

    # The action's name (displayed on menus/tool bar tools etc).
    name = Delegate('view')
    
    # The action's style.
    style = 'toggle'

    #### 'ViewAction' interface ###############################################

    # The view that we toggle the visibility for.
    view = Instance(IView)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(ToggleViewVisibilityAction, self).__init__(**traits)

        # Make sure that the action is checked if its view is already visible.
        self._refresh_checked()

        return

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        # fixme: In a world of commands this could be:-
        #
        # command = ToggleViewVisibilityCommand(window=window, view=view)
        # command.execute()
        self._toggle_view_visibility(self.window, self.view)

        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _toggle_view_visibility(self, window, view):
        """ Toggle the visibility of a view. """
        
        if view.visible:
            window.hide_view(view)

        else:
            window.show_view(view)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    @on_trait_change('view.visible')
    def _refresh_checked(self):
        """ Refresh the checked state of the action. """

        self.checked = self.view.visible

        return
    
#### EOF ######################################################################
