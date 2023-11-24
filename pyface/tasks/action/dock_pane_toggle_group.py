# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A Group for toggling the visibility of a task's dock panes. """


from traits.api import (
    cached_property,
    Instance,
    List,
    observe,
    Property,
    Str,
)


from pyface.action.api import Action, Group
from pyface.tasks.i_dock_pane import IDockPane


class DockPaneToggleAction(Action):
    """ An Action for toggling the visibility of a dock pane.
    """

    # 'DockPaneToggleAction' interface -------------------------------------

    dock_pane = Instance(IDockPane)

    # 'Action' interface ---------------------------------------------------

    name = Property(Str, observe="dock_pane.name")
    style = "toggle"
    tooltip = Property(Str, observe="name")

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def destroy(self):
        # Make sure that we are not listening to changes to the pane anymore.
        # In traits style, we will set the basic object to None and have the
        # listener check that if it is still there.
        self.dock_pane = None

        super().destroy()

    def perform(self, event=None):
        if self.dock_pane:
            self.dock_pane.visible = not self.dock_pane.visible

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _get_name(self):
        if self.dock_pane is None:
            return "UNDEFINED"
        return self.dock_pane.name

    def _get_tooltip(self):
        return "Toggles the visibility of the %s pane." % self.name

    @observe("dock_pane.visible")
    def _update_checked(self, event):
        if self.dock_pane:
            self.checked = self.dock_pane.visible

    @observe("dock_pane.closable")
    def _update_visible(self, event):
        if self.dock_pane:
            self.visible = self.dock_pane.closable


class DockPaneToggleGroup(Group):
    """ A Group for toggling the visibility of a task's dock panes.
    """

    # 'Group' interface ----------------------------------------------------

    id = "DockPaneToggleGroup"

    items = List()

    # 'DockPaneToggleGroup' interface -------------------------------------#

    task = Property(observe="parent.controller")

    @cached_property
    def _get_task(self):
        manager = self.get_manager()

        if manager is None or manager.controller is None:
            return None

        return manager.controller.task

    dock_panes = Property(observe="task.window._states.items.dock_panes")

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

    # Private interface ----------------------------------------------------

    @observe("dock_panes.items")
    def _dock_panes_updated(self, event):
        """Recreate the group items when dock panes have been added/removed.
        """
        from pyface.action.action_item import ActionItem

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
