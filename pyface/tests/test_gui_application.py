from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
from shutil import rmtree
import sys
from tempfile import mkdtemp
import unittest

from traits.api import Bool

from ..application_window import ApplicationWindow
from ..gui_application import GUIApplication
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


EVENTS = [
    'starting', 'started', 'application_initialized', 'stopping', 'stopped'
]


class TestingApp(GUIApplication):

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
        window.on_trait_change(
            lambda event: setattr(event, 'veto', self.veto_close), 'closing'
        )
        return True

    def stop(self):
        super(TestingApp, self).stop()
        return self.stop_cleanly

    def _on_window_closing(self, window, trait, old, new):
        if self.veto_close:
            new.veto = True

    def _exiting_fired(self, event):
        event.veto = self.veto_exit

    def _prepare_exit(self):
        super(TestingApp, self)._prepare_exit()
        self.exit_prepared = True
        if self.exit_prepared_error:
            raise Exception("Exit preparation failed")


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestGUIApplication(unittest.TestCase, GuiTestAssistant):

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.application_events = []

        if toolkit_object.toolkit == 'wx':
            import wx
            self.event_loop()
            wx.GetApp().DeletePendingEvents()
        else:
            self.event_loop()

    def event_listener(self, event):
        self.application_events.append(event)

    def connect_listeners(self, app):
        for event in EVENTS:
            app.on_trait_change(self.event_listener, event)

    def test_defaults(self):
        from traits.etsconfig.api import ETSConfig

        app = GUIApplication()

        self.assertEqual(app.home, ETSConfig.application_home)
        self.assertEqual(app.user_data, ETSConfig.user_data)
        self.assertEqual(app.company, ETSConfig.company)

    def test_logging_setup(self):
        dirpath = mkdtemp()
        home = os.path.join(dirpath, "test")
        app = GUIApplication(home=home)

        try:
            with app.logging():
                self.assertEqual(len(app.logging_handlers), 1)

            self.assertEqual(len(app.logging_handlers), 0)
        finally:
            rmtree(dirpath)

    def test_excepthook(self):
        excepthook = sys.excepthook
        app = GUIApplication()

        try:
            with app.excepthook():
                self.assertEqual(sys.excepthook, app._excepthook)

            self.assertEqual(sys.excepthook, excepthook)
        finally:
            sys.excepthook = excepthook

    def test_initialize_application_home(self):
        dirpath = mkdtemp()
        home = os.path.join(dirpath, "test")
        app = GUIApplication(home=home)

        app.initialize_application_home()
        try:
            self.assertTrue(os.path.exists(home))
        finally:
            rmtree(dirpath)

    def test_lifecycle(self):

        app = GUIApplication()
        self.connect_listeners(app)
        window = ApplicationWindow()
        app.on_trait_change(lambda: app.add_window(window), 'started')

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(100, app.exit)
            result = app.run()

        self.assertTrue(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_exit_prepare_error(self):
        app = TestingApp(exit_prepared_error=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(100, app.exit)
            result = app.run()

        self.assertTrue(result)
        self.assertFalse(app.exit_vetoed)
        self.assertTrue(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_veto_exit(self):
        app = TestingApp(veto_exit=True)
        self.connect_listeners(app)

        def hard_exit():
            app.exit_vetoed = True
            for window in app.windows:
                window.destroy()
                print( window.control)
            app.windows = []
            self.event_loop()
            self.gui.stop_event_loop()

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(100, app.exit)
            self.gui.invoke_after(200, hard_exit)
            result = app.run()

        self.assertTrue(result)
        self.assertTrue(app.exit_vetoed)
        self.assertFalse(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_veto_close(self):
        app = TestingApp(veto_close=True)
        self.connect_listeners(app)

        def hard_exit():
            app.exit_vetoed = True
            for window in app.windows:
                window.destroy()
            app.windows = []
            self.event_loop()
            self.gui.stop_event_loop()

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(100, app.exit)
            self.gui.invoke_after(200, hard_exit)
            result = app.run()

        self.assertTrue(result)
        self.assertTrue(app.exit_vetoed)
        self.assertFalse(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_force_exit(self):
        app = TestingApp(do_exit=True, force_exit=True, veto_exit=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(100, app.exit, True)
            result = app.run()

        self.assertTrue(result)
        self.assertFalse(app.exit_vetoed)
        self.assertTrue(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_force_exit_close_veto(self):
        app = TestingApp(do_exit=True, force_exit=True, veto_close=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(100, app.exit, True)
            result = app.run()

        self.assertTrue(result)
        self.assertFalse(app.exit_vetoed)
        self.assertTrue(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_bad_start(self):
        app = TestingApp(start_cleanly=False)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS[:1], EVENTS[1:]):
            result = app.run()

        self.assertFalse(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS[:1])
        self.assertEqual(app.windows, [])

    def test_bad_stop(self):
        app = TestingApp(stop_cleanly=False)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS[:-1], EVENTS[-1:]):
            self.gui.invoke_after(100, app.exit, True)
            result = app.run()

        self.assertFalse(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS[:-1])
        self.assertEqual(app.windows, [])