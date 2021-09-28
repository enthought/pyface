# ------------------------------------------------------------------------------
# Copyright (c) 2008, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited
# Description: <Enthought undo package component>
# ------------------------------------------------------------------------------

"""

API for ``pyface.undo``.

Interfaces and Implementations
------------------------------

- :class:`~.ICommand`
- :class:`~.AbstractCommand`
- :class:`~.ICommandStack`
- :class:`~.CommandStack`
- :class:`~.IUndoManager`
- :class:`~.UndoManager`

"""

from .abstract_command import AbstractCommand
from .command_stack import CommandStack
from .i_command import ICommand
from .i_command_stack import ICommandStack
from .i_undo_manager import IUndoManager
from .undo_manager import UndoManager
