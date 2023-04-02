# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance, List, Property

from pyface.action.schema.action_manager_builder import ActionManagerBuilder
from pyface.action.schema.schema_addition import SchemaAddition
from pyface.tasks.task import Task


class TaskActionManagerBuilder(ActionManagerBuilder):
    """ ActionManagerBuilder for Tasks.

    This provides some additional convenience methods for extracting schema
    information from a task and using it to build menu bar and toolbar
    managers directly.
    """

    #: The Task to build menubars and toolbars for.
    task = Instance(Task)

    #: The schema additions provided by the Task.
    additions = Property(List(SchemaAddition), observe='task.extra_actions')

    # ------------------------------------------------------------------------
    # 'TaskActionManagerBuilder' interface.
    # ------------------------------------------------------------------------

    def create_menu_bar_manager(self):
        """ Create a menu bar manager from the task's menu bar schema and
            additions.
        """
        if self.task.menu_bar:
            return self.create_action_manager(self.task.menu_bar)
        return None

    def create_tool_bar_managers(self):
        """ Create tool bar managers from the tasks's tool bar schemas and
            additions.
        """
        schemas = self.task.tool_bars + self.get_additional_toolbar_schemas()
        return [
            self.create_action_manager(schema)
            for schema in self._get_ordered_schemas(schemas)
        ]

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    # Trait initializers ---------------------------------------------------

    def _controller_default(self):
        from .task_action_controller import TaskActionController

        return TaskActionController(task=self.task)

    # Trait properties -----------------------------------------------------

    def _get_additions(self):
        # keep synchronized to task's extra actions, since that may change
        if self.task:
            return self.task.extra_actions
        else:
            return []
