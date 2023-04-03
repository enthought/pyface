# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from traits.api import Instance, Property, Str, cached_property


from pyface.tasks.i_editor import IEditor
from pyface.tasks.task import Task
from pyface.tasks.i_task_pane import ITaskPane
from pyface.action.listening_action import ListeningAction


class TaskAction(ListeningAction):
    """ An Action that makes a callback to a Task.

    Note that this is a convenience class. Actions associated with a Task need
    not inherit TaskAction, although they must, of course, inherit Action.
    """

    # ListeningAction interface --------------------------------------------

    object = Property(observe="task")

    # TaskAction interface -------------------------------------------------

    #: The Task with which the action is associated. Set by the framework.
    task = Instance(Task)

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _get_object(self):
        return self.task

    def destroy(self):
        # Disconnect listeners to task and dependent properties.
        self.task = None
        super().destroy()


class TaskWindowAction(TaskAction):
    """ An Action that makes a callback to a Task's window.
    """

    # ListeningAction interface --------------------------------------------

    object = Property(observe="task.window")

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _get_object(self):
        if self.task:
            return self.task.window
        return None


class CentralPaneAction(TaskAction):
    """ An Action that makes a callback to a Task's central pane.
    """

    # ListeningAction interface --------------------------------------------

    object = Property(observe="central_pane")

    # CentralPaneAction interface -----------------------------------------#

    #: The central pane with which the action is associated.
    central_pane = Property(Instance(ITaskPane), observe="task")

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    @cached_property
    def _get_central_pane(self):
        if self.task and self.task.window is not None:
            return self.task.window.get_central_pane(self.task)
        return None

    def _get_object(self):
        return self.central_pane


class DockPaneAction(TaskAction):
    """ An Action the makes a callback to one of a Task's dock panes.
    """

    # ListeningAction interface --------------------------------------------

    object = Property(observe="dock_pane")

    # DockPaneAction interface ---------------------------------------------

    #: The dock pane with which the action is associated. Set by the framework.
    dock_pane = Property(Instance(ITaskPane), observe="task")

    #: The ID of the dock pane with which the action is associated.
    dock_pane_id = Str()

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    @cached_property
    def _get_dock_pane(self):
        if self.task and self.task.window is not None:
            return self.task.window.get_dock_pane(self.dock_pane_id, self.task)
        return None

    def _get_object(self):
        return self.dock_pane


class EditorAction(CentralPaneAction):
    """ An action that makes a callback to the active editor in an editor pane.
    """

    # ListeningAction interface --------------------------------------------

    object = Property(observe="active_editor")

    # EditorAction interface -----------------------------------------------

    #: The active editor in the central pane with which the action is associated.
    active_editor = Property(
        Instance(IEditor), observe="central_pane.active_editor"
    )

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    @cached_property
    def _get_active_editor(self):
        if self.central_pane is not None:
            return self.central_pane.active_editor
        return None

    def _get_object(self):
        return self.active_editor
