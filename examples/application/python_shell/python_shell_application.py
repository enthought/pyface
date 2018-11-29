# Copyright (c) 2014-18 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
Example GUI Application
=======================

This is an example of a Pyface GUI application.  The key bulk of the work is
done by the create_python_shell_window function which creates a
PythonShellWindow instance and overrides the window's menu bar to add
additional application-level menu items.

This also shows how to provide branding for window icons, splash-screen images
and about dialogs.
"""

import argparse

from pyface.api import GUIApplication
from pyface.action.api import (
    AboutAction, CloseActiveWindowAction, CreateWindowAction, ExitAction,
    Group, MenuBarManager, MenuManager
)

from python_shell_window import (
    OpenURLAction, PYTHON_DOCS, PythonShellWindow, RunFileAction
)


def create_python_shell_window(application, **kwargs):
    """ Factory method for constructing application window instances. """
    window = PythonShellWindow(**kwargs)

    # Override the window's menubar with an enhanced one.
    # One of the advantages of Tasks is that we can extend easily, rather
    # than just overriding.
    window.menu_bar_manager = MenuBarManager(
        MenuManager(
            Group(
                CreateWindowAction(application=application),
                id='new_group',
            ),
            Group(
                CloseActiveWindowAction(application=application),
                ExitAction(application=application),
                id='close_group',
            ),
            name='&File',
            id='File',
        ),
        MenuManager(
            Group(
                RunFileAction(window=window),
                id='run_group',
            ),
            name='&Run',
            id='Run',
        ),
        MenuManager(
            Group(
                OpenURLAction(
                    name='Python Documentation',
                    id='python_docs',
                    url=PYTHON_DOCS,
                ),
                id="documentation_group",
            ),
            Group(
                AboutAction(application=application),
                id='about_group',
            ),
            name='&Help',
            id='Help',
        )
    )
    return window


def main():
    """ GUI application entrypoint. """
    app = GUIApplication(
        id="example_python_shell_application",
        name="Python Shell",
        description="An example application that provides a Python shell.",
        icon='python_icon',
        logo='python_logo',
        window_factory=create_python_shell_window,
    )

    # handle --help etc.
    parser = argparse.ArgumentParser(description=app.description)
    parser.parse_args(namespace=app)

    app.run()


if __name__ == '__main__':
    main()
