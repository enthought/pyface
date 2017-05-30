"""
Qt-specific tests for the Qt GUI implementation.
"""
from __future__ import absolute_import

import unittest

from traits.api import Event, HasStrictTraits, Instance

from pyface.api import GUI
from pyface.i_gui import IGUI
from pyface.util.guisupport import is_event_loop_running_qt4


class SimpleApplication(HasStrictTraits):
    """
    Simple application that attempts to set a trait at start time,
    and immediately exits in response to that trait.
    """
    # The GUI instance underlying this app.
    gui = Instance(IGUI)


    # Event fired after the event loop starts.
    application_running = Event

    def __init__(self):
        super(HasStrictTraits, self).__init__()
        self.gui = GUI()

    def start(self):
        """
        Start the application.
        """
        # This shouldn't be executed until after the event loop is running.
        self.gui.set_trait_later(self, 'application_running', True)
        self.gui.start_event_loop()

    def stop(self):
        self.gui.stop_event_loop()


class TestGui(unittest.TestCase):
    def test_set_trait_later_runs_later(self):
        # Regression test for enthought/pyface#272.
        application = SimpleApplication()

        application_running = []

        def exit_app():
            # Record whether the event loop is running or not, then exit.
            application_running.append(
                is_event_loop_running_qt4()
            )
            application.stop()

        application.on_trait_change(exit_app, 'application_running')
        application.start()

        self.assertTrue(application_running[0])
