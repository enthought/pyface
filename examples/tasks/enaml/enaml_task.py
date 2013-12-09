#------------------------------------------------------------------------------
# Copyright (c) 2013, Enthought, Inc.
# All rights reserved.
#------------------------------------------------------------------------------

# Enthought library imports.
from pyface.tasks.api import Task, TaskLayout, PaneItem

# Local imports.
from enaml_panes import DummyTaskPane, DummyDockPane


class EnamlTask(Task):
    """ A simple task for demonstrating the use of Enaml in Tasks.
    """

    #### Task interface #######################################################

    id = 'example.enaml_task'
    name = 'Enaml Demo'


    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def _default_layout_default(self):
        return TaskLayout(
            left=PaneItem('example.dummy_dock_pane'))

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        return DummyTaskPane()

    def create_dock_panes(self):
        """ Create the file browser and connect to its double click event.
        """
        return [DummyDockPane()]

