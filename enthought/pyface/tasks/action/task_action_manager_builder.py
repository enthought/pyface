# Standard library imports.
from collections import defaultdict

# Enthought library imports.
from enthought.traits.api import HasTraits, Instance, List

# Local imports.
from schema import Schema, MenuBarSchema, ToolBarSchema
from schema_addition import SchemaAddition


class TaskActionManagerBuilder(HasTraits):
    """ Builds menu bars and tool bars from menu bar and tool bar schema, along
        with
    """

    # The menu bar schema to be used by the builder.
    menu_bar_schema = Instance(MenuBarSchema)

    # The list of tool bar schemas to be used by the builder.
    tool_bar_schemas = List(ToolBarSchema)

    # The list of extra actions/groups/menus to be inserted into the action
    # managers constructed by the builder.
    additions = List(SchemaAddition)

    ###########################################################################
    # 'TaskActionManagerBuilder' interface.
    ###########################################################################

    def create_menu_bar_manager(self):
        """ Create a menu bar manager from the builder's menu bar schema and
            additions.
        """
        return self._create_manager(self.menu_bar_schema)

    def create_tool_bar_managers(self):
        """ Create tool bar managers from the builder's tool bar schemas and
            additions.
        """
        return [ self._create_manager(tbs) for tbs in self.tool_bar_schemas ]

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _create_manager(self, schema):
        """ Creates a manager for the specified schema using the builder's
            additions.
        """
        additions_map = defaultdict(list)
        for addition in self.additions:
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
            children.append(item)

        # Add children from the additions dictionary. In the first line, we
        # reverse the list of additions to ensure that the order of the
        # additions list given to build() is preserved (when it is not
        # completely determined by 'before' and 'after').
        for addition in reversed(additions[path]):
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
            children.insert(index, addition.item)

        # Finally, create the pyface.action instance for this schema.
        return schema.create(children)
