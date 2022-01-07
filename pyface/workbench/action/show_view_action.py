# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that shows a dialog to allow the user to choose a view. """


from .view_chooser import ViewChooser
from .workbench_action import WorkbenchAction


class ShowViewAction(WorkbenchAction):
    """ An action that shows a dialog to allow the user to choose a view. """

    # 'Action' interface ---------------------------------------------------

    # The action's unique identifier (may be None).
    id = "pyface.workbench.action.show_view"

    # The action's name (displayed on menus/tool bar tools etc).
    name = "Show View"

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Perform the action. """

        chooser = ViewChooser(window=self.window)

        ui = chooser.edit_traits(parent=self.window.control, kind="livemodal")

        # If the user closes the dialog by using the window manager's close button
        # (e.g. the little [x] in the top corner), ui.result is True, but chooser.view
        # might be None, so we need an explicit check for that.
        if ui.result and chooser.view is not None:
            # This shows the view...
            chooser.view.show()

            # ... and this makes it active (brings it to the front, gives it
            # focus etc).
            chooser.view.activate()

        return
