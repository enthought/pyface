"""
Simple example of an advanced task application creating tasks and panes from
traits components. Compared to the basic example, this version creates a real
TaskGuiApplication to manage the GUI part. Additionally, the code editor uses a
tab viewer to support opening multiple files at once.

Note: Run it with
$ ETS_TOOLKIT='qt4' python run.py
as the wx backend is not supported yet for the TaskWindow.
"""
# Enthought library imports.
from traits.api import Str, Tuple

from pyface.tasks.api import TaskApplication

# Local imports.
from example_task import ExampleTask


class MyApplication(TaskApplication):
    """ This application object can subclass TaskApplication and customize
    any of the Application attributes: name, window size, logging setup, splash
    screen, ...
    """

    # -------------------------------------------------------------------------
    # TaskGuiApplication interface
    # -------------------------------------------------------------------------

    app_name = Str("My Pyface Application")

    window_size = Tuple((800, 600))


    def start(self):
        starting = super(MyApplication, self).start()
        if not starting:
            return False

        self.create_new_task_window()
        return True

    # -------------------------------------------------------------------------
    # MyApplication interface
    # -------------------------------------------------------------------------

    def create_new_task_window(self):
        """ Create a new task and open a window for it.

        Returns
        -------
        window : TaskWindow
            Window that was created, containing the newly created task.
        """
        task = ExampleTask()
        window = self.create_task_window(task)
        return window


def main(argv):
    """ A more advanced example of using Tasks.
    """
    app = MyApplication()
    app.run()


if __name__ == '__main__':
    import sys
    main(sys.argv)
