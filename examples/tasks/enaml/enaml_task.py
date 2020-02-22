# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Enthought library imports.
from pyface.tasks.api import Task, TaskLayout, PaneItem

# Local imports.
from enaml_panes import DummyTaskPane, DummyDockPane


class EnamlTask(Task):
    """ A simple task for demonstrating the use of Enaml in Tasks.
    """

    # Task interface -------------------------------------------------------

    id = "example.enaml_task"
    name = "Enaml Demo"

    # ------------------------------------------------------------------------
    # 'Task' interface.
    # ------------------------------------------------------------------------

    def _default_layout_default(self):
        return TaskLayout(left=PaneItem("example.dummy_dock_pane"))

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        return DummyTaskPane()

    def create_dock_panes(self):
        """ Create the file browser and connect to its double click event.
        """
        return [DummyDockPane()]
