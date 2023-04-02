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
from unittest import TestCase

from traits.api import Bool, observe
from traits.testing.api import UnittestTools

from ..application import ApplicationExit, Application

EVENTS = [
    "starting",
    "started",
    "application_initialized",
    "stopping",
    "stopped",
]


class TestingApp(Application):

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

    #: Whether or not a call to the exit method was vetoed.
    exit_vetoed = Bool(False)

    #: Whether exit preparation happened.
    exit_prepared = Bool(False)

    #: Whether exit preparation raises an error.
    exit_prepared_error = Bool(False)

    def start(self):
        super().start()
        return self.start_cleanly

    def stop(self):
        super().stop()
        return self.stop_cleanly

    def _run(self):
        super()._run()
        if self.do_exit:
            if self.error_exit:
                raise ApplicationExit("error message")
            else:
                self.exit(self.force_exit)
            self.exit_vetoed = True
        return True

    @observe('exiting')
    def _set_veto_on_exiting_event(self, event):
        vetoable_event = event.new
        vetoable_event.veto = self.veto_exit

    def _prepare_exit(self):
        self.exit_prepared = True
        if self.exit_prepared_error:
            raise Exception("Exit preparation failed")


class TestApplication(TestCase, UnittestTools):
    def setUp(self):
        self.application_events = []

    def event_listener(self, event):
        application_event = event.new
        self.application_events.append(application_event)

    def connect_listeners(self, app):
        for event in EVENTS:
            app.observe(self.event_listener, event)

    def test_defaults(self):
        from traits.etsconfig.api import ETSConfig

        app = Application()

        self.assertEqual(app.home, ETSConfig.application_home)
        self.assertEqual(app.user_data, ETSConfig.user_data)
        self.assertEqual(app.company, ETSConfig.company)

    def test_initialize_application_home(self):
        dirpath = mkdtemp()
        home = os.path.join(dirpath, "test")
        app = Application(home=home)

        app.initialize_application_home()
        try:
            self.assertTrue(os.path.exists(home))
        finally:
            rmtree(dirpath)

    def test_lifecycle(self):
        app = Application()
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            result = app.run()

        self.assertTrue(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)

    def test_exit(self):
        app = TestingApp(do_exit=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            result = app.run()

        self.assertTrue(result)
        self.assertFalse(app.exit_vetoed)
        self.assertTrue(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)

    def test_exit_prepare_error(self):
        app = TestingApp(do_exit=True, exit_prepared_error=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            result = app.run()

        self.assertTrue(result)
        self.assertFalse(app.exit_vetoed)
        self.assertTrue(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)

    def test_veto_exit(self):
        app = TestingApp(do_exit=True, veto_exit=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            result = app.run()

        self.assertTrue(result)
        self.assertTrue(app.exit_vetoed)
        self.assertFalse(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)

    def test_force_exit(self):
        app = TestingApp(do_exit=True, force_exit=True, veto_exit=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            result = app.run()

        self.assertTrue(result)
        self.assertFalse(app.exit_vetoed)
        self.assertTrue(app.exit_prepared)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)

    def test_error_exit(self):
        app = TestingApp(do_exit=True, error_exit=True)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS, []):
            result = app.run()

        self.assertFalse(result)
        self.assertFalse(app.exit_vetoed)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS)

    def test_bad_start(self):
        app = TestingApp(start_cleanly=False)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS[:1], EVENTS[1:]):
            result = app.run()

        self.assertFalse(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS[:1])

    def test_bad_stop(self):
        app = TestingApp(stop_cleanly=False)
        self.connect_listeners(app)

        with self.assertMultiTraitChanges([app], EVENTS[:-1], EVENTS[-1:]):
            result = app.run()

        self.assertFalse(result)
        event_order = [event.event_type for event in self.application_events]
        self.assertEqual(event_order, EVENTS[:-1])
