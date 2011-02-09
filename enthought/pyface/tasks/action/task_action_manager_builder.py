# Standard library imports.
from collections import defaultdict

# Enthought library imports.
from enthought.pyface.action.api import ActionController, ActionManager
from enthought.traits.api import HasTraits, Instance

# Local imports.
from enthought.pyface.tasks.task import Task
from schema import Schema


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
        return self._create_manager_recurse(schema, additions_map, '')

    def _create_manager_recurse(self, schema, additions, path):
        """ Recursively builds the manager for with the specified additions map.
        """
        # Compute the new action path.
        if path: path += '/'
        path += schema.id

        # Add children that are explicitly specified, either as Schema or as
        # concrete pyface.action instances.
        children = []
        for item in schema.items:
            if isinstance(item, Schema):
                item = self._create_manager_recurse(item, additions, path)
            if isinstance(item, ActionManager):
                # Give even non-root action managers a reference to the
                # controller so that custom Groups, MenuManagers, etc. can get
                # access to their Tasks.
                item.controller = self.controller
            children.append(item)

        # Add children from the additions dictionary. In the first line, we
        # reverse the list of additions to ensure that the order of the
        # additions list given to build() is preserved (when it is not
        # completely determined by 'before' and 'after').
        for addition in reversed(additions[path]):
            # Determine the child item's index.
            if addition.before:
                index = schema.find(addition.before)
            elif addition.after:
                index = schema.find(addition.after)
                if index != -1: index += 1
            else:
                index = len(children)
            if index == -1:
                raise RuntimeError('Could not place addition %r at path %r.' %
                                   (addition, addition.path))
            
            # Insert the child item.
            item = addition.item
            if isinstance(item, ActionManager):
                # See comment above.
                item.controller = self.controller
            children.insert(index, item)

        # Finally, create the pyface.action instance for this schema.
        return schema.create(children)

    #### Trait initializers ###################################################

    def _controller_default(self):
        from task_action_controller import TaskActionController
        return TaskActionController(task=self.task)
