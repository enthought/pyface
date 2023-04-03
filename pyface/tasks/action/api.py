# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""

API for the ``pyface.tasks.action`` subpackage.

Tasks-specific Action Controller
--------------------------------

- :class:`~.TaskActionController`

Tasks-specific Action Manager factory
-------------------------------------

- :class:`~.TaskActionManagerBuilder`

Tasks-specific Actions
----------------------

- :class:`~.CentralPaneAction`
- :class:`~.DockPaneAction`
- :class:`~.EditorAction`
- :class:`~.TaskAction`
- :class:`~.TaskWindowAction`
- :class:`~.TasksApplicationAction`

Useful Tasks Actions and Groups
-------------------------------

- :class:`~.DockPaneToggleGroup`
- :class:`~.TaskToggleGroup`
- :class:`~.TaskWindowToggleGroup`
- :class:`~.CreateTaskWindowAction`

ActionSchemas and aliases
-------------------------

Import of these objects from pyface.tasks.actions.api is deprecated and will
be removed in a future Pyface release.  Instead use pyface.action.schema.api.

- :class:`~.ActionSchema`
- :class:`~.GroupSchema`
- :class:`~.MenuSchema`
- :class:`~.MenuBarSchema`
- :class:`~.ToolBarSchema`
- :attr:`~.SGroup`
- :attr:`~.SMenu`
- :attr:`~.SMenuBar`
- :attr:`~.SToolBar`

Schema Addition
---------------

Import of this object from pyface.tasks.actions.api is deprecated and will
be removed in a future Pyface release.  Instead use pyface.action.schema.api.

- :class:`~.SchemaAddition`

"""

from .dock_pane_toggle_group import DockPaneToggleGroup
from .schema import (
    ActionSchema,
    GroupSchema,
    MenuSchema,
    MenuBarSchema,
    ToolBarSchema,
    SGroup,
    SMenu,
    SMenuBar,
    SToolBar,
)
# deprecated: will be removed in a future Pyface release
from pyface.action.schema.schema_addition import SchemaAddition
from .task_action import (
    CentralPaneAction,
    DockPaneAction,
    EditorAction,
    TaskAction,
    TaskWindowAction,
)
from .task_action_controller import TaskActionController
from .task_action_manager_builder import TaskActionManagerBuilder
from .task_toggle_group import TaskToggleGroup
from .task_window_toggle_group import TaskWindowToggleGroup
from .tasks_application_action import (
    CreateTaskWindowAction,
    TasksApplicationAction,
)
