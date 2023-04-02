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
from unittest.mock import MagicMock

from pyface.toolkit import toolkit

not_wx = toolkit.toolkit != "wx"


class TestDockControl(unittest.TestCase):

    @unittest.skipIf(not_wx, "This test is specific to the wx backend")
    def test_feature_changed(self):
        from pyface.dock.dock_sizer import DockControl
        dock_control = DockControl()
        DockControl.set_feature_mode = MagicMock()
        dock_control.feature_changed = True

        dock_control.set_feature_mode.assert_called_once_with()
