""" A Group for toggling the visibility of a task's dock panes. """


# Enthought library imports.
from pyface.action.api import Action, ActionItem, Group
from traits.api import cached_property, Instance, List, on_trait_change, \
    Property, Unicode

# Local imports.
from pyface.tasks.i_dock_pane import IDockPane


class DockPaneToggleAction(Action):
    """ An Action for toggling the visibility of a dock pane.
    """

    #### 'DockPaneToggleAction' interface #####################################

    dock_pane = Instance(IDockPane)

    #### 'Action' interface ###################################################

    name = Property(Unicode, depends_on='dock_pane.name')
    style = 'toggle'
    tooltip = Property(Unicode, depends_on='name')

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def destroy(self):
        super(DockPaneToggleAction, self).destroy()

        # Make sure that we are not listening to changes to the pane anymore.
        # In traits style, we will set the basic object to None and have the
        # listener check that if it is still there.
        self.dock_pane = None

    def perform(self, event=None):
        if self.dock_pane:
            self.dock_pane.visible = not self.dock_pane.visible

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_name(self):
        if self.dock_pane is None:
            return 'UNDEFINED'
        return self.dock_pane.name

    def _get_tooltip(self):
        return u'Toggles the visibility of the %s pane.' % self.name

    @on_trait_change('dock_pane.visible')
    def _update_checked(self):
        if self.dock_pane:
            self.checked = self.dock_pane.visible

    @on_trait_change('dock_pane.closable')
    def _update_visible(self):
        if self.dock_pane:
            self.visible = self.dock_pane.closable

class DockPaneToggleGroup(Group):
    """ A Group for toggling the visibility of a task's dock panes.
    """

    #### 'Group' interface ####################################################

    id = 'DockPaneToggleGroup'

    items = List

    #### 'DockPaneToggleGroup' interface ######################################

    task = Property(depends_on='parent.controller')

    @cached_property
    def _get_task(self):
        manager = self.get_manager()

        if manager is None or manager.controller is None:
            return None

        return manager.controller.task

    dock_panes = Property(depends_on='task.window._states.dock_panes')

    @cached_property
    def _get_dock_panes(self):
        if self.task is None or self.task.window is None:
            return []

        task_state = self.task.window._get_state(self.task)
        return task_state.dock_panes

    def get_manager(self):
        # FIXME: Is there no better way to get a reference to the menu manager?
        manager = self
        while isinstance(manager, Group):
            manager = manager.parent
        return manager

    #### Private interface ####################################################

    @on_trait_change('dock_panes[]')
    def _dock_panes_updated(self):
        """Recreate the group items when dock panes have been added/removed.
        """

        # Remove the previous group items.
        self.destroy()

        items = []
        for dock_pane in self.dock_panes:
            action = DockPaneToggleAction(dock_pane=dock_pane)
            items.append(ActionItem(action=action))

        items.sort(key=lambda item: item.action.name)
        self.items = items

        # Inform the parent menu manager.
        manager = self.get_manager()
        manager.changed = True
