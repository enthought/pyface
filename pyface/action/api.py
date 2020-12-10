# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


"""

API for the ``pyface.action`` submodule.

Action and subclasses
---------------------

- :class:`~.Action`
- :class:`~.FieldAction`
- :class:`~.GUIApplicationAction`
- :class:`~.ListeningAction`
- :class:`~.TraitsUIWidgetAction`
- :class:`~.WindowAction`

Action Controller
-----------------

- :class:`~.ActionController`

Action Event
------------

- :class:`~.ActionEvent`

Action Manager and subclasses
-----------------------------

- :class:`~.ActionManager`

Toolkit-specific subclasses:

- ``MenuManager``
- ``MenuBarManager``
- ``ToolBarManager``
- ``ToolPaletteManager``, only for the Wx toolkit.
- ``StatusBarManager``. Note that the ``StatusBarManager`` is not actually an
  ``ActionManager`` subclass but it is listed here given it's similarily in
  function to the other subclasses.

Action Manager item and subclasses
----------------------------------

- :class:`~.ActionManagerItem`
- :class:`~.ActionItem`

Group and subclasses
--------------------

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

from .action import Action
from .action_controller import ActionController
from .action_event import ActionEvent
from .action_item import ActionItem
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
from .listening_action import ListeningAction
from .menu_manager import MenuManager
from .menu_bar_manager import MenuBarManager
from .status_bar_manager import StatusBarManager
from .tool_bar_manager import ToolBarManager
from .traitsui_widget_action import TraitsUIWidgetAction
from .window_action import CloseWindowAction, WindowAction

# This part of the module handles widgets that are still wx specific.  This
# will all be removed when everything has been ported to PyQt and pyface
# becomes toolkit agnostic.

from traits.etsconfig.api import ETSConfig

if ETSConfig.toolkit == "wx":
    from .tool_palette_manager import ToolPaletteManager
