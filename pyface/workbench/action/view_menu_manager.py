# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The 'View' menu """


import logging


from pyface.action.api import Group, MenuManager
from traits.api import Any, Bool, Instance, List, Str
from traits.api import observe


from .perspective_menu_manager import PerspectiveMenuManager
from .show_view_action import ShowViewAction
from .toggle_view_visibility_action import ToggleViewVisibilityAction


# Logging.
logger = logging.getLogger(__name__)


class ViewMenuManager(MenuManager):
    """ The 'View' menu.

    By default, this menu is displayed on the main menu bar.

    """

    # 'ActionManager' interface --------------------------------------------

    # All of the groups in the manager.
    groups = List(Group)

    # The manager's unique identifier (if it has one).
    id = Str("View")

    # 'MenuManager' interface ---------------------------------------------#

    # The menu manager's name (if the manager is a sub-menu, this is what its
    # label will be).
    name = Str("&View")

    # 'ViewMenuManager' interface -----------------------------------------#

    # Should the perspective menu be shown?
    show_perspective_menu = Bool(True)

    # The workbench window that the menu is part of.
    window = Instance("pyface.workbench.api.WorkbenchWindow")

    # 'Private' interface -------------------------------------------------#

    # The group containing the view hide/show actions.
    _view_group = Any()

    # ------------------------------------------------------------------------
    # 'ActionManager' interface.
    # ------------------------------------------------------------------------

    def _groups_default(self):
        """ Trait initializer. """

        groups = []

        # Add a group containing the perspective menu (if requested).
        if self.show_perspective_menu and len(self.window.perspectives) > 0:
            groups.append(Group(PerspectiveMenuManager(window=self.window)))

        # Add a group containing a 'toggler' for all visible views.
        self._view_group = self._create_view_group(self.window)
        groups.append(self._view_group)

        # Add a group containing an 'Other...' item that will launch a dialog
        # to allow the user to choose a view to show.
        groups.append(self._create_other_group(self.window))

        return groups

    # ------------------------------------------------------------------------
    # 'ViewMenuManager' interface.
    # ------------------------------------------------------------------------

    @observe("window.active_perspective,window.active_part,window.views.items")
    def refresh(self, event):
        """ Refreshes the checked state of the actions in the menu. """

        logger.debug("refreshing view menu")

        if self._view_group is not None:
            self._clear_group(self._view_group)
            self._initialize_view_group(self.window, self._view_group)
            self.changed = True

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _clear_group(self, group):
        """ Remove all items in a group. """

        # fixme: Fix this API in Pyface so there is only one call!
        group.destroy()
        group.clear()

    def _create_other_group(self, window):
        """ Creates a group containing the 'Other...' action. """

        group = Group()
        group.append(ShowViewAction(name="Other...", window=window))

        return group

    def _create_view_group(self, window):
        """ Creates a group containing the view 'togglers'. """

        group = Group()
        self._initialize_view_group(window, group)

        return group

    def _initialize_view_group(self, window, group):
        """ Initializes a group containing the view 'togglers'. """

        views = window.views[:]
        views.sort(key=lambda view: view.name)

        for view in views:
            # fixme: It seems a little smelly to be reaching in to the window
            # layout here. Should the 'contains_view' method be part of the
            # window interface?
            if window.layout.contains_view(view):
                group.append(
                    ToggleViewVisibilityAction(view=view, window=window)
                )

        return
