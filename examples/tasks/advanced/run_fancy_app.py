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
import os

from traits.api import Directory, Instance, List
from pyface.tasks.api import TaskApplication
from pyface.image_resource import ImageResource
from pyface.splash_screen import SplashScreen

from example_task import ExampleTask

logger = logging.getLogger()


class MyApplication(TaskApplication):
    """ This application object can subclass TaskApplication and customize
    any of the Application attributes: name, window size, logging setup, splash
    screen, ...
    """

    # -------------------------------------------------------------------------
    # TaskApplication interface
    # -------------------------------------------------------------------------

    id = "PythonEditorApplication"

    name = "Python Editor"

    window_size = (800, 600)

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

    def create_window(self, layout=None):
        """ Create a new task and open a window for it.

        Returns
        -------
        window : TaskWindow
            Window that was created, containing the newly created task.
        """
        task = ExampleTask()
        task.extra_actions.extend(self.extra_actions)
        task.extra_dock_pane_factories.extend(self.extra_dock_pane_factories)
        window = self.create_task_window(task)
        return window

    def _setup_logging(self):
        """ Initialize logger. """
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        filepath = os.path.join(self.logdir_path, self.id + ".log")
        logger.addHandler(logging.FileHandler(filepath))
        logger.debug("Log file is at '{}'".format(filepath))

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


def main(argv):
    """ A more advanced example of using Tasks.
    """
    app = MyApplication()
    app.run()


if __name__ == '__main__':
    import sys
    main(sys.argv)
