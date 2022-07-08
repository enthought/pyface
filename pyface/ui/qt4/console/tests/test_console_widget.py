# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest

from pyface.qt.QtGui import QApplication

from ..console_widget import ConsoleWidget


class TestConsoleWidget(unittest.TestCase):

    def setUp(self):
        # ensure QApplication is set up
        QApplication().instance()

    def test_format_as_columns(self):
        # regression test for Pyface #1146
        widget = ConsoleWidget()
        text = widget._format_as_columns(
            ["one", "two", "three"]
        )

        self.assertEqual(
            text,
            "one  two  three\n"
        )
