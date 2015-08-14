from __future__ import absolute_import

from traits.testing.unittest_tools import unittest, UnittestTools

from ..beep import beep


class TestBeep(unittest.TestCase):

    def test_beep(self):
        # does it call without error - the best we can do
        beep()
