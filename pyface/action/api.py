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

API for the ``pyface.action`` subpackage.

Actions
-------

- :class:`~.Action`
- :class:`~.FieldAction`
- :class:`~.GUIApplicationAction`
- :class:`~.ListeningAction`
- :class:`~.TraitsUIWidgetAction`
- :class:`~.WindowAction`

Action Controller
-----------------

- :class:`~pyface.action.action_controller.ActionController`

Action Event
------------

- :class:`~.ActionEvent`

Action Managers
---------------

- :class:`~.ActionManager`
- ``MenuManager``
- ``MenuBarManager``
- ``StatusBarManager``
- ``ToolBarManager``

Action Manager Items
--------------------

- :class:`~.ActionManagerItem`
- :class:`~.ActionItem`

Layout support
--------------

- :class:`~.Group`
- :class:`~.Separator`

Useful Application and Window actions
-------------------------------------

- :class:`~.AboutAction`
- :class:`~.CloseActiveWindowAction`
- :class:`~.CreateWindowAction`
- :class:`~.ExitAction`
- :class:`~.CloseWindowAction`

"""

# Imports which don't select the toolkit as a side-effect.

from .action import Action
from .action_controller import ActionController
from .action_event import ActionEvent
from .action_manager import ActionManager
from .action_manager_item import ActionManagerItem
from .field_action import FieldAction
from .group import Group, Separator
from .gui_application_action import (
    AboutAction,
    CloseActiveWindowAction,
    CreateWindowAction,
    ExitAction,
    GUIApplicationAction,
)
from .i_action_manager import IActionManager
from .i_menu_bar_manager import IMenuBarManager
from .i_menu_manager import IMenuManager
from .i_status_bar_manager import IStatusBarManager
from .i_tool_bar_manager import IToolBarManager
from .listening_action import ListeningAction
from .traitsui_widget_action import TraitsUIWidgetAction
from .window_action import CloseWindowAction, WindowAction


# ----------------------------------------------------------------------------
# Deferred imports
# ----------------------------------------------------------------------------

# These imports have the side-effect of performing toolkit selection

_toolkit_imports = {
    'MenuManager': "menu_manager",
    'MenuBarManager': "menu_bar_manager",
    'StatusBarManager': "status_bar_manager",
    'ToolBarManager': "tool_bar_manager",
}

# These are pyface.* imports that have selection as a side-effect
# TODO: refactor to delay imports where possible
_relative_imports = {
    'ActionItem': "action_item",
}


def __getattr__(name):
    """Lazily load attributes with side-effects

    In particular, lazily load toolkit backend names.  For efficiency, lazily
    loaded objects are injected into the module namespace
    """
    # sentinel object for no result
    not_found = object()
    result = not_found

    if name in _relative_imports:
        from importlib import import_module
        source = _relative_imports[name]
        module = import_module(f"pyface.action.{source}")
        result = getattr(module, name)

    elif name in _toolkit_imports:
        from pyface.toolkit import toolkit_object
        source = _toolkit_imports[name]
        result = toolkit_object(f"action.{source}:{name}")

    if result is not_found:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    globals()[name] = result
    return result


# ----------------------------------------------------------------------------
# Introspection support
# ----------------------------------------------------------------------------

# the list of available names we report for introspection purposes
_extra_names = set(_toolkit_imports) | set(_relative_imports)


def __dir__():
    return sorted(set(globals()) | _extra_names)
