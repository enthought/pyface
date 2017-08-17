# Copyright (c) 2014-2016 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" Define a base Task application class to create the event loop, and launch
the creation of tasks and corresponding windows.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging
import platform

from traits.api import List, Instance, Property

from pyface.application import Application
from .task_window import TaskWindow

IS_WINDOWS = platform.system() == 'Windows'
logger = logging.getLogger(__name__)


class TaskApplication(Application):
    """ A base class for Pyface tasks applications.

    This handles setting up logging, starting up the GUI, and other common
    features that we want when creating a GUI application.
    """

    # -------------------------------------------------------------------------
    # 'TaskGuiApplication' interface
    # -------------------------------------------------------------------------

    # Tasks management --------------------------------------------------------

    #: List of all running tasks
    tasks = List("pyface.tasks.task.Task")

    #: Currently active Task if any
    active_task = Property

    #: Hook to add global schema additions to tasks/windows
    extra_actions = List(Instance(
        'pyface.tasks.action.schema_addition.SchemaAddition'
    ))

    # Window lifecycle methods -----------------------------------------------

    def create_task_window(self, task):
        """ Connect task to application and open task in a new window.
        """
        if task not in self.tasks:
            self.tasks.append(task)

        window = TaskWindow()
        window.add_task(task)
        self.add_window(window)
        return window

    # -------------------------------------------------------------------------
    # Private interface
    # -------------------------------------------------------------------------

    def _create_close_group(self):
        """ Create a close group with a 'Quit' menu item """
        from pyface.action.api import Action
        from pyface.tasks.action.api import SGroup

        return SGroup(
            Action(name='Exit' if IS_WINDOWS else 'Quit',
                   accelerator='Alt+F4' if IS_WINDOWS else 'Ctrl+Q',
                   on_perform=self.exit),
            id='QuitGroup', name='Quit',
        )

    # Destruction utilities ---------------------------------------------------

    def _on_window_closed(self, window, trait, old, new):
        """ Listener that ensures window handles are released when closed.
        """
        if window.active_task in self.tasks:
            self.tasks.remove(window.active_task)
        super(TaskApplication, self)._on_window_closed(window, trait, old, new)

    # Trait initializers and property getters ---------------------------------

    def _extra_actions_default(self):
        """ Extra application-wide menu items

        This adds close group to end of file menu. """
        from pyface.tasks.action.api import SchemaAddition

        return [
            SchemaAddition(
                id='close_group',
                path='MenuBar/File',
                absolute_position='last',
                factory=self._create_close_group,
            ),
        ]

    def _get_active_task(self):
        if self.active_window is not None:
            return self.active_window.active_task
        else:
            return None
