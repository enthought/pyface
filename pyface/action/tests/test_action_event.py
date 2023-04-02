# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


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
