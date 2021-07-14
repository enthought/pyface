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

from pyface.image_resource import ImageResource

# -------------------------------------------------------------------------------
#  Constants:
# -------------------------------------------------------------------------------

image1 = ImageResource("folder")
image2 = ImageResource("gear")

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
    button7 = Button()
    button8 = Button()
    button9 = Button()
    button10 = Button()
    button11 = Button()
    button12 = Button()
    code1 = Code()
    code2 = Code()

    # ---------------------------------------------------------------------------
    #  Traits view definitions:
    # ---------------------------------------------------------------------------

    view = View(
        HSplit(
            VSplit(
                Tabbed("button1", "button2", image=image1),
                Tabbed("button3", "button4", image=image2),
            ),
            Tabbed(
                VSplit("button5", "button6"),
                Tabbed("button7", "button8"),
                HSplit("button9", "button10"),
                Group("code1@", "|<>", image=image1),
                Group("code2@", "|<>", image=image2),
                Group("button11", "button12"),
            ),
            id="dock_window",
        ),
        title="DockWindow Test",
        id="pyface.dock.dock_test3",
        dock="horizontal",
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
