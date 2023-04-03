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

API for the ``pyface.tasks`` submodule.

Tasks-specific Interfaces
-------------------------
- :class:`~.IDockPane`
- :class:`~pyface.tasks.i_editor.IEditor`
- :class:`~.IEditorAreaPane`
- :class:`~.ITaskPane`

Tasks, Tasks Application and related classes
--------------------------------------------

- :class:`~.AdvancedEditorAreaPane`
- :class:`~.DockPane`
- :class:`~.Editor`
- :class:`~.EditorAreaPane`
- :class:`~.SplitEditorAreaPane`
- :class:`~.Task`
- :class:`~.TasksApplication`
- :class:`~.TaskFactory`
- :class:`~.TaskPane`
- :class:`~.TaskWindow`

Tasks layout
------------
- :class:`~.TaskLayout`
- :class:`~.TaskWindowLayout`
- :class:`~.PaneItem`
- :class:`~.Tabbed`
- :class:`~.Splitter`
- :class:`~.HSplitter`
- :class:`~.VSplitter`

Traits-specific Tasks classes
-----------------------------
- :class:`~.TraitsDockPane`
- :class:`~.TraitsEditor`
- :class:`~.TraitsTaskPane`

Enaml-specific Tasks functionality
----------------------------------
- :class:`~.EnamlDockPane`
- :class:`~.EnamlEditor`
- :class:`~.EnamlTaskPane`

"""

from .i_dock_pane import IDockPane
from .i_editor import IEditor
from .i_editor_area_pane import IEditorAreaPane
from .i_task_pane import ITaskPane
from .task import Task
from .tasks_application import TasksApplication, TaskFactory
from .task_layout import (
    TaskLayout,
    PaneItem,
    Tabbed,
    Splitter,
    HSplitter,
    VSplitter,
)
from .task_window_layout import TaskWindowLayout


# ----------------------------------------------------------------------------
# Deferred imports
# ----------------------------------------------------------------------------

# These imports have the side-effect of performing toolkit selection

_toolkit_imports = {
    'AdvancedEditorAreaPane': "advanced_editor_area_pane",
    'DockPane': "dock_pane",
    'EditorAreaPane': "editor_area_pane",
    'Editor': "editor",
    'SplitEditorAreaPane': "split_editor_area_pane",
    'TaskPane': "task_pane",
}

# These are pyface.* imports that have selection as a side-effect
# TODO: refactor to delay imports where possible
_relative_imports = {
    'EnamlDockPane': "enaml_dock_pane",
    'EnamlEditor': "enaml_editor",
    'EnamlTaskPane': "enaml_task_pane",
    'TaskWindow': "task_window",
    'TraitsDockPane': "traits_dock_pane",
    'TraitsEditor': "traits_editor",
    'TraitsTaskPane': "traits_task_pane",
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
        module = import_module(f"pyface.tasks.{source}")
        result = getattr(module, name)

    elif name in _toolkit_imports:
        from pyface.toolkit import toolkit_object
        source = _toolkit_imports[name]
        result = toolkit_object(f"tasks.{source}:{name}")

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
