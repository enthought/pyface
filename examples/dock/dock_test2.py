# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import sys

from traits.api import *

from traitsui.api import *

from traitsui.menu import *

# -------------------------------------------------------------------------------
#  'TestDock' class:
# -------------------------------------------------------------------------------


class TestDock(HasPrivateTraits):

    # ---------------------------------------------------------------------------
    #  Trait definitions:
    # ---------------------------------------------------------------------------

    button1 = Button()
    button2 = Button()
    button3 = Button()
    button4 = Button()
    button5 = Button()
    button6 = Button()

    # ---------------------------------------------------------------------------
    #  Traits view definitions:
    # ---------------------------------------------------------------------------

    view = View(
        ["button1"],
        ["button2"],
        ["button3"],
        ["button4"],
        ["button5"],
        ["button6"],
        title="DockWindow Test",
        resizable=True,
        width=0.5,
        height=0.5,
        buttons=NoButtons,
    )


# -------------------------------------------------------------------------------
#  Run the test program:
# -------------------------------------------------------------------------------

if __name__ == "__main__":
    TestDock().configure_traits()
