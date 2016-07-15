"""
Simple demo of tasks used to develop the wx support for tasks.
"""
# Enthought library imports.
from pyface.api import GUI
from pyface.tasks.api import Task, TaskWindow, EditorAreaPane

class BlankTask(Task):
    """ A task that does nothing
    """

    #### Task interface #######################################################

    id = 'example.blank_task'
    name = 'Blank'

    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        self.editor_area = EditorAreaPane()
        return self.editor_area

def main(argv):
    """ A simple example of using Tasks.
    """
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create a Task and add it to a TaskWindow.
    task = BlankTask()
    window = TaskWindow(size=(800, 600))
    window.add_task(task)

    # Show the window.
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()


if __name__ == '__main__':
    import sys
    main(sys.argv)
