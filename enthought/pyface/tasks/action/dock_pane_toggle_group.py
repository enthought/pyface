# Enthought library imports.
from enthought.pyface.action.api import ActionItem, Group
from enthought.traits.api import List

# Local imports.
from dock_pane_toggle_action import DockPaneToggleAction


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
        return items
