"""
Simple example of a task application creating tasks and panes from traits 
components. 

Note: Run it with 
$ ETS_TOOLKIT='qt4' python run.py
as the wx backend is not supported yet for the TaskWindow.
"""
# Enthought library imports.
from pyface.api import GUI
from pyface.tasks.api import TaskWindow

# Local imports.
from example_task import ExampleTask


def main(argv):
    """ A simple example of using Tasks.
    """
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create a Task and add it to a TaskWindow.
    task = ExampleTask()
    window = TaskWindow(size=(800, 600))
    window.add_task(task)

    # Show the window.
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()


if __name__ == '__main__':
    import sys
    main(sys.argv)
