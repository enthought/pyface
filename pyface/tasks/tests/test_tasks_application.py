from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import unittest

from traits.api import Bool

from pyface.application_window import ApplicationWindow
from pyface.toolkit import toolkit_object

from ..tasks_application import TasksApplication

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')

EVENTS = [
    'starting', 'started', 'application_initialized', 'stopping', 'stopped'
]


class TestingApp(TasksApplication):

    #: Whether the app should start cleanly.
    start_cleanly = Bool(True)

    #: Whether the app should stop cleanly.
    stop_cleanly = Bool(True)

    #: Whether to try invoking exit method.
    do_exit = Bool(False)

    #: Whether the exit should be invoked as an error exit.
    error_exit = Bool(False)

    #: Whether to try force the exit (ie. ignore vetoes).
    force_exit = Bool(False)

    #: Whether to veto a call to the exit method.
    veto_exit = Bool(False)

    #: Whether to veto a closing a window.
    veto_close = Bool(False)

    #: Whether or not a call to the exit method was vetoed.
    exit_vetoed = Bool(False)

    #: Whether exit preparation happened.
    exit_prepared = Bool(False)

    #: Whether exit preparation raises an error.
    exit_prepared_error = Bool(False)

    def start(self):
        if not self.start_cleanly:
            return False
        super(TestingApp, self).start()

        window = self.windows[0]
        window.on_trait_change(self._on_window_closing, 'closing')
        return True

    def stop(self):
        super(TestingApp, self).stop()
        return self.stop_cleanly

    def _on_window_closing(self, window, trait, old, new):
        if self.veto_close_window and not self.exit_vetoed:
            new.veto = True
            self.exit_vetoed = True

    def _exiting_fired(self, event):
        event.veto = self.veto_exit
        self.exit_vetoed = self.veto_exit

    def _prepare_exit(self):
        if not self.exit_vetoed:
            self.exit_prepared = True
        if self.exit_prepared_error:
            raise Exception("Exit preparation failed")
        super(TestingApp, self)._prepare_exit()


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestApplication(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.application_events = []

        if toolkit_object.toolkit == 'wx':
            import wx
            self.event_loop()
            wx.GetApp().DeletePendingEvents()
        else:
            self.event_loop()

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def event_listener(self, event):
        self.application_events.append(event)

    def connect_listeners(self, app):
        for event in EVENTS:
            app.on_trait_change(self.event_listener, event)

    def test_defaults(self):
        from traits.etsconfig.api import ETSConfig

        app = TasksApplication()

        self.assertEqual(app.home, ETSConfig.application_home)
        self.assertEqual(app.user_data, ETSConfig.user_data)
        self.assertEqual(app.company, ETSConfig.company)

    def test_lifecycle(self):

        app = TasksApplication()
        self.connect_listeners(app)
        window = ApplicationWindow()
        app.on_trait_change(lambda: app.add_window(window), 'started')

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(1000, app.exit)
            result = app.run()

        self.assertTrue(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])
