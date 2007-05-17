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

    #### Trait change handlers ################################################

    @on_trait_change('view.visible')
    def _when_visible_changed_for_view(self, new):
        """ Dynamic trait change handler. """

        self.checked = new

        return
    
#### EOF ######################################################################
