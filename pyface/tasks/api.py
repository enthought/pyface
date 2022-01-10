# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
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

from .advanced_editor_area_pane import AdvancedEditorAreaPane
from .split_editor_area_pane import SplitEditorAreaPane
from .dock_pane import DockPane
from .editor import Editor
from .editor_area_pane import EditorAreaPane
from .enaml_dock_pane import EnamlDockPane
from .enaml_editor import EnamlEditor
from .enaml_task_pane import EnamlTaskPane
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
from .task_pane import TaskPane
from .task_window import TaskWindow
from .task_window_layout import TaskWindowLayout
from .traits_dock_pane import TraitsDockPane
from .traits_editor import TraitsEditor
from .traits_task_pane import TraitsTaskPane
