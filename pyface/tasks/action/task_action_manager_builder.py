# Standard library imports.
from collections import defaultdict
import logging

# Enthought library imports.
from pyface.action.api import ActionController, ActionManager
from traits.api import HasTraits, Instance

# Local imports.
from pyface.tasks.task import Task
from pyface.tasks.topological_sort import before_after_sort
from pyface.tasks.action.schema import Schema, ToolBarSchema
from pyface.tasks.action.schema_addition import SchemaAddition

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
        return schemas

    def _group_items_by_id(self, items):
        """ Group a list of action items by their ID.

        Action items are Schemas and Groups, MenuManagers, etc.

        Return a dictionary {item_id: list_of_items}, and a list containing
        all the ids ordered by their appearance in the `all_items` list. The
        ordered IDs are used as a replacement for an ordered dictionary, to
        keep compatibility with Python <2.7 .

        """

        ordered_items_ids = []
        id_to_items = defaultdict(list)

        for item in items:
            if item.id not in id_to_items:
                ordered_items_ids.append(item.id)
            id_to_items[item.id].append(item)

        return id_to_items, ordered_items_ids

    def _group_items_by_class(self, items):
        """ Group a list of action items by their class.

        Action items are Schemas and Groups, MenuManagers, etc.

        Return a dictionary {item_class: list_of_items}, and a list containing
        all the classes ordered by their appearance in the `all_items` list.
        The ordered classes are used as a replacement for an ordered
        dictionary, to keep compatibility with Python <2.7 .

        """

        ordered_items_class = []
        class_to_items = defaultdict(list)

        for item in items:
            if item.__class__ not in class_to_items:
                ordered_items_class.append(item.__class__)
            class_to_items[item.__class__].append(item)

        return class_to_items, ordered_items_class

    def _unpack_schema_additions(self, items):
        """ Unpack additions, since they may themselves be schemas. """

        unpacked_items = []

        for item in items:
            if isinstance(item, SchemaAddition):
                unpacked_items.append(item.factory())
            else:
                unpacked_items.append(item)

        return unpacked_items

    def _merge_items_with_same_path(self, id_to_items, ordered_items_ids):
        """ Merge items with the same path if possible.

        Items must be subclasses of `Schema` and they must be instances of
        the same class to be merged.

        """

        merged_items = []
        for item_id in ordered_items_ids:
            items_with_same_id = id_to_items[item_id]

            # Group items by class.
            class_to_items, ordered_items_class =\
            self._group_items_by_class(items_with_same_id)

            for items_class in ordered_items_class:
                items_with_same_class = class_to_items[items_class]

                if len(items_with_same_class) == 1:
                    merged_items.extend(items_with_same_class)

                else:
                    # Only schemas can be merged.
                    if issubclass(items_class, Schema):
                        # Merge into a single schema.
                        items_content = sum(
                            (item.items for item in items_with_same_class), []
                        )

                        merged_item = items_with_same_class[0].clone_traits()
                        merged_item.items = items_content
                        merged_items.append(merged_item)

                    else:
                        merged_items.extend(items_with_same_class)

        return merged_items

    def _preprocess_schemas(self, schema, additions, path):
        """ Sort and merge a schema and a set of schema additions. """

        # Determine the order of the items at this path.
        if additions[path]:
            all_items = self._get_ordered_schemas(schema.items+additions[path])
        else:
            all_items = schema.items

        unpacked_items = self._unpack_schema_additions(all_items)

        id_to_items, ordered_items_ids = self._group_items_by_id(unpacked_items)

        merged_items = self._merge_items_with_same_path(id_to_items,
                                                        ordered_items_ids)

        return merged_items

    def _create_action_manager_recurse(self, schema, additions, path=''):
        """ Recursively create a manager for the given schema and additions map.

        Items with the same path are merged together in a single entry if
        possible (i.e., if they have the same class).

        When a list of items is merged, their children are added to a clone
        of the first item in the list. As a consequence, traits like menu
        names etc. are inherited from the first item.

        """

        # Compute the new action path.
        if path:
            path = path + '/' + schema.id
        else:
            path = schema.id

        preprocessed_items = self._preprocess_schemas(schema, additions, path)

        # Create the actual children by calling factory items.
        children = []
        for item in preprocessed_items:
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

    #### Trait initializers ###################################################

    def _controller_default(self):
        from task_action_controller import TaskActionController
        return TaskActionController(task=self.task)
