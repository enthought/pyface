# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!from unittest import TestCase

import unittest

from pyface.toolkit import toolkit

is_wx = (toolkit.toolkit == "wx")


class TestGuiTestAssistant(unittest.TestCase):

    @unittest.skipIf(is_wx, "wx is not supported")
    def test_import(self):
        from pyface.util.gui_test_assistant import GuiTestAssistant
        self.assertNotEqual(GuiTestAssistant.__name__, "Unimplemented")
