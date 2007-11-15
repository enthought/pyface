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

        self._toggle_view_visibility(self.view)

        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    @on_trait_change('view.visible,view.window')
    def _refresh_checked(self):
        """ Refresh the checked state of the action. """

        self.checked = self.view is not None \
          and self.view.window is not None \
          and self.view.visible

        return
    
    def _toggle_view_visibility(self, view):
        """ Toggle the visibility of a view. """
        
        if view.visible:
            view.hide()
            
        else:
            view.show()
            
        return

#### EOF ######################################################################
