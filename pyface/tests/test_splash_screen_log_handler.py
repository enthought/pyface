# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from traits.api import HasTraits, Str

from ..splash_screen_log_handler import SplashScreenLogHandler


class DummySplashScreen(HasTraits):
    text = Str("original")


class DummyRecord(object):
    def __init__(self, message):
        self.message = message

    def getMessage(self):
        return self.message


class TestSplashScreenLogHandler(unittest.TestCase):
    def setUp(self):
        self.ss = DummySplashScreen()
        self.sslh = SplashScreenLogHandler(self.ss)

    def test_unicode_message(self):
        self.assertEqual(self.ss.text, "original")
        message = "G\u00f6khan"
        self.sslh.emit(DummyRecord(message))
        self.assertEqual(self.ss.text, message + "...")

    def test_ascii_message(self):
        message = "Goekhan"
        self.sslh.emit(DummyRecord(message))
        self.assertEqual(self.ss.text, message + "...")
