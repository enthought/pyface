from __future__ import absolute_import

import time
import unittest

from ..action_event import ActionEvent


class TestActionEvent(unittest.TestCase):

    def test_init(self):
        t0 = time.time()
        event = ActionEvent()
        t1 = time.time()
        self.assertGreaterEqual(event.when, t0)
        self.assertLessEqual(event.when, t1)
