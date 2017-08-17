"""
Simple example of an advanced task application creating tasks and panes from
traits components. Compared to the basic example, this version creates a real
TaskApplication to manage the GUI part. Additionally, the code editor uses a
tab viewer to support opening multiple files at once.

Note: Run it with
$ ETS_TOOLKIT='qt4' python run.py
as the wx backend is not supported yet for the TaskWindow.
"""
from pyface.tasks.api import TaskApplication

from example_task import ExampleTask


def create_task_window(application, files=()):
    """ Create a new task and open a window for it. """
    task = ExampleTask()
    window = application.create_task_window(task)

    # open files passed in as arguments
    for filename in files:
        try:
            task._open_file(filename)
        except Exception as exc:
            window.error(
                message="Can't open '{}'".format(filename),
            )


def main(argv):
    """ A more advanced example of using Tasks. """
    app = TaskApplication(
        id="MyTaskApplication",
        name="Python Editor",
        window_size=(800, 600),
    )

    # hook up listener to application initialized event
    def app_started(event):
        create_task_window(event.application, files=argv[1:])

    app.on_trait_change(app_started, "application_initialized")

    # run the application
    app.run()


if __name__ == '__main__':
    import sys
    main(sys.argv)
