#
# simple example of its use
#
from __future__ import print_function

import time
from pyface.api import GUI, ApplicationWindow, ProgressDialog
from pyface.action.api import Action, MenuManager, MenuBarManager

def task_func(t):
    progress = ProgressDialog(title="progress", message="counting to %d"%t, max=t, show_time=True, can_cancel=True)
    progress.open()

    for i in range(0,t+1):
        time.sleep(1)
        print(i)
        (cont, skip) = progress.update(i)
        if not cont or skip:
            break

    progress.update(t)

def _main():
    task_func(10)

class MainWindow(ApplicationWindow):
    """ The main application window. """

    ######################################################################
    # 'object' interface.
    ######################################################################

    def __init__(self, **traits):
        """ Creates a new application window. """

        # Base class constructor.
        super(MainWindow, self).__init__(**traits)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(
                Action(name='E&xit', on_perform=self.close),
                Action(name='DoIt', on_perform=_main),
                name = '&File',
            )
        )

        return


if __name__ == "__main__":
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    _main()

    # Start the GUI event loop!
    gui.start_event_loop()
