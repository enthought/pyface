
from pyface.api import GUIApplication
from pyface.action.api import (
    AboutAction, CloseWindowAction, CreateWindowAction, ExitAction, Group,
    MenuBarManager, MenuManager
)
from python_shell_window import PythonShellWindow, RunFileAction

class PythonShellApplication(GUIApplication):
    """ A GUI Application which gives an interactive Python shell. """

    #: The name of the application.
    name='Python Shell'

    #: The window factory to use.
    window_factory=PythonShellWindow

    def create_window(self):
        """ Create the window, populating the menu bar. """
        window = self.window_factory()
        window.menu_bar_manager = self.create_menubar(window)
        self.add_window(window)
        return window

    def create_menubar(self, window):
        """ Create a menubar for the PythonShellWindow """
        menu_bar = MenuBarManager(
            MenuManager(
                Group(
                    CreateWindowAction(application=self),
                    id='new_group',
                ),
                Group(
                    CloseWindowAction(window=window),
                    ExitAction(application=self),
                    id='close_group',
                ),
                name='&File', id='File',
            ),
            MenuManager(
                Group(
                    RunFileAction(window=window),
                    id='run_group',
                ),
                name='&Run', id='Run',
            ),
            MenuManager(
                Group(
                    AboutAction(application=self),
                    id='about_group',
                ),
                name='&Help', id='Help',
            )
        )
        return menu_bar


def main():
    app = PythonShellApplication(
        name='Python Shell',
        window_factory=PythonShellWindow,
    )

    with app.logging(), app.excepthook():
        app.run()


if __name__ == '__main__':
    main()
