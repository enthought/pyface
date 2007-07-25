""" A simple example of using the workbench. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.pyface.api import GUI, YES
from enthought.pyface.workbench.api import Workbench

# Local imports.
from example_workbench_window import ExampleWorkbenchWindow
from person import Person


# Log to stderr.
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.DEBUG)


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

        if self.active_window.confirm('Ok to exit?') != YES:
            event.veto = True

        return


def main(argv):
    """ A simple example of using the workbench window. """
    
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()
    
    # Create some objects to edit!
    fred = Person(name='fred', age=42)
    wilma = Person(name='wilma', age=35)

    # Create the workbench.
    #
    # fixme: I wouldn't really want to specify the state location here.
    # Ideally this would be part of the GUI's as DOMs idea, and the state
    # location would be an attribute picked up from the DOM hierarchy. This
    # would also be the mechanism for doing 'confirm' etc... Let the request
    # bubble up the DOM until somebody handles it.
    workbench = ExampleWorkbench(state_location=gui.state_location)

    # Create some workbench windows.
    x = 300; y = 300
    for i in range(1):
        window = workbench.create_window(position=(x, y), size=(800, 600))
        window.open()

        # Edit some objects!
        window.edit(fred)
        window.edit(wilma)

        # Cascade the windows!
        x += 100; y += 100
    
    # Start the GUI event loop!
    gui.start_event_loop()
    
    return


if __name__ == '__main__':
    import sys; main(sys.argv)
    
#### EOF ######################################################################
