# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Object with views for naming or renaming a user perspective. """


from traits.api import Bool, HasTraits, Constant, String
from traitsui.api import View, Item, VGroup


# Trait definitions --------------------------------------------------------

# Define a trait which can not be the empty string:
NotEmptyString = String(minlen=1)


class UserPerspectiveName(HasTraits):
    """ Object with views for naming or renaming a user perspective. """

    # ------------------------------------------------------------------------
    # 'UserPerspectiveName' interface.
    # ------------------------------------------------------------------------

    # The name of the new user perspective.
    name = NotEmptyString

    # Should the editor area be shown in this perpsective?
    show_editor_area = Bool(True)

    # Help notes when creating a new view.
    new_help = Constant(
        """Note:
 - The new perspective will initially be empty.
 - Add new views to the perspective by selecting
   them from the 'View' menu.
 - Drag the notebook tabs and splitter bars to
   arrange the views within the perspective."""
    )

    # Traits views ---------------------------------------------------------

    new_view = View(
        VGroup(
            VGroup("name", "show_editor_area"),
            VGroup("_", Item("new_help", style="readonly"), show_labels=False),
        ),
        title="New User Perspective",
        id="envisage.workbench.action."
        "new_user_perspective_action.UserPerspectiveName",
        buttons=["OK", "Cancel"],
        kind="livemodal",
        width=300,
    )

    save_as_view = View(
        "name",
        title="Save User Perspective As",
        id="envisage.workbench.action."
        "save_as_user_perspective_action.UserPerspectiveName",
        buttons=["OK", "Cancel"],
        kind="livemodal",
        width=300,
    )

    rename_view = View(
        "name",
        title="Rename User Perspective",
        id="envisage.workbench.action."
        "rename_user_perspective_action.UserPerspectiveName",
        buttons=["OK", "Cancel"],
        kind="livemodal",
        width=300,
    )
