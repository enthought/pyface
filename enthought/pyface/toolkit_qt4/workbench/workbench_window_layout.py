#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major library imports.
from PyQt4 import QtCore, QtGui

# Local imports.
from split_tab_widget import SplitTabWidget


# For mapping positions relative to the editor area.
EDIT_AREA_MAP = {
    'left':     QtCore.Qt.LeftDockWidgetArea,
    'right':    QtCore.Qt.RightDockWidgetArea,
    'top':      QtCore.Qt.TopDockWidgetArea,
    'bottom':   QtCore.Qt.BottomDockWidgetArea
}

# For mapping positions relative to another view.
VIEW_AREA_MAP = {
    'left':     (QtCore.Qt.Horizontal, True),
    'right':    (QtCore.Qt.Horizontal, False),
    'top':      (QtCore.Qt.Vertical, True),
    'bottom':   (QtCore.Qt.Vertical, False)
}


class WorkbenchWindowLayout_qt4(object):
    """ The WorkbenchWindowLayout monkey patch for Qt4. """

    ###########################################################################
    # 'WorkbenchWindowLayout' toolkit interface.
    ###########################################################################

    def _tk_workbenchwindowlayout_activate_editor(self, editor):
        """ Activates an editor. """

        if editor.control is not None:
            self._qt4_activate_editor(editor.control)

    def _tk_workbenchwindowlayout_activate_view(self, view):
        """ Activates a view. """

        # ZZZ: This probably doesn't work as expected.
        view.control.raise_()

    def _tk_workbenchwindowlayout_add_editor(self, editor, title):
        """ Adds an editor. """

        # Create the editor control if it hasn't already been done.
        # ZZZ: We need to handle editor_closing and editor_closed as well.
        if editor.control is None:
            self.editor_opening = editor
            editor.control = editor.create_control(None)
            self.editor_opened = editor

        self._qt4_monitor_focus(editor.control)

        self.window.control.centralWidget().addTab(editor.control, title)

    def _tk_workbenchwindowlayout_add_view(self, view, position, relative_to=None, size=(-1, -1)):
        """ Adds a view. """

        dw = self._qt4_create_view_dock_widget(view)
        mw = self.window.control

        self._qt4_monitor_focus(view.control)

        try:
            rel_dw = relative_to._qt4_dock
        except AttributeError:
            rel_dw = None

        if rel_dw is None:
            # Position the view relative to the editor area.
            try:
                dwa = EDIT_AREA_MAP[position]
            except KeyError:
                raise ValueError, "unknown view position: %s" % position

            mw.addDockWidget(dwa, dw)
        elif position == 'with':
            # ZZZ: The Qt documentation says that the second should be placed
            # above the first, but it always seems to be underneath (ie.
            # hidden) which is not what the user is expecting.
            mw.tabifyDockWidget(rel_dw, dw)
        else:
            try:
                orient, swap = VIEW_AREA_MAP[position]
            except KeyError:
                raise ValueError, "unknown view position: %s" % position

            mw.splitDockWidget(rel_dw, dw, orient)

            # The Qt documentation implies that the layout direction can be
            # used to position the new dock widget relative to the existing one
            # but I could only get the button positions to change.  Instead we
            # move things around afterwards if required.
            if swap:
                mw.removeDockWidget(rel_dw)
                mw.splitDockWidget(dw, rel_dw, orient)
                rel_dw.show()

    def _tk_workbenchwindowlayout_close_editor(self, editor):
        """ Closes an editor. """

        if editor.control is None:
            return

        eds = self.window.control.centralWidget()
        idx = eds.indexOf(editor.control)

        if idx < 0:
            return

        eds.removeTab(idx)

        # ZZZ: Are we also supposed to delete the editor?
        editor.control.setParent(self.window.control)

    def _tk_workbenchwindowlayout_close(self):
        """ Closes the entire window layout. """

        mw = self.window.control

        # ZZZ: On application shutdown this is None - need to understand why.
        if mw is None:
            return

        # Handle the editors.
        for e in self.window.editors:
            self._tk_workbenchwindowlayout_close_editor(e)

        # Delete the editor area if there is one.
        cw = mw.centralWidget()

        if cw is not None:
            cw.deleteLater()

        # Delete all dock widgets.
        # ZZZ: Are we also supposed to delete the views?
        for v in self.window.views:
            if self._tk_workbenchwindowlayout_contains_view(v):
                self._qt4_delete_view_dock_widget(v)

    def _tk_workbenchwindowlayout_create(self):
        """ Creates the initial window layout. """

        self.window.control.setCentralWidget(SplitTabWidget())

    def _tk_workbenchwindowlayout_contains_view(self, view):
        """ Returns True if the view exists in the window layout. """

        return hasattr(view, '_qt4_dock')

    def _tk_workbenchwindowlayout_refresh(self):
        """ Refreshes the window layout to reflect any changes. """

        # Nothing to do.
        pass

    def _tk_workbenchwindowlayout_reset_editors(self):
        """ Activates the first editor. """

        self.window.control.centralWidget().setCurrentIndex(0)

    def _tk_workbenchwindowlayout_reset_views(self):
        """ Activates the first view in every region. """

        # Qt doesn't provide information about the order of dock widgets in a
        # dock area.
        pass

    def _tk_workbenchwindowlayout_set_editor_area_visible(self, visible):
        """ Sets the editor area visibility. """

        eds = self.window.control.centralWidget()

        if eds is not None:
            eds.setVisible(visible)

    def _tk_workbenchwindowlayout_set_view_visible(self, view, visible):
        """ Sets a view's visibility. """

        view._qt4_dock.setVisible(visible)

    def _tk_workbenchwindowlayout_get_view_memento(self):
        """ Returns the state of the views. """

        # Get the IDs of the views in the main window.  This information is
        # also in the QMainWindow state, but that is opaque.
        view_ids = [v.id for v in self.window.views if self._tk_workbenchwindowlayout_contains_view(v)]

        # Everything else is provided by QMainWindow.
        state = str(self.window.control.saveState())

        return (view_ids, state)

    def _tk_workbenchwindowlayout_set_view_memento(self, memento):
        """ Restores the state of the views. """

        view_ids, state = memento

        # Get a list of all views that have dock widgets and mark them.
        dock_views = [v for v in self.window.views if self._tk_workbenchwindowlayout_contains_view(v)]

        for v in dock_views:
            v._qt4_gone = True

        # Create a dock window for all views that had one last time.
        for v in self.window.views:
            # Make sure this is in a know state.
            v.visible = False

            for vid in view_ids:
                if vid == v.id:
                    # Create the dock widget if needed and make sure that it is
                    # invisible so that it matches the state of the visible
                    # trait.  Things will all come right when the main window
                    # state is restored below.
                    self._qt4_create_view_dock_widget(v).setVisible(False)

                    if v in dock_views:
                        delattr(v, '_qt4_gone')

                    break

        # Remove any remain unused dock widgets.
        for v in dock_views:
            try:
                delattr(v, '_qt4_gone')
            except AttributeError:
                pass
            else:
                self._qt4_delete_view_dock_widget(v)

        # Restore the state.  This will update the view's visible trait through
        # the dock window's toggle action.
        self.window.control.restoreState(state)

    def _tk_workbenchwindowlayout_get_editor_memento(self):
        """ Returns the state of the editors. """

        # ZZZ: TODO (when it is decided how the editor area is going to be
        # handled)
        return None

    def _tk_workbenchwindowlayout_set_editor_memento(self, memento):
        """ Restores the state of the editors. """

        # ZZZ: TODO (when it is decided how the editor area is going to be
        # handled)
        pass

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _qt4_create_view_dock_widget(self, view):
        """ Create a dock widget that wraps a view. """

        # See if it has already been created.
        try:
            dw = view._qt4_dock
        except AttributeError:
            dw = QtGui.QDockWidget(view.name, self.window.control)
            dw.setObjectName(view.id)
            dw.connect(dw.toggleViewAction(), QtCore.SIGNAL('toggled(bool)'),
                    self._qt4_handle_dock_visibility)

            # Save the dock window.
            view._qt4_dock = dw

        # Make sure the view control exists.
        if view.control is None:
            # Make sure that the view knows which window it is in.
            view.window = self.window

            try:
                view.control = view.create_control(self.window.control)
            except:
                # Tidy up if the view couldn't be created.
                delattr(view, '_qt4_dock')
                dw.deleteLater()
                raise

        dw.setWidget(view.control)

        return dw

    def _qt4_handle_dock_visibility(self, checked):
        """ Handle the visibility of a dock window changing. """

        # Find the dock window by its toggle action.
        for v in self.window.views:
            try:
                dw = v._qt4_dock
            except AttributeError:
                continue

            if dw.toggleViewAction() is dw.sender():
                v.visible = checked

    def _qt4_delete_view_dock_widget(self, view):
        """ Delete a view's dock widget. """

        dw = view._qt4_dock

        # Remove the view first and reparent it so that it doesn't get deleted.
        dw.setWidget(None)
        view.control.setParent(self.window.control)

        # Don't use deleteLater() because we want it to go now in case we are
        # about to restore the main window state.
        dw.setParent(None)
        delattr(view, '_qt4_dock')

    def _qt4_activate_editor(self, control):
        """ Activate an editor control. """

        control.show()
        self.window.control.centralWidget().setCurrentWidget(control)

    def _qt4_monitor_focus(self, control):
        """ Install an event filter for a view or editor control to allow the
        has_focus traits to be maintained.
        """

        # Create the monitoring object if needed.
        try:
            mon = self._qt4_monitor
        except AttributeError:
            mon = self._qt4_monitor = _Monitor(self.window)

        control.installEventFilter(mon)


class _Monitor(QtCore.QObject):
    """ This class monitors a view or editor control and updates their
    has_focus traits accordingly.
    """

    def __init__(self, window):
        """ Initialise the instance. """

        QtCore.QObject.__init__(self, window.control)

        self._window = window

    def eventFilter(self, obj, e):
        """ Inspect any focus events. """

        if isinstance(e, QtGui.QFocusEvent) and e.reason() != QtCore.Qt.PopupFocusReason:
            for editor in self._window.editors:
                if editor.control is obj:
                    editor.has_focus = e.gotFocus()
                    break
            else:
                for view in self._window.views:
                    if view.control is obj:
                        view.has_focus = e.gotFocus()
                        break

        return False
