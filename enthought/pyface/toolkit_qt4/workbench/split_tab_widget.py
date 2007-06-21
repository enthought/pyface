#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major library imports.
from PyQt4 import QtCore, QtGui


class SplitTabWidget(QtGui.QSplitter):
    """ The SplitTabWidget class is a hierarchy of QSplitters the leaves of
    which are QTabWidgets.  Any tab may be moved around with the hierarchy
    automatically extended and reduced as required.
    """

    # The different hotspots of a QTabWidget.  An non-negative value is a tab
    # index and the hotspot is to the left of it.
    _HS_NONE = -1
    _HS_AFTER_LAST_TAB = -2
    _HS_NORTH = -3
    _HS_SOUTH = -4
    _HS_EAST = -5
    _HS_WEST = -6

    def __init__(self, *args):
        """ Initialise the instance. """

        QtGui.QSplitter.__init__(self, *args)

        self._rband = None
        self._selected_tab_widget = None
        self._selected_hotspot = self._HS_NONE

    def addTab(self, w, text):
        """ Add a new tab to the main tab widget. """

        # Find the first tab widget going down the left of the hierarchy.  This
        # will be the one in the top left corner.
        if self.count() > 0:
            ch = self.widget(0)

            while not isinstance(ch, _TabWidget):
                assert isinstance(ch, QtGui.QSplitter)
                ch = ch.widget(0)
        else:
            # There is not tab widget so create one.
            ch = _TabWidget(self)
            self.addWidget(ch)

        ch.addTab(w, text)

    def setCurrentWidget(self, w):
        """ Make the given widget current. """

        tw = self._tab_widget(w)

        if tw is not None:
            tw.setCurrentWidget(w)

    def select(self, pos):
        tw, hs, hs_geom = self._hotspot(pos)

        # See if the hotspot has changed.
        if self._selected_tab_widget is not tw or self._selected_hotspot != hs:
            if self._selected_tab_widget is not None:
                self._rband.hide()

            if tw is not None and hs != self._HS_NONE:
                # Create the rubber band if it hasn't already been done.
                if self._rband is None:
                    self._rband = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle)

                self._rband.setGeometry(*hs_geom)
                self._rband.show()

            self._selected_tab_widget = tw
            self._selected_hotspot = hs

    def drop(self, stab_w, stab):
        self._rband.hide()

        dtab_w = self._selected_tab_widget
        dhs = self._selected_hotspot

        # Handle the trivial case.
        if dtab_w is None or dhs == self._HS_NONE:
            return

        self._selected_tab_widget = None
        self._selected_hotspot = self._HS_NONE

        # See if the tab is being moved to an existing tab widget.
        if dhs >= 0 or dhs == self._HS_AFTER_LAST_TAB:
            # Make sure it really is being moved.
            if stab_w is dtab_w:
                if stab == dhs:
                    return

                if dhs == self._HS_AFTER_LAST_TAB and stab == stab_w.count() - 1:
                    return

            ttext, twidg = self._remove_tab(stab_w, stab)

            if dhs == self._HS_AFTER_LAST_TAB:
                idx = dtab_w.addTab(twidg, ttext)
            elif dtab_w is stab_w:
                # Adjust the index if necessary because in case the removal of
                # the tab from its old position has skewed things.
                dst = dhs

                if dhs > stab:
                    dst -= 1

                idx = dtab_w.insertTab(dst, twidg, ttext)
            else:
                idx = dtab_w.insertTab(dhs, twidg, ttext)

            # Make the tab current in its new position.
            dtab_w.setCurrentIndex(idx)
        else:
            # Remove the tab from its current tab widget and create a new one
            # for it.
            ttext, twidg = self._remove_tab(stab_w, stab)
            new_tw = _TabWidget(self)
            new_tw.addTab(twidg, ttext)

            # Get the splitter containing the destination tab widget.
            dspl = dtab_w.parent()
            dspl_idx = dspl.indexOf(dtab_w)

            if dhs in (self._HS_NORTH, self._HS_SOUTH):
                dspl, dspl_idx = self._horizontal_split(dspl, dspl_idx, dhs)
            else:
                dspl, dspl_idx = self._vertical_split(dspl, dspl_idx, dhs)

            # Add the new tab widget in the right place.
            dspl.insertWidget(dspl_idx, new_tw)

        stab_w.still_needed()

    def _horizontal_split(self, spl, idx, hs):
        """ Returns a tuple of the splitter and index where the new tab widget
        should be put.
        """

        if spl.orientation() == QtCore.Qt.Vertical:
            if hs == self._HS_SOUTH:
                idx += 1
        elif spl is self and spl.count() == 1:
            # The splitter is the root and only has one child so we can just
            # change its orientation.
            spl.setOrientation(QtCore.Qt.Vertical)

            if hs == self._HS_SOUTH:
                idx = -1
        else:
            new_spl = QtGui.QSplitter(QtCore.Qt.Vertical)
            new_spl.addWidget(spl.widget(idx))
            spl.insertWidget(idx, new_spl)

            if hs == self._HS_SOUTH:
                idx = -1
            else:
                idx = 0

            spl = new_spl

        return (spl, idx)

    def _vertical_split(self, spl, idx, hs):
        """ Returns a tuple of the splitter and index where the new tab widget
        should be put.
        """

        if spl.orientation() == QtCore.Qt.Horizontal:
            if hs == self._HS_EAST:
                idx += 1
        elif spl is self and spl.count() == 1:
            # The splitter is the root and only has one child so we can just
            # change its orientation.
            spl.setOrientation(QtCore.Qt.Horizontal)

            if hs == self._HS_EAST:
                idx = -1
        else:
            new_spl = QtGui.QSplitter(QtCore.Qt.Horizontal)
            new_spl.addWidget(spl.widget(idx))
            spl.insertWidget(idx, new_spl)

            if hs == self._HS_EAST:
                idx = -1
            else:
                idx = 0

            spl = new_spl

        return (spl, idx)

    def _remove_tab(self, tab_w, tab):
        """ Remove a tab from a tab widget and return a tuple of the label text
        and the widget so that it can be recreated.
        """

        text = tab_w.tabText(tab)
        w = tab_w.widget(tab)
        tab_w.removeTab(tab)

        return (text, w)

    def _hotspot(self, pos):
        """ Return a tuple of the tab widget, hotspot and hostspot geometry (as
        a list) at the given position.
        """
        miss = (None, self._HS_NONE, None)

        # Handle the trivial case.
        if not self.geometry().contains(self.mapToParent(pos)):
            return miss

        # Go through each tab widget.
        for tw in self.findChildren(_TabWidget):
            if tw.geometry().contains(tw.parent().mapFrom(self, pos)):
                break
        else:
            return miss

        # See if the hotspot is in the widget area.
        widg = tw.currentWidget()

        if widg is not None:
            # Get the widget's position relative to its parent.
            wpos = widg.parent().mapFrom(self, pos)

            if widg.geometry().contains(wpos):
                # Get the position of the widget relative to itself (ie. the
                # top left corner is (0, 0)).
                p = widg.mapFromParent(wpos)
                x = p.x()
                y = p.y()
                h = widg.height()
                w = widg.width()

                # Get the global position of the widget.
                gpos = widg.mapToGlobal(widg.pos())
                gx = gpos.x()
                gy = gpos.y()

                # The corners of the widget belong to the north and south
                # sides.
                if y < h / 4:
                    return (tw, self._HS_NORTH, (gx, gy, w, h / 4))

                if y >= (3 * h) / 4:
                    return (tw, self._HS_SOUTH, (gx, gy + (3 * h) / 4, w, h / 4))

                if x < w / 4:
                    return (tw, self._HS_WEST, (gx, gy, w / 4, h))

                if x >= (3 * w) / 4:
                    return (tw, self._HS_EAST, (gx + (3 * w) / 4, gy, w / 4, h))

                return miss

        # See if the hotspot is in the tab area.
        tpos = tw.mapFrom(self, pos)
        tab_bar = tw.tabBar()
        top_bottom = tw.tabPosition() in (QtGui.QTabWidget.North, QtGui.QTabWidget.South)

        for i in range(tw.count()):
            rect = tab_bar.tabRect(i)

            if rect.contains(tpos):
                w = rect.width()
                h = rect.height()

                # Get the global position.
                gpos = tab_bar.mapToGlobal(rect.topLeft())
                gx = gpos.x()
                gy = gpos.y()

                if top_bottom:
                    off = pos.x() - rect.x()
                    ext = w
                    gx -= w / 2
                else:
                    off = pos.y() - rect.y()
                    ext = h
                    gy -= h / 2

                # See if it is in the left (or top) half or the right (or
                # bottom) half.
                if off < ext / 2:
                    return (tw, i, (gx, gy, w, h))

                if top_bottom:
                    gx += w
                else:
                    gy += h

                if i + 1 == tw.count():
                    return (tw, self._HS_AFTER_LAST_TAB, (gx, gy, w, h))

                return (tw, i + 1, (gx, gy, w, h))

        return miss

    def _tab_widget(self, w):
        """ Return the _TabWidget instance containing the given widget. """

        for tw in self.findChildren(_TabWidget):
            for i in range(tw.count()):
                if tw.widget(i) is w:
                    return tw

        return None


class _TabWidget(QtGui.QTabWidget):
    """ The _TabWidget class is a QTabWidget with a dragable tab bar. """

    def __init__(self, root, *args):
        """ Initialise the instance. """

        QtGui.QTabWidget.__init__(self, *args)

        self._root = root

        # We explicitly pass the parent to the tab bar ctor to work round a bug
        # in PyQt v4.2 and earlier.
        self.setTabBar(_DragableTabBar(self._root, self))

        # Add the button used to close the current tab.
        buttn = _TabCloseButton(self)
        self.connect(buttn, QtCore.SIGNAL('clicked()'), self._close_tab)
        self.setCornerWidget(buttn)

    def still_needed(self):
        """ Delete the tab widget (and any relevant parent splitters) if it is
        no longer needed.
        """

        if self.count() == 0:
            prune = self
            parent = prune.parent()

            # Go up the QSplitter hierarchy until we find one with at least one
            # sibling.
            while parent is not self._root and parent.count() == 1:
                prune = parent
                parent = prune.parent()

            prune.deleteLater()

    def _close_tab(self):
        """ Close the current tab. """

        # Orphan the widget.  Note that this might cause it to be garbage
        # collected if there is no other reference to it.
        # ZZZ: How do we feed this back to the workbench and what should we
        # really do with the widget?
        # ZZZ: Check the removeTab() ownership transfer is really working
        # properly.
        w = self.currentWidget()
        self.removeTab(self.currentIndex())
        w.setParent(None)

        self.still_needed()


class _TabCloseButton(QtGui.QAbstractButton):
    """ The _TabCloseButton class implements a button that is intended to close
    the current tab.  It uses the same pixmap as that used to draw the dock
    widget used for workbench views (in fact the code is based on the original
    C++ code that implements the same).
    """

    def __init__(self, *args):
        """ Initialise the instance. """

        QtGui.QAbstractButton.__init__(self, *args)

        self.setToolTip("Close current tab")
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Get the standard icon and compute the size.  We can do it once here
        # because the icon will never be changed.
        sty = self.style()

        icon = sty.standardIcon(QtGui.QStyle.SP_TitleBarCloseButton)
        pm = icon.pixmap(sty.pixelMetric(QtGui.QStyle.PM_SmallIconSize))

        size = max(pm.width(), pm.height())

        try:
            # This is Qt v4.3.0 and later.
            margin = sty.pixelMetric(QtGui.QStyle.PM_DockWidgetTitleBarButtonMargin)
        except AttributeError:
            margin = 2

        size += margin * 2

        # Pretend it is a little bigger to that we will have room to create a
        # small gap to the right and below.
        self._size_hint = QtCore.QSize(size + 1, size + 6)

        self.setIcon(icon)

    def minimumSizeHint(self):
        """ Reimplemented to return the minimum size. """

        return self._size_hint

    def sizeHint(self):
        """ Reimplemented to return the current size. """

        return self._size_hint

    def paintEvent(self, e):
        """ Reimplemented to paint the button. """

        p = QtGui.QPainter(self)
        r = self.rect()
        sty = self.style()

        opt = QtGui.QStyleOption()
        opt.initFrom(self)
        opt.state |= QtGui.QStyle.State_AutoRaise

        if self.isChecked():
            opt.state |= QtGui.QStyle.State_On
        elif self.isDown():
            opt.state |= QtGui.QStyle.State_Sunken
        elif self.isEnabled() and self.underMouse():
            opt.state |= QtGui.QStyle.State_Raised

        # Create the gaps.
        r.adjust(0, 0, -1, -6)
        opt.rect.adjust(0, 0, -1, -6)

        sty.drawPrimitive(QtGui.QStyle.PE_PanelButtonTool, opt, p, self)

        if opt.state & QtGui.QStyle.State_Sunken:
            hshift = sty.pixelMetric(QtGui.QStyle.PM_ButtonShiftHorizontal, opt, self)
            vshift = sty.pixelMetric(QtGui.QStyle.PM_ButtonShiftVertical, opt, self)

            r.translate(hshift, vshift)

        if self.isEnabled():
            if self.underMouse():
                mode = QtGui.QIcon.Active
            else:
                mode = QtGui.QIcon.Normal
        else:
            mode = QtGui.QIcon.Disabled

        if self.isDown():
            state = QtGui.QIcon.On
        else:
            state = QtGui.QIcon.Off

        pm = self.icon().pixmap(sty.pixelMetric(QtGui.QStyle.PM_SmallIconSize), mode, state)
        sty.drawItemPixmap(p, r, QtCore.Qt.AlignCenter, pm)


class _DragableTabBar(QtGui.QTabBar):
    """ The _DragableTabBar class is a QTabBar that can be dragged around. """

    def __init__(self, root, *args):
        """ Initialise the instance. """

        QtGui.QTabBar.__init__(self, *args)

        self._root = root
        self._drag_state = None

    def mousePressEvent(self, e):
        """ Reimplemented to handle mouse press events. """

        QtGui.QTabBar.mousePressEvent(self, e)

        if e.button() != QtCore.Qt.LeftButton:
            return

        if self._drag_state is not None:
            return

        tab = self._tab_at(e.pos())

        if tab < 0:
            return

        self._drag_state = _DragState(self._root, self, tab, e.pos())

    def mouseMoveEvent(self, e):
        """ Reimplemented to handle mouse move events. """

        QtGui.QTabBar.mouseMoveEvent(self, e)

        if self._drag_state is None:
            return

        if self._drag_state.dragging:
            self._drag_state.drag(e.pos())
        else:
            self._drag_state.start_dragging(e.pos())

    def mouseReleaseEvent(self, e):
        """ Reimplemented to handle mouse release events. """

        QtGui.QTabBar.mouseReleaseEvent(self, e)

        if e.button() != QtCore.Qt.LeftButton:
            return

        if self._drag_state is None:
            return

        if self._drag_state.dragging:
            self._drag_state.drop(e.pos())

        self._drag_state = None

    def _tab_at(self, pos):
        """ Return the index of the tab at the given point. """

        for i in range(self.count()):
            if self.tabRect(i).contains(pos):
                return i

        return -1


class _DragState(object):
    """ The _DragState class handles most of the work when dragging a tab. """

    def __init__(self, root, tab_bar, tab, start_pos):
        """ Initialise the instance. """

        self.dragging = False

        self._root = root
        self._tab_bar = tab_bar
        self._tab = tab
        self._start_pos = QtCore.QPoint(start_pos)
        self._clone = None

    def start_dragging(self, pos):
        """ Start dragging a tab. """

        if (pos - self._start_pos).manhattanLength() <= QtGui.QApplication.startDragDistance():
            return

        self.dragging = True

        # Create a clone of the tab being moved.
        otb = self._tab_bar
        tab = self._tab

        ctb = self._clone = QtGui.QTabBar()
        ctb.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                           QtCore.Qt.Tool |
                           QtCore.Qt.X11BypassWindowManagerHint)
        ctb.setWindowOpacity(0.5)
        ctb.setElideMode(otb.elideMode())
        ctb.setShape(otb.shape())

        ctb.addTab(otb.tabText(tab))
        ctb.setTabIcon(0, otb.tabIcon(tab))
        ctb.setTabTextColor(0, otb.tabTextColor(tab))

        # The offset is the position of the clone relative to the mouse.
        self._offset = otb.tabRect(tab).topLeft() - pos

        self.drag(pos)

        ctb.show()

    def drag(self, pos):
        """ Handle the movement of the cloned tab during dragging. """

        self._clone.move(self._tab_bar.mapToGlobal(pos) + self._offset)
        self._root.select(self._tab_bar.mapTo(self._root, pos))

    def drop(self, pos):
        """ Handle the drop of the cloned tab. """

        self.drag(pos)
        self._clone = None

        self._root.drop(self._tab_bar.parent(), self._tab)

        self.dragging = False
