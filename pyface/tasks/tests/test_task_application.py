from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest import TestCase

from traits.api import Bool
from traits.testing.unittest_tools import UnittestTools

from pyface.application_window import ApplicationWindow
from pyface.gui import GUI
from pyface.toolkit import toolkit_object
from ..task_application import TaskApplication


EVENTS = [
    'starting', 'started', 'application_initialized', 'stopping', 'stopped'
]


class TestingApp(TaskApplication):

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
        super(TestingApp, self).start()
        window = ApplicationWindow()
        window.on_trait_change(
            lambda event: setattr(event, 'veto', self.veto_close), 'closing'
        )
        self.add_window(window)
        return self.start_cleanly

    def stop(self):
        super(TestingApp, self).stop()
        return self.stop_cleanly

    def _on_window_closing(self, window, trait, old, new):
        if self.veto_close:
            new.veto = True

    def _exiting_fired(self, event):
        event.veto = self.veto_exit

    def _prepare_exit(self):
        self.exit_prepared = True
        if self.exit_prepared_error:
            raise Exception("Exit preparation failed")
        super(TestingApp, self)._prepare_exit()


class TestApplication(TestCase, UnittestTools):

    def setUp(self):
        self.gui = GUI()
        self.gui.exit_on_last_window_close = False
        self.application_events = []

        if toolkit_object.toolkit == 'wx':
            import wx
            self.gui.process_events()
            wx.GetApp().DeletePendingEvents()
        else:
            self.gui.process_events()

    def tearDown(self):
        # poor man's clearing of events
        if toolkit_object.toolkit == 'wx':
            import wx
            self.gui.process_events()
            wx.GetApp().DeletePendingEvents()
        else:
            self.gui.process_events()

    def event_listener(self, event):
        self.application_events.append(event)

    def connect_listeners(self, app):
        for event in EVENTS:
            app.on_trait_change(self.event_listener, event)

    def test_defaults(self):
        from traits.etsconfig.api import ETSConfig

        app = TaskApplication()

        self.assertEqual(app.home, ETSConfig.application_home)
        self.assertEqual(app.user_data, ETSConfig.user_data)
        self.assertEqual(app.company, ETSConfig.company)

    def test_lifecycle(self):

        app = TaskApplication()
        self.connect_listeners(app)
        window = ApplicationWindow()
        app.on_trait_change(lambda: app.add_window(window), 'started')

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(10000, self.gui.stop_event_loop)
            self.gui.invoke_after(100, app.exit)
            result = app.run()

        self.assertTrue(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])
