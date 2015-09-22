"""Example of using a splash screen (and the use of pyface Timer)."""

from __future__ import print_function

import time

from pyface.timer.api import Timer
from pyface.api import GUI, ApplicationWindow, ImageResource, SplashScreen
from pyface.action.api import Action, MenuManager, MenuBarManager
from traits.api import Any, Int


splash_screen = SplashScreen(image=ImageResource('images/splash'))


class MainWindow(ApplicationWindow):
    """ The main application window. """

    # The pyface Timer.
    my_timer = Any()

    # Count each time the timer task executes.
    counter = Int

    def __init__(self, **traits):
        """ Creates a new application window. """

        # Base class constructor.
        super(MainWindow, self).__init__(**traits)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(
                Action(name='Start Timer', on_perform=self._start_timer),
                Action(name='Stop Timer', on_perform=self._stop_timer),
                Action(name='E&xit', on_perform=self.close),
                name = '&File',
            )
        )

        return

    def _start_timer(self):
        """Called when the user selects "Start Timer" from the menu."""

        if self.my_timer is None:
            # First call, so create a Timer.  It starts automatically.
            self.my_timer = Timer(500, self._timer_task)
        else:
            self.my_timer.Start()

    def _stop_timer(self):
        """Called when the user selecte "Stop Timer" from the menu."""

        if self.my_timer is not None:
            self.my_timer.Stop()


    def _timer_task(self):
        """The method run periodically by the timer."""

        self.counter += 1
        print("counter = %d" % self.counter)


if __name__ == "__main__":

    gui = GUI(splash_screen=splash_screen)

    # Create and open the main window.
    window = MainWindow()

    # Simulate a busy window initialization.
    time.sleep(5)
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
