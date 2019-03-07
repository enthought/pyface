# Standard library imports.
from itertools import combinations
import logging

# Enthought library imports.
from traits.api import Any, HasTraits

# Local imports.
from dock_pane import AREA_MAP, INVERSE_AREA_MAP
from pyface.tasks.task_layout import LayoutContainer, PaneItem, Tabbed, \
     Splitter, HSplitter, VSplitter

# row/col orientation for AUI
ORIENTATION_NEEDS_NEW_ROW = { 
    'horizontal' : { 'top': False, 'bottom': False, 'left': True, 'right': True},
    'vertical': { 'top': True, 'bottom': True, 'left': False, 'right': False},
    }


# Logging.
logger = logging.getLogger(__name__)


class MainWindowLayout(HasTraits):
    """ A class for applying declarative layouts to an AUI managed window.
    """

    ###########################################################################
    # 'MainWindowLayout' interface.
    ###########################################################################

    def get_layout(self, layout, window):
        """ Get the layout by adding sublayouts to the specified DockLayout.
        """
        logger.debug("get_layout: %s" % layout)
        layout.perspective = window._aui_manager.SavePerspective()
        logger.debug("get_layout: saving perspective %s" % layout.perspective)

    def set_layout(self, layout, window):
        """ Applies a DockLayout to the window.
        """
        logger.debug("set_layout: %s" % layout)
        
        if hasattr(layout, "perspective"):
            self._set_layout_from_aui(layout, window)
            return

        # Perform the layout. This will assign fixed sizes to the dock widgets
        # to enforce size constraints specified in the PaneItems.
        for name, direction in AREA_MAP.items():
            sublayout = getattr(layout, name)
            if sublayout:
                self.set_layout_for_area(sublayout, direction)

        self._add_dock_panes(window)

    def _add_dock_panes(self, window):
        # Add all panes not assigned an area by the TaskLayout.
        mgr = window._aui_manager
        for dock_pane in self.state.dock_panes:
            info = mgr.GetPane(dock_pane.pane_name)
            if not info.IsOk():
                logger.debug("_add_dock_panes: managing pane %s" % dock_pane.pane_name)
                dock_pane.add_to_manager()
            else:
                logger.debug("_add_dock_panes: arleady managed pane: %s" % dock_pane.pane_name)
    
    def _set_layout_from_aui(self, layout, window):
        # The central pane will have already been added, but we need to add all
        # of the dock panes to the manager before the call to LoadPerspective
        logger.debug("_set_layout_from_aui: using saved perspective")
        self._add_dock_panes(window)
        logger.debug("_set_layout_from_aui: restoring perspective %s" % layout.perspective)
        window._aui_manager.LoadPerspective(layout.perspective)
        for dock_pane in self.state.dock_panes:
            logger.debug("validating dock pane traits for %s" % dock_pane.id)
            dock_pane.validate_traits_from_pane_info()

    def set_layout_for_area(self, layout, direction, row=None, pos=None):
        """ Applies a LayoutItem to the specified dock area.
        """
        # AUI doesn't have full, arbitrary row/col positions, nor infinitely
        # splittable areas.  Top and bottom docks are only splittable
        # vertically, and within each vertical split each can be split
        # horizontally and that's it.  Similarly, left and right docks can
        # only be split horizontally and within each horizontal split can be
        # split vertically.
        logger.debug("set_layout_for_area: %s" % INVERSE_AREA_MAP[direction])
        
        if isinstance(layout, PaneItem):
            dock_pane = self._get_dock_pane(layout)
            if dock_pane is None:
                raise MainWindowLayoutError("Unknown dock pane %r" % layout)
            dock_pane.dock_area = INVERSE_AREA_MAP[direction]
            logger.debug("layout size (%d,%d)" % (layout.width, layout.height))
            dock_pane.add_to_manager(row=row, pos=pos)
            dock_pane.visible = True
        
        elif isinstance(layout, Tabbed):
            active_pane = first_pane = None
            for item in layout.items:
                dock_pane = self._get_dock_pane(item)
                dock_pane.dock_area = INVERSE_AREA_MAP[direction]
                if item.id == layout.active_tab:
                    active_pane = dock_pane
                dock_pane.add_to_manager(tabify_pane=first_pane)
                if not first_pane:
                    first_pane = dock_pane
                dock_pane.visible = True

            # Activate the appropriate tab, if possible.
            if not active_pane:
                # By default, AUI will activate the last widget.
                active_pane = first_pane
            if active_pane:
                mgr = active_pane.task.window._aui_manager
                info = active_pane.get_pane_info()
                mgr.ShowPane(info.window, True)

        elif isinstance(layout, Splitter):
            dock_area = INVERSE_AREA_MAP[direction]
            needs_new_row = ORIENTATION_NEEDS_NEW_ROW[layout.orientation][dock_area]
            if needs_new_row:
                if row is None:
                    row = 0
                else:
                    row += 1
                for i, item in enumerate(layout.items):
                    self.set_layout_for_area(item, direction, row, pos)
                    row += 1
            else:
                pos = 0
                for i, item in enumerate(layout.items):
                    self.set_layout_for_area(item, direction, row, pos)
                    pos += 1
                
        else:
            raise MainWindowLayoutError("Unknown layout item %r" % layout)

    ###########################################################################
    # 'MainWindowLayout' abstract interface.
    ###########################################################################

    def _get_dock_widget(self, pane):
        """ Returns the QDockWidget associated with a PaneItem.
        """
        raise NotImplementedError

    def _get_pane(self, dock_widget):
        """ Returns a PaneItem for a QDockWidget.
        """
        raise NotImplementedError

    def _get_dock_pane(self, pane):
        """ Returns the DockPane associated with a PaneItem.
        """
        for dock_pane in self.state.dock_panes:
            if dock_pane.id == pane.id:
                return dock_pane
        return None


class MainWindowLayoutError(ValueError):
    """ Exception raised when a malformed LayoutItem is passed to the
    MainWindowLayout.
    """
    pass
