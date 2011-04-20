# Standard library imports.
from collections import defaultdict

# Enthought library imports.
from pyface.action.api import ActionController, ActionManager
from traits.api import HasTraits, Instance

# Local imports.
from pyface.tasks.task import Task
from pyface.tasks.topological_sort import before_after_sort
from schema import Schema
from schema_addition import SchemaAddition


class TaskActionManagerBuilder(HasTraits):
    """ Builds menu bars and tool bars from menu bar and tool bar schema, along
        with
    """

    # The controller to assign to the menubar and toolbars.
    controller = Instance(ActionController)

    # The Task to build menubars and toolbars for.
    task = Instance(Task)

    ###########################################################################
    # 'TaskActionManagerBuilder' interface.
    ###########################################################################

    def create_menu_bar_manager(self):
        """ Create a menu bar manager from the builder's menu bar schema and
            additions.
        """
        if self.task.menu_bar:
            return self._create_manager(self.task.menu_bar)
        return None

    def create_tool_bar_managers(self):
        """ Create tool bar managers from the builder's tool bar schemas and
            additions.
        """
        return [ self._create_manager(tbs) for tbs in self.task.tool_bars ]

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _create_manager(self, schema):
        """ Creates a manager for the specified schema using the builder's
            additions.
        """
        additions_map = defaultdict(list)
        for addition in self.task.extra_actions:
            additions_map[addition.path].append(addition)

        manager = self._create_manager_recurse(schema, additions_map)
        manager.controller = self.controller
        return manager

    def _create_manager_recurse(self, schema, additions, path=''):
        """ Recursively builds the manager for with the specified additions map.
        """
        # Compute the new action path.
        if path: path += '/'
        path += schema.id

        # Determine the order of the items at this path.
        items = schema.items
        if additions[path]:
            items = before_after_sort(items + additions[path])

        # Create the actual children by calling factory items.
        children = []
        for item in items:
            # Unpack additions first, since they may themselves be schemas.
            if isinstance(item, SchemaAddition):
                item = item.factory()

            if isinstance(item, Schema):
                item = self._create_manager_recurse(item, additions, path)

            if isinstance(item, ActionManager):
                # Give even non-root action managers a reference to the
                # controller so that custom Groups, MenuManagers, etc. can get
                # access to their Tasks.
                item.controller = self.controller
            
            children.append(item)
            
        # Finally, create the pyface.action instance for this schema.
        return schema.create(children)

    #### Trait initializers ###################################################

    def _controller_default(self):
        from task_action_controller import TaskActionController
        return TaskActionController(task=self.task)
