# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from typing import Type

from .i_menu_bar_manager import IMenuBarManager
from .i_menu_manager import IMenuManager
from .i_status_bar_manager import IStatusBarManager
from .i_tool_bar_manager import IToolBarManager


# we know these are importable and implement the interfaces
MenuBarManager: Type[IMenuBarManager]
MenuManager: Type[IMenuManager]
StatusBarManager: Type[IStatusBarManager]
ToolBarManager: Type[IToolBarManager]
