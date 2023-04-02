# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that sets the active perspective. """


from pyface.workbench.api import IPerspective
from traits.api import Delegate, Instance, observe


from .workbench_action import WorkbenchAction


class SetActivePerspectiveAction(WorkbenchAction):
    """ An action that sets the active perspective. """

    # 'Action' interface ---------------------------------------------------

    # Is the action enabled?
    enabled = Delegate("perspective")

    # The action's unique identifier (may be None).
    id = Delegate("perspective")

    # The action's name (displayed on menus/tool bar tools etc).
    name = Delegate("perspective")

    # The action's style.
    style = "radio"

    # 'SetActivePerspectiveAction' interface -------------------------------

    # The perspective that we set the active perspective to.
    perspective = Instance(IPerspective)

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def destroy(self):
        """ Destroy the action. """

        self.window = None

    def perform(self, event):
        """ Perform the action. """

        self.window.active_perspective = self.perspective

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    @observe("perspective,window.active_perspective")
    def _refresh_checked(self, event):
        """ Refresh the checked state of the action. """

        self.checked = (
            self.perspective is not None
            and self.window is not None
            and self.window.active_perspective is not None
            and self.perspective.id is self.window.active_perspective.id
        )

        return
