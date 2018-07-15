"""
Simple example of an advanced task application creating tasks and panes from
traits components. Compared to the basic example, this version creates a real
TaskGuiApplication to manage the GUI part. Additionally, the code editor uses a
tab viewer to support opening multiple files at once.

Note: Run it with
$ ETS_TOOLKIT='qt4' python run.py
as the wx backend is not supported yet for the TaskWindow.
"""
import logging
from logging.handlers import RotatingFileHandler
import os

from traits.api import Directory, Instance, List
from pyface.tasks.api import TaskApplication
from pyface.image_resource import ImageResource
from pyface.splash_screen import SplashScreen

from example_task import ExampleTask

logger = logging.getLogger()

# Parameters for default RotatingFileHandler
LOG_FILE_MAX_SIZE = 1000000
LOG_FILE_BACKUPS = 5

# Whether to set up application in debug mode
DEBUG = False


class MyApplication(TaskApplication):
    """ This application object can subclass TaskApplication and customize
    any of the Application attributes: name, window size, logging setup, splash
    screen, ...
    """

    # -------------------------------------------------------------------------
    # TaskApplication interface
    # -------------------------------------------------------------------------

    id = "MyPyfaceApplication"

    name = "Python Editor"

    window_size = (800, 600)

    extra_actions = List(Instance(
        'pyface.tasks.action.schema_addition.SchemaAddition'
    ))

    def _on_window_closing(self, window, trait, old, new):
        """ Ask confirmation when a window is closed. """
        from pyface.api import confirm, YES

        msg = "Are you sure you want to close the window?"
        return_code = confirm(None, msg)
        if return_code != YES:
            logger.info("Window closing event was veto-ed")
            new.veto = True

    # -------------------------------------------------------------------------
    # MyApplication interface
    # -------------------------------------------------------------------------

    #: The path to the log directory.
    logdir_path = Directory

    def create_new_task_window(self):
        """ Create a new task and open a window for it.

        Returns
        -------
        window : TaskWindow
            Window that was created, containing the newly created task.
        """
        task = ExampleTask()
        task.extra_actions = self.extra_actions
        window = self.create_task_window(task)
        return window

    def setup_logging(self):
        """ Initialize logger. """
        root_logger = logging.getLogger()
        root_logger.addHandler(logging.StreamHandler())
        root_logger.setLevel(logging.DEBUG)

        filepath = os.path.join(self.logdir_path, self.id + ".log")
        file_handler = logging.RotatingFileHandler(
            filepath, backupCount=LOG_FILE_BACKUPS, maxBytes=LOG_FILE_MAX_SIZE)
        root_logger.addHandler(file_handler)
        root_logger.debug("Log file is at '{}'".format(filepath))

    def reset_logging(self):
        """ Reset root logger to default WARNING level and remove handlers.
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)

    # Traits change handlers ------------------------------------------------

    def _application_initialized_changed(self, event):
        """ Wait for event loop to be running before opening task window. """
        self.create_new_task_window()

    # Traits default handlers ------------------------------------------------

    def _icon_default(self):
        return ImageResource("python_icon.png")

    def _splash_screen_default(self):
        img = ImageResource("python_logo.png")
        return SplashScreen(image=img)

    def _logdir_path_default(self):
        return os.path.join(self.home, 'log')


def main():
    """ A more advanced example of using Tasks.
    """
    app = MyApplication()
    app.run()


if __name__ == '__main__':
    main()
