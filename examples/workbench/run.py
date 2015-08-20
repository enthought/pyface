""" Run the workbench example. """


# Standard library imports.
import logging

# Enthought library imports.
from pyface.api import GUI

# Local imports.
from example_workbench import ExampleWorkbench
from person import Person


# Log to stderr.
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(open('example_workbench.log', 'w')))
logger.setLevel(logging.DEBUG)


def main(argv):
    """ A simple example of using the workbench. """

    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create some objects to edit.
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
    for i in range(2):
        window = workbench.create_window(position=(x, y), size=(800, 600))
        window.open()

        # Edit the objects if they weren't restored from a previous session.
        if window.get_editor_by_id('fred') is None:
            window.edit(fred)

        if window.get_editor_by_id('wilma') is None:
            window.edit(wilma)

        # Cascade the windows.
        x += 100; y += 100

    # Start the GUI event loop.
    gui.start_event_loop()

    return


if __name__ == '__main__':
    import sys; main(sys.argv)

#### EOF ######################################################################
