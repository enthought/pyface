"""
Simple example of an advanced task application creating tasks and panes from
traits components. Compared to the basic example, this version creates a real
TaskApplication to manage the GUI part. Additionally, the code editor uses a
tab viewer to support opening multiple files at once.

Note: Run it with
$ ETS_TOOLKIT='qt4' python run.py
as the wx backend is not supported yet for the TaskWindow.
"""

from pyface.api import ImageResource, SplashScreen
from pyface.tasks.api import TasksApplication
from pyface.tasks.task_application import TaskFactory

from example_task import ExampleTask


def open_files(window, files=()):
    """ Open a list of files in the task. """
    for filename in files:
        try:
            window.active_task._open_file(filename)
        except Exception as exc:
            window.error(
                message="Can't open '{}'".format(filename),
            )


def main(argv):
    """ A more advanced example of using Tasks. """
    app = TasksApplication(
        id="PythonEditorApplication",
        name="Python Editor",
        splash_screen=SplashScreen(
            image=ImageResource("python_logo.png")
        ),
        task_factories=[
            TaskFactory(
                id='example.example_task',
                name='Python Editor',
                factory=ExampleTask
            ),
        ],
    )
    app.about_dialog.image = ImageResource("python_logo.png")
    app.about_dialog.additions += [
        u"<p>A simple Python editor application that demonstrates the Tasks " +
        u"framework<br>and the TasksApplication class.</p>"
    ]

    # hook up listener to application initialized event to open files
    def app_started(event):
        open_files(event.application.windows[0], files=argv[1:])

    app.on_trait_change(app_started, "application_initialized")

    # run the application
    app.run()


if __name__ == '__main__':
    import sys
    main(sys.argv)
