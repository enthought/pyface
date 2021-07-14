# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Example Tasks Application
=========================

This is a Tasks application to demonstrate a vary basic multi-tab,
multi-window editor.  The application is very thin, since all we need to do
is supply the task factory for the Python editor task.  More sophisticated
applications may need to subclass the application class to hold
application-global state and provide application-global functionality.
"""

import argparse

from pyface.tasks.api import TaskFactory, TasksApplication

from python_editor_task import PythonEditorTask


def main():
    """ Main entrypoint for the application. """

    app = TasksApplication(
        id="example_python_editor_application",
        name="Python Editor",
        description=(
            "An example Tasks application that provides a Python editor."
        ),
        icon="python_icon",
        logo="python_logo",
        task_factories=[
            TaskFactory(
                id="example.python_editor_task",
                name="Python Editor",
                factory=PythonEditorTask,
            )
        ],
    )

    # get file names from arguments
    parser = argparse.ArgumentParser(description=app.description)
    parser.add_argument("files", nargs="*", help="the files to open")
    namespace = parser.parse_args()
    if len(namespace.files) == 0:
        namespace.files.append("")

    # set up callback to open files once app is up and running
    def open_files(event):
        """ Open files once app is active. """
        for path in namespace.files:
            app.active_task.create_editor(path)

    app.observe(open_files, "application_initialized")

    # invoke the mainloop
    app.run()


if __name__ == "__main__":
    main()
