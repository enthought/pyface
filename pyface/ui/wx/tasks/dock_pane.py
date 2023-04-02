# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import logging


from pyface.tasks.i_dock_pane import IDockPane, MDockPane
from traits.api import (
    Bool,
    observe,
    Property,
    provides,
    Tuple,
    Str,
    Int,
)


import wx
from pyface.wx.aui import aui


from .task_pane import TaskPane

# Constants.
AREA_MAP = {
    "left": aui.AUI_DOCK_LEFT,
    "right": aui.AUI_DOCK_RIGHT,
    "top": aui.AUI_DOCK_TOP,
    "bottom": aui.AUI_DOCK_BOTTOM,
}
INVERSE_AREA_MAP = dict((int(v), k) for k, v in AREA_MAP.items())

# Logging
logger = logging.getLogger(__name__)


@provides(IDockPane)
class DockPane(TaskPane, MDockPane):
    """ The toolkit-specific implementation of a DockPane.

    See the IDockPane interface for API documentation.
    """

    # Keep a reference to the Aui pane name in order to update dock state
    pane_name = Str()

    # Whether the title bar of the pane is currently visible.
    caption_visible = Bool(True)

    # AUI ring number; note that panes won't be movable out of their ring
    # number.  This is a way to isolate panes
    dock_layer = Int(0)

    # 'IDockPane' interface ------------------------------------------------

    size = Property(Tuple)

    # Protected traits -----------------------------------------------------

    _receiving = Bool(False)

    # ------------------------------------------------------------------------
    # 'ITaskPane' interface.
    # ------------------------------------------------------------------------

    @classmethod
    def get_hierarchy(cls, parent, indent=""):
        lines = ["%s%s %s" % (indent, str(parent), parent.GetName())]
        for child in parent.GetChildren():
            lines.append(cls.get_hierarchy(child, indent + "  "))
        return "\n".join(lines)

    def create(self, parent):
        """ Create and set the dock widget that contains the pane contents.
        """
        # wx doesn't need a wrapper control, so the contents become the control
        self.control = self.create_contents(parent)

        # hide the pane till the task gets activated, whereupon it will take
        # its visibility from the task state
        self.control.Hide()

        # Set the widget's object name. This important for AUI Manager state
        # saving. Use the task ID and the pane ID to avoid collisions when a
        # pane is present in multiple tasks attached to the same window.
        self.pane_name = self.task.id + ":" + self.id
        logger.debug(
            "dock_pane.create: %s  HIERARCHY:\n%s"
            % (self.pane_name, self.get_hierarchy(parent, "    "))
        )

    def get_new_info(self):
        info = aui.AuiPaneInfo().Name(self.pane_name).DestroyOnClose(False)

        # size?

        # Configure the dock widget according to the DockPane settings.
        self.update_dock_area(info)
        self.update_dock_features(info)
        self.update_dock_title(info)
        self.update_floating(info)
        self.update_visible(info)

        return info

    def add_to_manager(self, row=None, pos=None, tabify_pane=None):
        info = self.get_new_info()
        if tabify_pane is not None:
            target = tabify_pane.get_pane_info()
            logger.debug(
                "dock_pane.add_to_manager: Tabify! %s onto %s"
                % (self.pane_name, target.name)
            )
        else:
            target = None
        if row is not None:
            info.Row(row)
        if pos is not None:
            info.Position(pos)
        self.task.window._aui_manager.AddPane(
            self.control, info, target=target
        )

    def validate_traits_from_pane_info(self):
        """ Sync traits from the AUI pane info.

        Useful after perspective restore to make sure e.g. visibility state
        is set correctly.
        """
        info = self.get_pane_info()
        self.visible = info.IsShown()

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the contents.
        """
        if self.control is not None:
            logger.debug("Destroying %s" % self.control)
            self.task.window._aui_manager.DetachPane(self.control)

            # Some containers (e.g.  TraitsDockPane) will destroy the control
            # before we get here (e.g.  traitsui.ui.UI.finish by way of
            # TraitsDockPane.destroy), so check to see if it's already been
            # destroyed.  Fortunately, the Reparent in DetachPane still seems
            # to work on a destroyed control.
            if self.control:
                self.control.Hide()
                self.control.Destroy()
            self.control = None

    # ------------------------------------------------------------------------
    # 'IDockPane' interface.
    # ------------------------------------------------------------------------

    def create_contents(self, parent):
        """ Create and return the toolkit-specific contents of the dock pane.
        """
        return wx.Window(parent, name=self.task.id + ":" + self.id)

    # Trait property getters/setters ---------------------------------------

    def _get_size(self):
        if self.control is not None:
            return self.control.GetSize().Get()
        return (-1, -1)

    # Trait change handlers ------------------------------------------------

    def get_pane_info(self):
        info = self.task.window._aui_manager.GetPane(self.pane_name)
        return info

    def commit_layout(self, layout=True):
        if layout:
            self.task.window._aui_manager.Update()
        else:
            self.task.window._aui_manager.UpdateWithoutLayout()

    def commit_if_active(self, layout=True):
        # Only attempt to commit the AUI changes if the area if the task is active.
        main_window = self.task.window.control
        if main_window and self.task == self.task.window.active_task:
            self.commit_layout(layout)
        else:
            logger.debug("task not active so not committing...")

    def update_dock_area(self, info):
        info.Direction(AREA_MAP[self.dock_area])
        logger.debug(
            "info: dock_area=%s dir=%s" % (self.dock_area, info.dock_direction)
        )

    @observe("dock_area")
    def _set_dock_area(self, event):
        logger.debug("trait change: dock_area")
        if self.control is not None:
            info = self.get_pane_info()
            self.update_dock_area(info)
            self.commit_if_active()

    def update_dock_features(self, info):
        info.CloseButton(self.closable)
        info.Floatable(self.floatable)
        info.Movable(self.movable)
        info.CaptionVisible(self.caption_visible)
        info.Layer(self.dock_layer)

    @observe("closable,floatable,movable,caption_visible,dock_layer")
    def _set_dock_features(self, event):
        if self.control is not None:
            info = self.get_pane_info()
            self.update_dock_features(info)
            self.commit_if_active()

    def update_dock_title(self, info):
        info.Caption(self.name)

    @observe("name")
    def _set_dock_title(self, event):
        if self.control is not None:
            info = self.get_pane_info()
            self.update_dock_title(info)

            # Don't need to refresh everything if only the name is changing
            self.commit_if_active(False)

    def update_floating(self, info):
        if self.floating:
            info.Float()
        else:
            info.Dock()

    @observe("floating")
    def _set_floating(self, event):
        if self.control is not None:
            info = self.get_pane_info()
            self.update_floating(info)
            self.commit_if_active()

    def update_visible(self, info):
        if self.visible:
            info.Show()
        else:
            info.Hide()

    @observe("visible")
    def _set_visible(self, event):
        logger.debug(
            "_set_visible %s on pane=%s, control=%s"
            % (self.visible, self.pane_name, self.control)
        )
        if self.control is not None:
            info = self.get_pane_info()
            self.update_visible(info)
            self.commit_if_active()
