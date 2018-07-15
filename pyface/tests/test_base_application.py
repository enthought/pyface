from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
from shutil import rmtree
import sys
from tempfile import mkdtemp
from unittest import TestCase

from traits.api import Bool
from traits.testing.unittest_tools import UnittestTools

from ..application import ApplicationExit, BaseApplication


EVENTS = [
    'starting', 'started', 'application_initialized', 'stopping', 'stopped'
]


class TestingApp(BaseApplication):

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
        super(TestingApp, self).start()
        return self.start_cleanly

    def stop(self):
        super(TestingApp, self).stop()
        return self.stop_cleanly

    def _run(self):
        super(TestingApp, self)._run()
        if self.do_exit:
            if self.error_exit:
                raise ApplicationExit("error message")
            else:
                self.exit(self.force_exit)
            self.exit_vetoed = True
        return True

    def _exiting_fired(self, event):
        event.veto = self.veto_exit

    def _prepare_exit(self):
        self.exit_prepared = True
        if self.exit_prepared_error:
            raise Exception("Exit preparation failed")


class TestBaseApplication(TestCase, UnittestTools):

    def setUp(self):
        self.application_events = []

    def event_listener(self, event):
        self.application_events.append(event)

    def connect_listeners(self, app):
        for event in EVENTS:
            app.on_trait_change(self.event_listener, event)

    def test_defaults(self):
        from traits.etsconfig.api import ETSConfig

        app = BaseApplication()

        self.assertEqual(app.home, ETSConfig.application_home)
        self.assertEqual(app.user_data, ETSConfig.user_data)
        self.assertEqual(app.company, ETSConfig.company)

    def test_logging_setup(self):
        dirpath = mkdtemp()
        home = os.path.join(dirpath, "test")
        app = BaseApplication(home=home)

        app.setup_logging()
        try:
            try:
                self.assertEqual(len(app.logging_handlers), 1)
            finally:
                app.reset_logging()

            self.assertEqual(len(app.logging_handlers), 0)
        finally:
            rmtree(dirpath)

    def test_excepthook(self):
        excepthook = sys.excepthook
        app = BaseApplication()

        app.install_excepthook()
        try:
            self.assertEqual(sys.excepthook, app._excepthook)
            app.reset_excepthook()
            self.assertEqual(sys.excepthook, excepthook)
        finally:
            sys.excepthook = excepthook

    def test_initialize_application_home(self):
        dirpath = mkdtemp()
        home = os.path.join(dirpath, "test")
        app = BaseApplication(home=home)

        app.initialize_application_home()
        try:
            self.assertTrue(os.path.exists(home))
        finally:
            rmtree(dirpath)

    def test_lifecycle(self):
        app = BaseApplication()
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
