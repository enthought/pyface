""" A simple example of using the workbench. """


# Enthought library imports.
from pyface.api import YES
from pyface.workbench.api import Workbench

# Local imports.
from example_workbench_window import ExampleWorkbenchWindow


class ExampleWorkbench(Workbench):
    """ A simple example of using the workbench. """

    #### 'Workbench' interface ################################################

    # The factory (in this case simply a class!) that is used to create
    # workbench windows.
    window_factory = ExampleWorkbenchWindow

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _exiting_changed(self, event):
        """ Called when the workbench is exiting. """

        if self.confirm('Ok to exit?') != YES:
            event.veto = True

        return

#### EOF ######################################################################
