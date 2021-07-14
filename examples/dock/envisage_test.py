# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import wx

from traits.api import *

from traitsui.api import *

from traitsui.menu import *

from pyface.image_resource import ImageResource

from pyface.dock.api import *

# -------------------------------------------------------------------------------
#  Global data:
# -------------------------------------------------------------------------------

# DockControl style to use:
style = "tab"

image1 = ImageResource("folder")
image2 = ImageResource("gear")

# -------------------------------------------------------------------------------
#  Creates a DockWindow as a Traits UI widget:
# -------------------------------------------------------------------------------


def create_dock_window(parent, editor):
    """ Creates a window for editing a workflow canvas.
    """
    main = DockWindow(parent).control
    views = [wx.Button(main, -1, "View %d" % (i + 1)) for i in range(6)]
    edit = DockWindow(main).control
    editors = [wx.Button(edit, -1, "Editor %d" % (i + 1)) for i in range(6)]
    controls = [
        DockControl(
            name="Editor %d" % (i + 1),
            image=image1,
            closeable=True,
            control=editors[i],
            style=style,
        )
        for i in range(6)
    ]
    controls[0].export = "any"
    edit_sizer = DockSizer(contents=[tuple(controls)])
    main_sizer = DockSizer(
        contents=[
            [
                DockControl(
                    name="View 1",
                    image=image1,
                    closeable=True,
                    control=views[0],
                    style=style,
                ),
                DockControl(
                    name="View 2",
                    image=image1,
                    closeable=True,
                    height=400,
                    control=views[1],
                    style=style,
                ),
            ],
            [
                DockControl(
                    name="Editors", image=image1, control=edit, style="fixed"
                ),
                [
                    DockControl(
                        name="View 3",
                        image=image2,
                        control=views[2],
                        style=style,
                    ),
                    DockControl(
                        name="View 4",
                        image=image2,
                        control=views[3],
                        style=style,
                    ),
                ],
            ],
            [
                DockControl(name="View 5", control=views[4], style=style),
                DockControl(name="View 6", control=views[5], style=style),
            ],
        ]
    )
    edit.SetSizer(edit_sizer)
    main.SetSizer(main_sizer)

    return main


# -------------------------------------------------------------------------------
#  'EnvisageDock' class:
# -------------------------------------------------------------------------------


class EnvisageDock(HasPrivateTraits):

    # ---------------------------------------------------------------------------
    #  Trait definitions:
    # ---------------------------------------------------------------------------

    dummy = Int()

    # ---------------------------------------------------------------------------
    #  Traits view definitions:
    # ---------------------------------------------------------------------------

    view = View(
        [
            Item(
                "dummy",
                resizable=True,
                editor=CustomEditor(create_dock_window),
            ),
            "|<>",
        ],
        title="Envisage DockWindow Mock-up",
        resizable=True,
        width=1.00,
        height=1.00,
        buttons=NoButtons,
    )


# -------------------------------------------------------------------------------
#  Run the test program:
# -------------------------------------------------------------------------------

if __name__ == "__main__":
    EnvisageDock().configure_traits()
