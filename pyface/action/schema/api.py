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
API for the ``pyface.action.schema`` subpackage.

Schemas and Aliases
-------------------

- :class:`~.ActionSchema`
- :class:`~.GroupSchema`
- :class:`~.MenuBarSchema`
- :class:`~.MenuSchema`
- :attr:`~.SGroup`
- :attr:`~.SMenu`
- :attr:`~.SMenuBar`
- :attr:`~.SToolBar`
- :class:`~.ToolBarSchema`

Builder and Schema Additions
----------------------------

- :class:`~.ActionManagerBuilder`
- :class:`~.SchemaAddition`

"""

from .action_manager_builder import ActionManagerBuilder
from .schema import (
    ActionSchema,
    GroupSchema,
    MenuBarSchema,
    MenuSchema,
    SGroup,
    SMenu,
    SMenuBar,
    SToolBar,
    ToolBarSchema,
)
from .schema_addition import SchemaAddition
