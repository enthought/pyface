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

from traits.api import Directory, on_trait_change
from pyface.api import AboutDialog, ImageResource, SplashScreen
from pyface.tasks.api import (
    PaneItem, TaskLayout, TasksApplication, TaskWindowLayout
)

from example_task import ExampleTask

logger = logging.getLogger()


class MyApplication(TasksApplication):
    """ This application object can subclass TasksApplication and customize
    any of the Application attributes: name, window size, logging setup, splash
    screen, ...
    """

    id = "CustomPythonEditorApplication"

    name = "Python Editor"

    icon = ImageResource("python_icon.png")

    log_dir = Directory

    # -------------------------------------------------------------------------
    # MyApplication interface
    # -------------------------------------------------------------------------

    def do_new_window(self):
        self.create_window(layout=self.default_layout[0])

    # -------------------------------------------------------------------------
    # TaskApplication interface
    # -------------------------------------------------------------------------

    def create_task(self, id):
        task = ExampleTask(id=id)
        task.extra_actions.extend(self.extra_actions)
        task.extra_dock_pane_factories.extend(self.extra_dock_pane_factories)
        return task

    # -------------------------------------------------------------------------
    # Application interface
    # -------------------------------------------------------------------------

    def setup_logging(self):
        """ Initialize logger. """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)

        log_file = os.path.join(self.log_dir, 'app.log')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        file_handler = logging.FileHandler(log_file)
        logger.addHandler(file_handler)
        logger.debug("Log file is at '{}'".format(log_file))

        self.logging_handlers += [stream_handler, file_handler]

    # -------------------------------------------------------------------------
    # Private interface
    # -------------------------------------------------------------------------

    # Traits change handlers ------------------------------------------------

    def _application_initialized_changed(self, event):
        """ Wait for event loop to be running before opening files. """
        import sys

        for filename in sys.argv[1:]:
            try:
                self.active_task._open_file(filename)
            except Exception as exc:
                print(exc)
                self.active_window.error(
                    message="Can't open '{}'".format(filename),
                )

    @on_trait_change('windows:closing')
    def _on_window_closing(self, window, trait, old, new):
        """ Ask confirmation when a window is closed. """
        from pyface.api import confirm, YES

        if not window.active_task.editor_area.editors:
            # no open editors, so OK to close
            return

        msg = "Are you sure you want to close the window?"
        return_code = confirm(None, msg)
        if return_code != YES:
            logger.info("Window closing event was vetoed")
            new.veto = True

    # Traits default handlers ------------------------------------------------

    def _log_dir_default(self):
        """ Directory for log files. """
        return os.path.join(self.home, 'log')

    def _splash_screen_default(self):
        """ Customized splash screen """
        img = ImageResource("python_logo.png")
        return SplashScreen(image=img)

    def _about_dialog_default(self):
        """ Customized About dialog """
        dialog = AboutDialog(
            image = ImageResource("python_logo.png"),
            additions = [
                u"<h1>Python Editor</h1>",
                u"<p>A simple Python editor application that demonstrates the Tasks " +
                u"framework<br>and the TasksApplication class.</p>"
                u"Copyright &copy; 2017, Enthought"
            ]
        )
        return dialog

    def _default_layout_default(self):
        """ Customized task window layout """
        layout = TaskWindowLayout(
            size=(1000, 800),
            items=[TaskLayout(
                id='example.example_task',
                right=PaneItem(id='example.python_script_browser_pane')
            )]
        )
        return [layout]

    def _extra_actions_default(self):
        """ Extra application-wide menu items"""
        from pyface.tasks.action.api import SchemaAddition
        from pyface.action.api import GUIApplicationAction

        extra_actions = super(MyApplication, self)._extra_actions_default()

        extra_actions += [
            SchemaAddition(
                id='new_window_action',
                factory=lambda: GUIApplicationAction(
                    name='New Window',
                    accelerator='Ctrl+Shift+N',
                    application=self,
                    method='do_new_window',
                ),
                before='open',
                path='MenuBar/File/open_group',
            ),
        ]
        return extra_actions

def main(argv):
    """ A more advanced example of using Tasks.
    """
    app = MyApplication()
    with app.logging(), app.excepthook():
        app.run()


if __name__ == '__main__':
    import sys
    main(sys.argv)
