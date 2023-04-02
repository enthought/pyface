# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import os
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from traits.api import Bool, observe

from ..application_window import ApplicationWindow
from ..gui_application import GUIApplication
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

EVENTS = [
    "starting",
    "started",
    "application_initialized",
    "stopping",
    "stopped",
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

    #: Whether to veto a opening a window.
    veto_open_window = Bool(False)

    #: Whether to veto a closing a window.
    veto_close_window = Bool(False)

    #: Whether or not a call to the open a window was vetoed.
    window_open_vetoed = Bool(False)

    #: Whether or not a call to the exit method was vetoed.
    exit_vetoed = Bool(False)

    #: Whether exit preparation happened.
    exit_prepared = Bool(False)

    #: Whether exit preparation raises an error.
    exit_prepared_error = Bool(False)

    def start(self):
        if not self.start_cleanly:
            return False
        super().start()

        window = self.windows[0]
        window.observe(self._on_window_closing, "closing")
        return True

    def stop(self):
        super().stop()
        return self.stop_cleanly

    def _on_window_closing(self, event):
        window = event.new
        if self.veto_close_window and not self.exit_vetoed:
            window.veto = True
            self.exit_vetoed = True

    @observe("application_initialized")
    def _update_window_open_vetoed(self, event):
        self.window_open_vetoed = (
            len(self.windows) > 0 and self.windows[0].control is None
        )

    @observe('exiting')
    def _set_veto_on_exiting_event(self, event):
        vetoable_event = event.new
        vetoable_event.veto = self.veto_exit
        self.exit_vetoed = self.veto_exit

    def _prepare_exit(self):
        super()._prepare_exit()
        if not self.exit_vetoed:
            self.exit_prepared = True
        if self.exit_prepared_error:
            raise Exception("Exit preparation failed")

    @observe("windows:items:opening")
    def _on_activate_window(self, event):
        if self.veto_open_window:
            window = event.new
            window.veto = self.veto_open_window


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestGUIApplication(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.application_events = []

        if toolkit_object.toolkit == "wx":
            import wx

            self.event_loop()
            wx.GetApp().DeletePendingEvents()
        else:
            self.event_loop()

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def event_listener(self, event):
        application_event = event.new
        self.application_events.append(application_event)

    def connect_listeners(self, app):
        for event in EVENTS:
            app.observe(self.event_listener, event)

    def test_defaults(self):
        from traits.etsconfig.api import ETSConfig

        app = GUIApplication()

        self.assertEqual(app.home, ETSConfig.application_home)
        self.assertEqual(app.user_data, ETSConfig.user_data)
        self.assertEqual(app.company, ETSConfig.company)

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
        app.observe(lambda _: app.add_window(window), "started")

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(1000, app.exit)
            result = app.run()

        self.assertTrue(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_exit_prepare_error(self):
        app = TestingApp(exit_prepared_error=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(1000, app.exit)
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

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(1000, app.exit)
            self.gui.invoke_after(2000, app.exit, force=True)
            result = app.run()

        self.assertTrue(result)
        self.assertTrue(app.exit_vetoed)
        self.assertFalse(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_veto_open_window(self):
        app = TestingApp(veto_open_window=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(1000, app.exit)
            result = app.run()

        self.assertTrue(result)
        self.assertTrue(app.window_open_vetoed)
        self.assertFalse(app.exit_vetoed)
        self.assertTrue(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)
        self.assertEqual(app.windows, [])

    def test_veto_close_window(self):
        app = TestingApp(veto_close_window=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(1000, app.exit)
            self.gui.invoke_after(2000, app.exit, force=True)
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
        app = TestingApp(do_exit=True, force_exit=True, veto_close_window=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            self.gui.invoke_after(1000, app.exit, True)
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
            self.gui.invoke_after(1000, app.exit, True)
            result = app.run()

        self.assertFalse(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS[:-1])
        self.assertEqual(app.windows, [])
