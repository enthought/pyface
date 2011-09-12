# Enthought library imports.
from pyface.action.api import Action, ActionItem, Group
from traits.api import Bool, Instance, List, Property, Unicode, on_trait_change

# Local imports.
from pyface.tasks.i_dock_pane import IDockPane


class DockPaneToggleAction(Action):
    """ An Action for toggling the visibily of a dock pane.
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

    def perform(self, event=None):
        if self.dock_pane:
            self.dock_pane.visible = not self.dock_pane.visible

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_name(self):
        return self.dock_pane.name

    def _get_tooltip(self):
        return u'Toggles the visibilty of the %s pane.' % self.name

    @on_trait_change('dock_pane.visible')
    def _update_checked(self):
        self.checked = self.dock_pane.visible

    @on_trait_change('dock_pane.closable')
    def _update_visible(self):
        self.visible = self.dock_pane.closable


class DockPaneToggleGroup(Group):
    """ A Group for toggling the visibility of a task's dock panes.
    """

    #### 'Group' interface ####################################################

    id = 'DockPaneToggleGroup'

    items = List

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _items_default(self):
        """ Create a DockPaneToggleAction for each dock pane.
        """
        manager = self
        while isinstance(manager, Group):
            manager = manager.parent
        task = manager.controller.task

        items = []
        for dock_pane in task.window.get_dock_panes(task):
            action = DockPaneToggleAction(dock_pane=dock_pane)
            items.append(ActionItem(action=action))
        items.sort(key=lambda item: item.action.name)
        return items
