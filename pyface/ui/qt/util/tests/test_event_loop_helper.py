# Copyright (c) 2005-2023, Enthought Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
import unittest

from traits.api import HasTraits, provides

from pyface.i_gui import IGUI
from pyface.ui.qt.util.event_loop_helper import EventLoopHelper


@provides(IGUI)
class DummyGUI(HasTraits):
    pass


class TestEventLoopHelper(unittest.TestCase):

    def test_gui_trait_expects_IGUI_interface(self):
        # Trivial test where we simply set the trait
        # and the test passes because no errors are raised.
        event_loop_helper = EventLoopHelper()
        event_loop_helper.gui = DummyGUI()
