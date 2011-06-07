# Standard library imports.
from itertools import combinations

# System library imports.
from traits.qt import QtCore, QtGui

# Enthought library imports.
from traits.api import Any

# Local imports.
from dock_pane import AREA_MAP
from pyface.tasks.task_layout import LayoutContainer, DockArea, PaneItem, \
     Tabbed, Splitter, HSplitter, VSplitter

# Contants.
ORIENTATION_MAP = { 'horizontal' : QtCore.Qt.Horizontal,
                    'vertical': QtCore.Qt.Vertical }
QWIDGETSIZE_MAX = (1 << 24) - 1 # Not exposed by Qt bindings.


class MainWindowLayout(HasTraits):
    """ A class for applying declarative layouts to a QMainWindow.
    """

    # The QMainWindow on which to operate.
    control = Any

    ###########################################################################
    # 'MainWindowLayout' interface.
    ###########################################################################

    def get_layout(self, layout, include_sizes=True):
        """ Get the layout by adding DockAreas to the specified LayoutContainer.
        """
        for name, q_dock_area in AREA_MAP.iteritems():
            sublayout = self.get_layout_for_area(q_dock_area, include_sizes)
            if sublayout:
                layout.items.append(DockArea(sublayout, area=name))

    def get_layout_for_area(self, q_dock_area, include_sizes=True):
        """ Gets a LayoutItem for the specified dock area.
        """
        # Build the initial set of leaf-level items.
        items = set()
        rects = {}
        for child in self.children():
            # Iterate through *visibile* dock widgets. (Inactive tabbed dock
            # widgets are "visible" but have invalid positions.)
            if isinstance(child, QtGui.QDockWidget) and child.isVisible() and \
                   self.control.dockWidgetArea(child) == q_dock_area and \
                   child.x() >= 0 and child.y() >= 0:
                # Get the list of dock widgets in this tab group in order.
                geometry = child.geometry()
                tabs = self.control.tabifiedDockWidgets(child)
                if tabs:
                    tab_bar = self._get_tab_bar(child)
                    tabs.insert(tab_bar.currentIndex(), child)
                    geometry = tab_bar.geometry().united(geometry)

                # Create the leaf-level item for the child.
                if tabs:
                    panes = [ self.get_pane(w, include_sizes) for w in tabs ]
                    item = Tabbed(*panes, active_tab=child.windowTitle())
                else:
                    item = self.get_pane(child, include_sizes)
                items.add(item)
                rects[item] = geometry

        # Build the layout tree bottom-up, in multiple passes.
        while len(items) > 1:
            add, remove = set(), set()
            
            for item1, item2 in combinations(items, 2):
                if item1 not in remove and item2 not in remove:
                    rect1, rect2 = rects[item1], rects[item2]
                    orient = self._get_division_orientation(rect1, rect2, True)
                    if orient == QtCore.Qt.Horizontal:
                        if rect1.y() < rect2.y():
                            item = VSplitter(item1, item2)
                        else:
                            item = VSplitter(item2, item1)
                    elif orient == QtCore.Qt.Vertical:
                        if rect1.x() < rect2.x():
                            item = HSplitter(item1, item2)
                        else:
                            item = HSplitter(item2, item1)
                    else:
                        continue
                    rects[item] = rect1.united(rect2)
                    add.add(item)
                    remove.update((item1, item2))
                    
            if add or remove:
                items.update(add)
                items.difference_update(remove)
            else:
                # Raise an exception instead of falling into an infinite loop.
                raise RuntimeError('Unable to extract layout from QMainWindow.')

        if items:
            return items.pop()
        return None

    ###########################################################################
    # 'MainWindowLayout' abstract interface.
    ###########################################################################

    def _get_pane_for_widget(self, dock_widget):
        pass

    def _get_widget_for_pane(self, pane):
        pass

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_division_orientation(self, one, two, splitter=False):
        """ Returns whether there is a division between two visible QWidgets.

        Divided in context means that the widgets are adjacent and aligned along
        the direction of the adjaceny.
        """
        united = one.united(two)
        if splitter:
            sep = self.style().pixelMetric(
                QtGui.QStyle.PM_DockWidgetSeparatorExtent, None, self)
            united.adjust(0, 0, -sep, -sep)
            
        if one.x() == two.x() and one.width() == two.width() and \
               united.height() == one.height() + two.height():
            return QtCore.Qt.Horizontal
        
        elif one.y() == two.y() and one.height() == two.height() and \
                 united.width() == one.width() + two.width():
            return QtCore.Qt.Vertical
        
        return 0

    def _get_tab_bar(self, dock_widget):
        """ Returns the tab bar associated with the given QDockWidget, or None
        if there is no tab bar.
        """
        dock_geometry = dock_widget.geometry()
        for child in self.children():
            if isinstance(child, QtGui.QTabBar) and child.isVisible():
                geometry = child.geometry()
                if self._get_division_orientation(dock_geometry, geometry):
                    return child
        return None

    def _prepare_toplevel_for_item(self, layout):
        """
        """
        if isinstance(layout, Pane):
            dock_widget = self._get_widget_for_pane(pane)
            if layout.width > 0:
                dock_widget.widget().setFixedWidth(layout.width)
            if layout.height > 0:
                dock_widget.widget().setFixedHeight(layout.height)
            return dock_widget
        
        elif isinstance(layout, LayoutContainer):
            return self.get_toplevel_for_item(layout.items[0])
        
        else:
            raise LayoutError("Leaves of layout must be Panes.")

    def _reset_fixed_sizes(self):
        """
        """
        for child in self.children():
            if isinstance(child, QtGui.QDockWidget):
                child.widget().setFixedSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
