# Standard library imports.
from collections import defaultdict
import logging

# Enthought library imports.
from pyface.action.api import ActionController, ActionManager
from traits.api import HasTraits, Instance

# Local imports.
from pyface.tasks.task import Task
from pyface.tasks.topological_sort import before_after_sort
from schema import Schema, ToolBarSchema
from schema_addition import SchemaAddition

# Logging.
logger = logging.getLogger(__name__)


class TaskActionManagerBuilder(HasTraits):
    """ Builds menu bars and tool bars from menu bar and tool bar schema, along
    with any additions provided by the task.
    """

    # The controller to assign to the menubar and toolbars.
    controller = Instance(ActionController)

    # The Task to build menubars and toolbars for.
    task = Instance(Task)

    ###########################################################################
    # 'TaskActionManagerBuilder' interface.
    ###########################################################################

    def create_action_manager(self, schema):
        """ Create a manager for the given schema using the task's additions.
        """
        additions_map = defaultdict(list)
        for addition in self.task.extra_actions:
            if addition.path:
                additions_map[addition.path].append(addition)

        manager = self._create_action_manager_recurse(schema, additions_map)
        manager.controller = self.controller
        return manager

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
        schemas = self.task.tool_bars[:]
        for addition in self.task.extra_actions:
            if not addition.path:
                schema = addition.factory()
                if isinstance(schema, ToolBarSchema):
                    schemas.append(schema)
                else:
                    logger.error('Invalid top-level schema addition: %r. Only '
                                 'ToolBar schemas can be path-less.', schema)
        return [ self.create_action_manager(schema)
                 for schema in self._get_ordered_schemas(schemas) ]

    def prepare_item(self, item, path):
        """ Called immediately after a concrete Pyface item has been created
        (or, in the case of items that are not produced from schemas,
        immediately before they are processed).

        This hook can be used to perform last-minute transformations or
        configuration. Returns a concrete Pyface item.
        """
        return item

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_action_manager_recurse(self, schema, additions, path=''):
        """ Recursively create a manager for the given schema and additions map.
        """
        # Compute the new action path.
        if path: path += '/'
        path += schema.id

        # Determine the order of the items at this path.
        items = schema.items
        if additions[path]:
            items = self._get_ordered_schemas(items + additions[path])

        # Create the actual children by calling factory items.
        children = []
        for item in items:
            # Unpack additions first, since they may themselves be schemas.
            if isinstance(item, SchemaAddition):
                item = item.factory()

            if isinstance(item, Schema):
                item = self._create_action_manager_recurse(item,additions,path)
            else:
                item = self.prepare_item(item, path+'/'+item.id)

            if isinstance(item, ActionManager):
                # Give even non-root action managers a reference to the
                # controller so that custom Groups, MenuManagers, etc. can get
                # access to their Tasks.
                item.controller = self.controller
            
            children.append(item)
            
        # Finally, create the pyface.action instance for this schema.
        return self.prepare_item(schema.create(children), path)

    def _get_ordered_schemas(self, schemas):
        begin = []
        middle = []
        end = []

        for schema in schemas:
            absolute_position = getattr(schema, 'absolute_position', None)
            if absolute_position is None:
                middle.append(schema)
            elif absolute_position == 'last':
                end.append(schema)
            else:
                begin.append(schema)

        schemas = (before_after_sort(begin)
                   + before_after_sort(middle)
                   + before_after_sort(end))

    #### Trait initializers ###################################################

    def _controller_default(self):
        from task_action_controller import TaskActionController
        return TaskActionController(task=self.task)
