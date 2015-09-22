""" An action that toggles a view's visibility (ie. hides/shows it). """


# Enthought library imports.
from pyface.workbench.api import IView
from traits.api import Delegate, Instance

# Local imports.
from .workbench_action import WorkbenchAction


class ToggleViewVisibilityAction(WorkbenchAction):
    """ An action that toggles a view's visibility (ie. hides/shows it). """

    #### 'Action' interface ###################################################

    # The action's unique identifier (may be None).
    id = Delegate('view', modify=True)

    # The action's name (displayed on menus/tool bar tools etc).
    name = Delegate('view', modify=True)

    # The action's style.
    style = 'toggle'

    #### 'ViewAction' interface ###############################################

    # The view that we toggle the visibility for.
    view = Instance(IView)

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def destroy(self):
        """ Called when the action is no longer required. """

        if self.view is not None:
            self._remove_view_listeners(self.view)

        return

    def perform(self, event):
        """ Perform the action. """

        self._toggle_view_visibility(self.view)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _view_changed(self, old, new):
        """ Static trait change handler. """

        if old is not None:
            self._remove_view_listeners(old)

        if new is not None:
            self._add_view_listeners(new)

        self._refresh_checked()

        return

    #### Methods ##############################################################

    def _add_view_listeners(self, view):
        """ Add listeners for trait events on a view. """

        view.on_trait_change(self._refresh_checked, 'visible')
        view.on_trait_change(self._refresh_checked, 'window')

        return

    def _remove_view_listeners(self, view):
        """ Add listeners for trait events on a view. """

        view.on_trait_change(self._refresh_checked, 'visible', remove=True)
        view.on_trait_change(self._refresh_checked, 'window', remove=True)

        return

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
