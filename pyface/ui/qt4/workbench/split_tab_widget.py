# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2008 Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

# ------------------------------------------------------------------------------


import sys


from pyface.qt import QtCore, QtGui, qt_api

from pyface.image_resource import ImageResource


class SplitTabWidget(QtGui.QSplitter):
    """ The SplitTabWidget class is a hierarchy of QSplitters the leaves of
    which are QTabWidgets.  Any tab may be moved around with the hierarchy
    automatically extended and reduced as required.
    """

    # Signals for WorkbenchWindowLayout to handle
    new_window_request = QtCore.Signal(QtCore.QPoint, QtGui.QWidget)
    tab_close_request = QtCore.Signal(QtGui.QWidget)
    tab_window_changed = QtCore.Signal(QtGui.QWidget)
    editor_has_focus = QtCore.Signal(QtGui.QWidget)
    focus_changed = QtCore.Signal(QtGui.QWidget, QtGui.QWidget)

    # The different hotspots of a QTabWidget.  An non-negative value is a tab
    # index and the hotspot is to the left of it.

    tabTextChanged = QtCore.Signal(QtGui.QWidget, str)
    _HS_NONE = -1
    _HS_AFTER_LAST_TAB = -2
    _HS_NORTH = -3
    _HS_SOUTH = -4
    _HS_EAST = -5
    _HS_WEST = -6
    _HS_OUTSIDE = -7

    def __init__(self, *args):
        """ Initialise the instance. """

        QtGui.QSplitter.__init__(self, *args)

        self.clear()

        QtGui.QApplication.instance().focusChanged.connect(self._focus_changed)

    def clear(self):
        """ Restore the widget to its pristine state. """

        w = None
        for i in range(self.count()):
            w = self.widget(i)
            w.hide()
            w.deleteLater()
        del w

        self._repeat_focus_changes = True
        self._rband = None
        self._selected_tab_widget = None
        self._selected_hotspot = self._HS_NONE

        self._current_tab_w = None
        self._current_tab_idx = -1

    def saveState(self):
        """ Returns a Python object containing the saved state of the widget.
        Widgets are saved only by their object name.
        """

        return self._save_qsplitter(self)

    def _save_qsplitter(self, qsplitter):
        # A splitter state is a tuple of the QSplitter state (as a string) and
        # the list of child states.
        sp_ch_states = []

        # Save the children.
        for i in range(qsplitter.count()):
            ch = qsplitter.widget(i)

            if isinstance(ch, _TabWidget):
                # A tab widget state is a tuple of the current tab index and
                # the list of individual tab states.
                tab_states = []

                for t in range(ch.count()):
                    # A tab state is a tuple of the widget's object name and
                    # the title.
                    name = str(ch.widget(t).objectName())
                    title = str(ch.tabText(t))

                    tab_states.append((name, title))

                ch_state = (ch.currentIndex(), tab_states)
            else:
                # Recurse down the tree of splitters.
                ch_state = self._save_qsplitter(ch)

            sp_ch_states.append(ch_state)

        return (QtGui.QSplitter.saveState(qsplitter).data(), sp_ch_states)

    def restoreState(self, state, factory):
        """ Restore the contents from the given state (returned by a previous
        call to saveState()).  factory is a callable that is passed the object
        name of the widget that is in the state and needs to be restored.  The
        callable returns the restored widget.
        """

        # Ensure we are not restoring to a non-empty widget.
        assert self.count() == 0

        self._restore_qsplitter(state, factory, self)

    def _restore_qsplitter(self, state, factory, qsplitter):
        sp_qstate, sp_ch_states = state

        # Go through each child state which will consist of a tuple of two
        # objects.  We use the type of the first to determine if the child is a
        # tab widget or another splitter.
        for ch_state in sp_ch_states:
            if isinstance(ch_state[0], int):
                current_idx, tabs = ch_state

                new_tab = _TabWidget(self)

                # Go through each tab and use the factory to restore the page.
                for name, title in tabs:
                    page = factory(name)

                    if page is not None:
                        new_tab.addTab(page, title)

                # Only add the new tab widget if it is used.
                if new_tab.count() > 0:
                    qsplitter.addWidget(new_tab)

                    # Set the correct tab as the current one.
                    new_tab.setCurrentIndex(current_idx)
                else:
                    del new_tab
            else:
                new_qsp = QtGui.QSplitter()

                # Recurse down the tree of splitters.
                self._restore_qsplitter(ch_state, factory, new_qsp)

                # Only add the new splitter if it is used.
                if new_qsp.count() > 0:
                    qsplitter.addWidget(new_qsp)
                else:
                    del new_qsp

        # Restore the QSplitter state (being careful to get the right
        # implementation).
        QtGui.QSplitter.restoreState(qsplitter, sp_qstate)

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
            # There is no tab widget so create one.
            ch = _TabWidget(self)
            self.addWidget(ch)

        idx = ch.insertTab(self._current_tab_idx + 1, w, text)

        # If the tab has been added to the current tab widget then make it the
        # current tab.
        if ch is not self._current_tab_w:
            self._set_current_tab(ch, idx)
            ch.tabBar().setFocus()

    def _close_tab_request(self, w):
        """ A close button was clicked in one of out _TabWidgets """

        self.tab_close_request.emit(w)

    def setCurrentWidget(self, w):
        """ Make the given widget current. """

        tw, tidx = self._tab_widget(w)

        if tw is not None:
            self._set_current_tab(tw, tidx)

    def setActiveIcon(self, w, icon=None):
        """ Set the active icon on a widget. """

        tw, tidx = self._tab_widget(w)

        if tw is not None:
            if icon is None:
                icon = tw.active_icon()

            tw.setTabIcon(tidx, icon)

    def setTabTextColor(self, w, color=None):
        """ Set the tab text color on a particular widget w
        """
        tw, tidx = self._tab_widget(w)

        if tw is not None:
            if color is None:
                # null color reverts to foreground role color
                color = QtGui.QColor()
            tw.tabBar().setTabTextColor(tidx, color)

    def setWidgetTitle(self, w, title):
        """ Set the title for the given widget. """

        tw, idx = self._tab_widget(w)

        if tw is not None:
            tw.setTabText(idx, title)

    def _tab_widget(self, w):
        """ Return the tab widget and index containing the given widget. """

        for tw in self.findChildren(_TabWidget, None):
            idx = tw.indexOf(w)

            if idx >= 0:
                return (tw, idx)

        return (None, None)

    def _set_current_tab(self, tw, tidx):
        """ Set the new current tab. """

        # Handle the trivial case.
        if self._current_tab_w is tw and self._current_tab_idx == tidx:
            return

        if tw is not None:
            tw.setCurrentIndex(tidx)

        # Save the new current widget.
        self._current_tab_w = tw
        self._current_tab_idx = tidx

    def _set_focus(self):
        """ Set the focus to an appropriate widget in the current tab. """

        # Only try and change the focus if the current focus isn't already a
        # child of the widget.
        w = self._current_tab_w.widget(self._current_tab_idx)
        fw = self.window().focusWidget()

        if fw is not None and not w.isAncestorOf(fw):
            # Find a widget to focus using the same method as
            # QStackedLayout::setCurrentIndex().  First try the last widget
            # with the focus.
            nfw = w.focusWidget()

            if nfw is None:
                # Next, try the first child widget in the focus chain.
                nfw = fw.nextInFocusChain()

                while nfw is not fw:
                    if (
                        nfw.focusPolicy() & QtCore.Qt.FocusPolicy.TabFocus
                        and nfw.focusProxy() is None
                        and nfw.isVisibleTo(w)
                        and nfw.isEnabled()
                        and w.isAncestorOf(nfw)
                    ):
                        break

                    nfw = nfw.nextInFocusChain()
                else:
                    # Fallback to the tab page widget.
                    nfw = w

            nfw.setFocus()

    def _focus_changed(self, old, new):
        """ Handle a change in focus that affects the current tab. """

        # It is possible for the C++ layer of this object to be deleted between
        # the time when the focus change signal is emitted and time when the
        # slots are dispatched by the Qt event loop. This may be a bug in PyQt4.
        if qt_api == "pyqt":
            import sip

            if sip.isdeleted(self):
                return

        if self._repeat_focus_changes:
            self.focus_changed.emit(old, new)

        if new is None:
            return
        elif isinstance(new, _DragableTabBar):
            ntw = new.parent()
            ntidx = ntw.currentIndex()
        else:
            ntw, ntidx = self._tab_widget_of(new)

        if ntw is not None:
            self._set_current_tab(ntw, ntidx)

        # See if the widget that has lost the focus is ours.
        otw, _ = self._tab_widget_of(old)

        if otw is not None or ntw is not None:
            if ntw is None:
                nw = None
            else:
                nw = ntw.widget(ntidx)

            self.editor_has_focus.emit(nw)

    def _tab_widget_of(self, target):
        """ Return the tab widget and index of the widget that contains the
        given widget.
        """

        for tw in self.findChildren(_TabWidget, None):
            for tidx in range(tw.count()):
                w = tw.widget(tidx)

                if w is not None and w.isAncestorOf(target):
                    return (tw, tidx)

        return (None, None)

    def _move_left(self, tw, tidx):
        """ Move the current tab to the one logically to the left. """

        tidx -= 1

        if tidx < 0:
            # Find the tab widget logically to the left.
            twlist = self.findChildren(_TabWidget, None)
            i = twlist.index(tw)
            i -= 1

            if i < 0:
                i = len(twlist) - 1

            tw = twlist[i]

            # Move the to right most tab.
            tidx = tw.count() - 1

        self._set_current_tab(tw, tidx)
        tw.setFocus()

    def _move_right(self, tw, tidx):
        """ Move the current tab to the one logically to the right. """

        tidx += 1

        if tidx >= tw.count():
            # Find the tab widget logically to the right.
            twlist = self.findChildren(_TabWidget, None)
            i = twlist.index(tw)
            i += 1

            if i >= len(twlist):
                i = 0

            tw = twlist[i]

            # Move the to left most tab.
            tidx = 0

        self._set_current_tab(tw, tidx)
        tw.setFocus()

    def _select(self, pos):
        tw, hs, hs_geom = self._hotspot(pos)

        # See if the hotspot has changed.
        if self._selected_tab_widget is not tw or self._selected_hotspot != hs:
            if self._selected_tab_widget is not None:
                self._rband.hide()

            if tw is not None and hs != self._HS_NONE:
                if self._rband:
                    self._rband.deleteLater()
                position = QtCore.QPoint(*hs_geom[0:2])
                window = tw.window()
                self._rband = QtGui.QRubberBand(
                    QtGui.QRubberBand.Shape.Rectangle, window
                )
                self._rband.move(window.mapFromGlobal(position))
                self._rband.resize(*hs_geom[2:4])
                self._rband.show()

            self._selected_tab_widget = tw
            self._selected_hotspot = hs

    def _drop(self, pos, stab_w, stab):
        self._rband.hide()

        # Get the destination locations.
        dtab_w = self._selected_tab_widget
        dhs = self._selected_hotspot
        if dhs == self._HS_NONE:
            return
        elif dhs != self._HS_OUTSIDE:
            dsplit_w = dtab_w.parent()
            while not isinstance(dsplit_w, SplitTabWidget):
                dsplit_w = dsplit_w.parent()

        self._selected_tab_widget = None
        self._selected_hotspot = self._HS_NONE

        # See if the tab is being moved to a new window.
        if dhs == self._HS_OUTSIDE:
            # Disable tab tear-out for now. It works, but this is something that
            # should be turned on manually. We need an interface for this.
            # ticon, ttext, ttextcolor, tbuttn, twidg = self._remove_tab(stab_w, stab)
            # self.new_window_request.emit(pos, twidg)
            return

        # See if the tab is being moved to an existing tab widget.
        if dhs >= 0 or dhs == self._HS_AFTER_LAST_TAB:
            # Make sure it really is being moved.
            if stab_w is dtab_w:
                if stab == dhs:
                    return

                if (
                    dhs == self._HS_AFTER_LAST_TAB
                    and stab == stab_w.count() - 1
                ):
                    return

            QtGui.QApplication.instance().blockSignals(True)

            ticon, ttext, ttextcolor, tbuttn, twidg = self._remove_tab(
                stab_w, stab
            )

            if dhs == self._HS_AFTER_LAST_TAB:
                idx = dtab_w.addTab(twidg, ticon, ttext)
                dtab_w.tabBar().setTabTextColor(idx, ttextcolor)
            elif dtab_w is stab_w:
                # Adjust the index if necessary in case the removal of the tab
                # from its old position has skewed things.
                dst = dhs

                if dhs > stab:
                    dst -= 1

                idx = dtab_w.insertTab(dst, twidg, ticon, ttext)
                dtab_w.tabBar().setTabTextColor(idx, ttextcolor)
            else:
                idx = dtab_w.insertTab(dhs, twidg, ticon, ttext)
                dtab_w.tabBar().setTabTextColor(idx, ttextcolor)

            if tbuttn:
                dtab_w.show_button(idx)
            dsplit_w._set_current_tab(dtab_w, idx)

        else:
            # Ignore drops to the same tab widget when it only has one tab.
            if stab_w is dtab_w and stab_w.count() == 1:
                return

            QtGui.QApplication.instance().blockSignals(True)

            # Remove the tab from its current tab widget and create a new one
            # for it.
            ticon, ttext, ttextcolor, tbuttn, twidg = self._remove_tab(
                stab_w, stab
            )
            new_tw = _TabWidget(dsplit_w)
            idx = new_tw.addTab(twidg, ticon, ttext)
            new_tw.tabBar().setTabTextColor(0, ttextcolor)
            if tbuttn:
                new_tw.show_button(idx)

            # Get the splitter containing the destination tab widget.
            dspl = dtab_w.parent()
            dspl_idx = dspl.indexOf(dtab_w)

            if dhs in (self._HS_NORTH, self._HS_SOUTH):
                dspl, dspl_idx = dsplit_w._horizontal_split(
                    dspl, dspl_idx, dhs
                )
            else:
                dspl, dspl_idx = dsplit_w._vertical_split(dspl, dspl_idx, dhs)

            # Add the new tab widget in the right place.
            dspl.insertWidget(dspl_idx, new_tw)

            dsplit_w._set_current_tab(new_tw, 0)

        dsplit_w._set_focus()

        # Signal that the tab's SplitTabWidget has changed, if necessary.
        if dsplit_w != self:
            self.tab_window_changed.emit(twidg)

        QtGui.QApplication.instance().blockSignals(False)

    def _horizontal_split(self, spl, idx, hs):
        """ Returns a tuple of the splitter and index where the new tab widget
        should be put.
        """

        if spl.orientation() == QtCore.Qt.Orientation.Vertical:
            if hs == self._HS_SOUTH:
                idx += 1
        elif spl is self and spl.count() == 1:
            # The splitter is the root and only has one child so we can just
            # change its orientation.
            spl.setOrientation(QtCore.Qt.Orientation.Vertical)

            if hs == self._HS_SOUTH:
                idx = -1
        else:
            new_spl = QtGui.QSplitter(QtCore.Qt.Orientation.Vertical)
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

        if spl.orientation() == QtCore.Qt.Orientation.Horizontal:
            if hs == self._HS_EAST:
                idx += 1
        elif spl is self and spl.count() == 1:
            # The splitter is the root and only has one child so we can just
            # change its orientation.
            spl.setOrientation(QtCore.Qt.Orientation.Horizontal)

            if hs == self._HS_EAST:
                idx = -1
        else:
            new_spl = QtGui.QSplitter(QtCore.Qt.Orientation.Horizontal)
            new_spl.addWidget(spl.widget(idx))
            spl.insertWidget(idx, new_spl)

            if hs == self._HS_EAST:
                idx = -1
            else:
                idx = 0

            spl = new_spl

        return (spl, idx)

    def _remove_tab(self, tab_w, tab):
        """ Remove a tab from a tab widget and return a tuple of the icon,
        label text and the widget so that it can be recreated.
        """

        icon = tab_w.tabIcon(tab)
        text = tab_w.tabText(tab)
        text_color = tab_w.tabBar().tabTextColor(tab)
        button = tab_w.tabBar().tabButton(tab, QtGui.QTabBar.ButtonPosition.LeftSide)
        w = tab_w.widget(tab)
        tab_w.removeTab(tab)

        return (icon, text, text_color, button, w)

    def _hotspot(self, pos):
        """ Return a tuple of the tab widget, hotspot and hostspot geometry (as
        a tuple) at the given position.
        """
        global_pos = self.mapToGlobal(pos)
        miss = (None, self._HS_NONE, None)

        # Get the bounding rect of the cloned QTbarBar.
        top_widget = QtGui.QApplication.instance().topLevelAt(global_pos)
        if isinstance(top_widget, QtGui.QTabBar):
            cloned_rect = top_widget.frameGeometry()
        else:
            cloned_rect = None

        # Determine which visible SplitTabWidget, if any, is under the cursor
        # (compensating for the cloned QTabBar that may be rendered over it).
        split_widget = None
        for top_widget in QtGui.QApplication.instance().topLevelWidgets():
            for split_widget in top_widget.findChildren(SplitTabWidget, None):
                visible_region = split_widget.visibleRegion()
                widget_pos = split_widget.mapFromGlobal(global_pos)
                if cloned_rect and split_widget.geometry().contains(
                    widget_pos
                ):
                    visible_rect = visible_region.boundingRect()
                    widget_rect = QtCore.QRect(
                        split_widget.mapFromGlobal(cloned_rect.topLeft()),
                        split_widget.mapFromGlobal(cloned_rect.bottomRight()),
                    )
                    if not visible_rect.intersected(widget_rect).isEmpty():
                        break
                elif visible_region.contains(widget_pos):
                    break
            else:
                split_widget = None
            if split_widget:
                break

        # Handle a drag outside of any split tab widget.
        if not split_widget:
            if self.window().frameGeometry().contains(global_pos):
                return miss
            else:
                return (None, self._HS_OUTSIDE, None)

        # Go through each tab widget.
        pos = split_widget.mapFromGlobal(global_pos)
        for tw in split_widget.findChildren(_TabWidget, None):
            if tw.geometry().contains(tw.parent().mapFrom(split_widget, pos)):
                break
        else:
            return miss

        # See if the hotspot is in the widget area.
        widg = tw.currentWidget()
        if widg is not None:

            # Get the widget's position relative to its parent.
            wpos = widg.parent().mapFrom(split_widget, pos)

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
                    return (
                        tw,
                        self._HS_SOUTH,
                        (gx, gy + (3 * h) / 4, w, h / 4),
                    )

                if x < w / 4:
                    return (tw, self._HS_WEST, (gx, gy, w / 4, h))

                if x >= (3 * w) / 4:
                    return (
                        tw,
                        self._HS_EAST,
                        (gx + (3 * w) / 4, gy, w / 4, h),
                    )

                return miss

        # See if the hotspot is in the tab area.
        tpos = tw.mapFrom(split_widget, pos)
        tab_bar = tw.tabBar()
        top_bottom = tw.tabPosition() in (
            QtGui.QTabWidget.TabPosition.North,
            QtGui.QTabWidget.TabPosition.South,
        )
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
        else:
            rect = tab_bar.rect()
            if rect.contains(tpos):
                gpos = tab_bar.mapToGlobal(rect.topLeft())
                gx = gpos.x()
                gy = gpos.y()
                w = rect.width()
                h = rect.height()
                if top_bottom:
                    tab_widths = sum(
                        tab_bar.tabRect(i).width()
                        for i in range(tab_bar.count())
                    )
                    w -= tab_widths
                    gx += tab_widths
                else:
                    tab_heights = sum(
                        tab_bar.tabRect(i).height()
                        for i in range(tab_bar.count())
                    )
                    h -= tab_heights
                    gy -= tab_heights
                return (tw, self._HS_AFTER_LAST_TAB, (gx, gy, w, h))

        return miss


active_style = """QTabWidget::pane { /* The tab widget frame */
     border: 2px solid #00FF00;
 }
"""
inactive_style = """QTabWidget::pane { /* The tab widget frame */
     border: 2px solid #C2C7CB;
     margin: 0px;
 }
"""


class _TabWidget(QtGui.QTabWidget):
    """ The _TabWidget class is a QTabWidget with a dragable tab bar. """

    # The active icon.  It is created when it is first needed.
    _active_icon = None

    _spinner_data = None

    def __init__(self, root, *args):
        """ Initialise the instance. """

        QtGui.QTabWidget.__init__(self, *args)

        # XXX this requires Qt > 4.5
        if sys.platform == "darwin":
            self.setDocumentMode(True)
        # self.setStyleSheet(inactive_style)

        self._root = root

        # We explicitly pass the parent to the tab bar ctor to work round a bug
        # in PyQt v4.2 and earlier.
        self.setTabBar(_DragableTabBar(self._root, self))

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self._close_tab)

        if not (_TabWidget._spinner_data):
            _TabWidget._spinner_data = ImageResource("spinner.gif")

    def show_button(self, index):
        lbl = QtGui.QLabel(self)
        movie = QtGui.QMovie(
            _TabWidget._spinner_data.absolute_path, parent=lbl
        )
        movie.setCacheMode(QtGui.QMovie.CacheMode.CacheAll)
        movie.setScaledSize(QtCore.QSize(16, 16))
        lbl.setMovie(movie)
        movie.start()
        self.tabBar().setTabButton(index, QtGui.QTabBar.ButtonPosition.LeftSide, lbl)

    def hide_button(self, index):
        curr = self.tabBar().tabButton(index, QtGui.QTabBar.ButtonPosition.LeftSide)
        if curr:
            curr.close()
            self.tabBar().setTabButton(index, QtGui.QTabBar.ButtonPosition.LeftSide, None)

    def active_icon(self):
        """ Return the QIcon to be used to indicate an active tab page. """

        if _TabWidget._active_icon is None:
            # The gradient start and stop colours.
            start = QtGui.QColor(0, 255, 0)
            stop = QtGui.QColor(0, 63, 0)

            size = self.iconSize()
            width = size.width()
            height = size.height()

            pm = QtGui.QPixmap(size)

            p = QtGui.QPainter()
            p.begin(pm)

            # Fill the image background from the tab background.
            p.initFrom(self.tabBar())
            p.fillRect(0, 0, width, height, p.background())

            # Create the colour gradient.
            rg = QtGui.QRadialGradient(width / 2, height / 2, width)
            rg.setColorAt(0.0, start)
            rg.setColorAt(1.0, stop)

            # Draw the circle.
            p.setBrush(rg)
            p.setPen(QtCore.Qt.PenStyle.NoPen)
            p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            p.drawEllipse(0, 0, width, height)

            p.end()

            _TabWidget._active_icon = QtGui.QIcon(pm)

        return _TabWidget._active_icon

    def _still_needed(self):
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

            prune.hide()
            prune.deleteLater()

    def tabRemoved(self, idx):
        """ Reimplemented to update the record of the current tab if it is
        removed.
        """

        self._still_needed()

        if (
            self._root._current_tab_w is self
            and self._root._current_tab_idx == idx
        ):
            self._root._current_tab_w = None

    def _close_tab(self, index):
        """ Close the current tab. """

        self._root._close_tab_request(self.widget(index))


class _IndependentLineEdit(QtGui.QLineEdit):
    def keyPressEvent(self, e):
        QtGui.QLineEdit.keyPressEvent(self, e)
        if e.key() == QtCore.Qt.Key.Key_Escape:
            self.hide()


class _DragableTabBar(QtGui.QTabBar):
    """ The _DragableTabBar class is a QTabBar that can be dragged around. """

    def __init__(self, root, parent):
        """ Initialise the instance. """

        QtGui.QTabBar.__init__(self, parent)

        # XXX this requires Qt > 4.5
        if sys.platform == "darwin":
            self.setDocumentMode(True)

        self._root = root
        self._drag_state = None
        # LineEdit to change tab bar title
        te = _IndependentLineEdit("", self)
        te.hide()
        te.editingFinished.connect(te.hide)
        te.returnPressed.connect(self._setCurrentTabText)
        self._title_edit = te

    def resizeEvent(self, e):
        # resize edit tab
        if self._title_edit.isVisible():
            self._resize_title_edit_to_current_tab()
        QtGui.QTabBar.resizeEvent(self, e)

    def keyPressEvent(self, e):
        """ Reimplemented to handle traversal across different tab widgets. """

        if e.key() == QtCore.Qt.Key.Key_Left:
            self._root._move_left(self.parent(), self.currentIndex())
        elif e.key() == QtCore.Qt.Key.Key_Right:
            self._root._move_right(self.parent(), self.currentIndex())
        else:
            e.ignore()

    def mouseDoubleClickEvent(self, e):
        self._resize_title_edit_to_current_tab()
        te = self._title_edit
        te.setText(self.tabText(self.currentIndex())[1:])
        te.setFocus()
        te.selectAll()
        te.show()

    def mousePressEvent(self, e):
        """ Reimplemented to handle mouse press events. """

        # There is something odd in the focus handling where focus temporarily
        # moves elsewhere (actually to a View) when switching to a different
        # tab page.  We suppress the notification so that the workbench doesn't
        # temporarily make the View active.
        self._root._repeat_focus_changes = False
        QtGui.QTabBar.mousePressEvent(self, e)
        self._root._repeat_focus_changes = True

        # Update the current tab.
        self._root._set_current_tab(self.parent(), self.currentIndex())
        self._root._set_focus()

        if e.button() != QtCore.Qt.MouseButton.LeftButton:
            return

        if self._drag_state is not None:
            return

        # Potentially start dragging if the tab under the mouse is the current
        # one (which will eliminate disabled tabs).
        tab = self._tab_at(e.pos())

        if tab < 0 or tab != self.currentIndex():
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

            # If the mouse has moved far enough that dragging has started then
            # tell the user.
            if self._drag_state.dragging:
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.OpenHandCursor)

    def mouseReleaseEvent(self, e):
        """ Reimplemented to handle mouse release events. """

        QtGui.QTabBar.mouseReleaseEvent(self, e)

        if e.button() != QtCore.Qt.MouseButton.LeftButton:
            if e.button() == QtCore.Qt.MidddleButton:
                self.tabCloseRequested.emit(self.tabAt(e.pos()))
            return

        if self._drag_state is not None and self._drag_state.dragging:
            QtGui.QApplication.restoreOverrideCursor()
            self._drag_state.drop(e.pos())

        self._drag_state = None

    def _tab_at(self, pos):
        """ Return the index of the tab at the given point. """

        for i in range(self.count()):
            if self.tabRect(i).contains(pos):
                return i

        return -1

    def _setCurrentTabText(self):
        idx = self.currentIndex()
        text = self._title_edit.text()
        self.setTabText(idx, "\u25b6" + text)
        self._root.tabTextChanged.emit(self.parent().widget(idx), text)

    def _resize_title_edit_to_current_tab(self):
        idx = self.currentIndex()
        tab = QtGui.QStyleOptionTabV3()
        self.initStyleOption(tab, idx)
        rect = self.style().subElementRect(QtGui.QStyle.SubElement.SE_TabBarTabText, tab)
        self._title_edit.setGeometry(rect.adjusted(0, 8, 0, -8))


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

        if (
            pos - self._start_pos
        ).manhattanLength() <= QtGui.QApplication.startDragDistance():
            return

        self.dragging = True

        # Create a clone of the tab being moved (except for its icon).
        otb = self._tab_bar
        tab = self._tab

        ctb = self._clone = QtGui.QTabBar()
        if sys.platform == "darwin" and QtCore.QT_VERSION >= 0x40500:
            ctb.setDocumentMode(True)

        ctb.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        ctb.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        ctb.setWindowOpacity(0.5)
        ctb.setElideMode(otb.elideMode())
        ctb.setShape(otb.shape())

        ctb.addTab(otb.tabText(tab))
        ctb.setTabTextColor(0, otb.tabTextColor(tab))

        # The clone offset is the position of the clone relative to the mouse.
        trect = otb.tabRect(tab)
        self._clone_offset = trect.topLeft() - pos

        # The centre offset is the position of the center of the clone relative
        # to the mouse.  The center of the clone determines the hotspot, not
        # the position of the mouse.
        self._centre_offset = trect.center() - pos

        self.drag(pos)

        ctb.show()

    def drag(self, pos):
        """ Handle the movement of the cloned tab during dragging. """

        self._clone.move(self._tab_bar.mapToGlobal(pos) + self._clone_offset)
        self._root._select(
            self._tab_bar.mapTo(self._root, pos + self._centre_offset)
        )

    def drop(self, pos):
        """ Handle the drop of the cloned tab. """

        self.drag(pos)
        self._clone = None

        global_pos = self._tab_bar.mapToGlobal(pos)
        self._root._drop(global_pos, self._tab_bar.parent(), self._tab)

        self.dragging = False
