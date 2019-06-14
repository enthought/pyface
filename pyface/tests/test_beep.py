from __future__ import absolute_import

import unittest

from traits.testing.unittest_tools import UnittestTools

from ..beep import beep


class TestBeep(unittest.TestCase):

    def test_beep(self):
        # does it call without error - the best we can do
        beep()
