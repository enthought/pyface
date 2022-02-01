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


import logging


from pyface.qt import QtCore, QtGui


from traits.api import Instance, observe


from pyface.message_dialog import error
from pyface.workbench.i_workbench_window_layout import MWorkbenchWindowLayout
from .split_tab_widget import SplitTabWidget


# Logging.
logger = logging.getLogger(__name__)


# For mapping positions relative to the editor area.
_EDIT_AREA_MAP = {
    "left": QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
    "right": QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
    "top": QtCore.Qt.DockWidgetArea.TopDockWidgetArea,
    "bottom": QtCore.Qt.DockWidgetArea.BottomDockWidgetArea,
}

# For mapping positions relative to another view.
_VIEW_AREA_MAP = {
    "left": (QtCore.Qt.Orientation.Horizontal, True),
    "right": (QtCore.Qt.Orientation.Horizontal, False),
    "top": (QtCore.Qt.Orientation.Vertical, True),
    "bottom": (QtCore.Qt.Orientation.Vertical, False),
}


class WorkbenchWindowLayout(MWorkbenchWindowLayout):
    """ The Qt4 implementation of the workbench window layout interface.

    See the 'IWorkbenchWindowLayout' interface for the API documentation.

    """

    # Private interface ----------------------------------------------------

    # The widget that provides the editor area.  We keep (and use) this
    # separate reference because we can't always assume that it has been set to
    # be the main window's central widget.
    _qt4_editor_area = Instance(SplitTabWidget)

    # ------------------------------------------------------------------------
    # 'IWorkbenchWindowLayout' interface.
    # ------------------------------------------------------------------------

    def activate_editor(self, editor):
        if editor.control is not None:
            editor.control.show()
            self._qt4_editor_area.setCurrentWidget(editor.control)
            editor.set_focus()

        return editor

    def activate_view(self, view):
        # FIXME v3: This probably doesn't work as expected.
        view.control.raise_()
        view.set_focus()

        return view

    def add_editor(self, editor, title):
        if editor is None:
            return None

        try:
            self._qt4_editor_area.addTab(
                self._qt4_get_editor_control(editor), title
            )

            if editor._loading_on_open:
                self._qt4_editor_tab_spinner(editor, "", True)
        except Exception:
            logger.exception("error creating editor control [%s]", editor.id)

        return editor

    def add_view(self, view, position=None, relative_to=None, size=(-1, -1)):
        if view is None:
            return None

        try:
            self._qt4_add_view(view, position, relative_to, size)
            view.visible = True
        except Exception:
            logger.exception("error creating view control [%s]", view.id)

            # Even though we caught the exception, it sometimes happens that
            # the view's control has been created as a child of the application
            # window (or maybe even the dock control).  We should destroy the
            # control to avoid bad UI effects.
            view.destroy_control()

            # Additionally, display an error message to the user.
            error(
                self.window.control,
                "Unable to add view [%s]" % view.id,
                "Workbench Plugin Error",
            )

        return view

    def close_editor(self, editor):
        if editor.control is not None:
            editor.control.close()

        return editor

    def close_view(self, view):
        self.hide_view(view)

        return view

    def close(self):
        # Don't fire signals for editors that have destroyed their controls.
        self._qt4_editor_area.editor_has_focus.disconnect(
            self._qt4_editor_focus
        )

        self._qt4_editor_area.clear()

        # Delete all dock widgets.
        for v in self.window.views:
            if self.contains_view(v):
                self._qt4_delete_view_dock_widget(v)

    def create_initial_layout(self, parent):
        self._qt4_editor_area = editor_area = SplitTabWidget(parent)

        editor_area.editor_has_focus.connect(self._qt4_editor_focus)

        # We are interested in focus changes but we get them from the editor
        # area rather than qApp to allow the editor area to restrict them when
        # needed.
        editor_area.focus_changed.connect(self._qt4_view_focus_changed)

        editor_area.tabTextChanged.connect(self._qt4_editor_title_changed)
        editor_area.new_window_request.connect(self._qt4_new_window_request)
        editor_area.tab_close_request.connect(self._qt4_tab_close_request)
        editor_area.tab_window_changed.connect(self._qt4_tab_window_changed)

        return editor_area

    def contains_view(self, view):
        return hasattr(view, "_qt4_dock")

    def hide_editor_area(self):
        self._qt4_editor_area.hide()

    def hide_view(self, view):
        view._qt4_dock.hide()
        view.visible = False

        return view

    def refresh(self):
        # Nothing to do.
        pass

    def reset_editors(self):
        self._qt4_editor_area.setCurrentIndex(0)

    def reset_views(self):
        # Qt doesn't provide information about the order of dock widgets in a
        # dock area.
        pass

    def show_editor_area(self):
        self._qt4_editor_area.show()

    def show_view(self, view):
        view._qt4_dock.show()
        view.visible = True

    # Methods for saving and restoring the layout -------------------------#

    def get_view_memento(self):
        # Get the IDs of the views in the main window.  This information is
        # also in the QMainWindow state, but that is opaque.
        view_ids = [v.id for v in self.window.views if self.contains_view(v)]

        # Everything else is provided by QMainWindow.
        state = self.window.control.saveState()

        return (0, (view_ids, state))

    def set_view_memento(self, memento):
        version, mdata = memento

        # There has only ever been version 0 so far so check with an assert.
        assert version == 0

        # Now we know the structure of the memento we can "parse" it.
        view_ids, state = mdata

        # Get a list of all views that have dock widgets and mark them.
        dock_views = [v for v in self.window.views if self.contains_view(v)]

        for v in dock_views:
            v._qt4_gone = True

        # Create a dock window for all views that had one last time.
        for v in self.window.views:
            # Make sure this is in a known state.
            v.visible = False

            for vid in view_ids:
                if vid == v.id:
                    # Create the dock widget if needed and make sure that it is
                    # invisible so that it matches the state of the visible
                    # trait.  Things will all come right when the main window
                    # state is restored below.
                    self._qt4_create_view_dock_widget(v).setVisible(False)

                    if v in dock_views:
                        delattr(v, "_qt4_gone")

                    break

        # Remove any remain unused dock widgets.
        for v in dock_views:
            try:
                delattr(v, "_qt4_gone")
            except AttributeError:
                pass
            else:
                self._qt4_delete_view_dock_widget(v)

        # Restore the state.  This will update the view's visible trait through
        # the dock window's toggle action.
        self.window.control.restoreState(state)

    def get_editor_memento(self):
        # Get the layout of the editors.
        editor_layout = self._qt4_editor_area.saveState()

        # Get a memento for each editor that describes its contents.
        editor_references = self._get_editor_references()

        return (0, (editor_layout, editor_references))

    def set_editor_memento(self, memento):
        version, mdata = memento

        # There has only ever been version 0 so far so check with an assert.
        assert version == 0

        # Now we know the structure of the memento we can "parse" it.
        editor_layout, editor_references = mdata

        def resolve_id(id):
            # Get the memento for the editor contents (if any).
            editor_memento = editor_references.get(id)

            if editor_memento is None:
                return None

            # Create the restored editor.
            editor = self.window.editor_manager.set_editor_memento(
                editor_memento
            )
            if editor is None:
                return None

            # Save the editor.
            self.window.editors.append(editor)

            # Create the control if needed and return it.
            return self._qt4_get_editor_control(editor)

        self._qt4_editor_area.restoreState(editor_layout, resolve_id)

    def get_toolkit_memento(self):
        return (0, {"geometry": self.window.control.saveGeometry()})

    def set_toolkit_memento(self, memento):
        if hasattr(memento, "toolkit_data"):
            data = memento.toolkit_data
            if isinstance(data, tuple) and len(data) == 2:
                version, datadict = data
                if version == 0:
                    geometry = datadict.pop("geometry", None)
                    if geometry is not None:
                        self.window.control.restoreGeometry(geometry)

    def is_editor_area_visible(self):
        return self._qt4_editor_area.isVisible()

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _qt4_editor_focus(self, new):
        """ Handle an editor getting the focus. """

        for editor in self.window.editors:
            control = editor.control
            editor.has_focus = control is new or (
                control is not None and new in control.children()
            )

    def _qt4_editor_title_changed(self, control, title):
        """ Handle the title being changed """
        for editor in self.window.editors:
            if editor.control == control:
                editor.name = str(title)

    def _qt4_editor_tab_spinner(self, event):
        editor = event.object

        # Do we need to do this verification?
        tw, tidx = self._qt4_editor_area._tab_widget(editor.control)

        if event.new:
            tw.show_button(tidx)
        else:
            tw.hide_button(tidx)

        if not event.new and not editor == self.window.active_editor:
            self._qt4_editor_area.setTabTextColor(
                editor.control, QtCore.Qt.GlobalColor.red
            )

    @observe("window:active_editor")
    def _qt4_active_editor_changed(self, event):
        """ Handle change of active editor """
        # Reset tab title to foreground color
        editor = event.new
        if editor is not None:
            self._qt4_editor_area.setTabTextColor(editor.control)

    def _qt4_view_focus_changed(self, old, new):
        """ Handle the change of focus for a view. """

        focus_part = None

        if new is not None:
            # Handle focus changes to views.
            for view in self.window.views:
                if view.control is not None and view.control.isAncestorOf(new):
                    view.has_focus = True
                    focus_part = view
                    break

        if old is not None:
            # Handle focus changes from views.
            for view in self.window.views:
                if (
                    view is not focus_part
                    and view.control is not None
                    and view.control.isAncestorOf(old)
                ):
                    view.has_focus = False
                    break

    def _qt4_new_window_request(self, pos, control):
        """ Handle a tab tear-out request from the splitter widget. """

        editor = self._qt4_remove_editor_with_control(control)
        kind = self.window.editor_manager.get_editor_kind(editor)

        window = self.window.workbench.create_window()
        window.open()
        window.add_editor(editor)
        window.editor_manager.add_editor(editor, kind)
        window.position = (pos.x(), pos.y())
        window.size = self.window.size
        window.activate_editor(editor)
        editor.window = window

    def _qt4_tab_close_request(self, control):
        """ Handle a tabCloseRequest from the splitter widget. """

        for editor in self.window.editors:
            if editor.control == control:
                editor.close()
                break

    def _qt4_tab_window_changed(self, control):
        """ Handle a tab drag to a different WorkbenchWindow. """

        editor = self._qt4_remove_editor_with_control(control)
        kind = self.window.editor_manager.get_editor_kind(editor)

        while not control.isWindow():
            control = control.parent()
        for window in self.window.workbench.windows:
            if window.control == control:
                window.editors.append(editor)
                window.editor_manager.add_editor(editor, kind)
                window.layout._qt4_get_editor_control(editor)
                window.activate_editor(editor)
                editor.window = window
                break

    def _qt4_remove_editor_with_control(self, control):
        """ Finds the editor associated with 'control' and removes it. Returns
            the editor, or None if no editor was found.
        """
        for editor in self.window.editors:
            if editor.control == control:
                self.editor_closing = editor
                control.removeEventFilter(self._qt4_mon)
                self.editor_closed = editor

                # Make sure that focus events get fired if this editor is
                # subsequently added to another window.
                editor.has_focus = False

                return editor

    def _qt4_get_editor_control(self, editor):
        """ Create the editor control if it hasn't already been done. """

        if editor.control is None:
            self.editor_opening = editor

            # We must provide a parent (because TraitsUI checks for it when
            # deciding what sort of panel to create) but it can't be the editor
            # area (because it will be automatically added to the base
            # QSplitter).
            editor.control = editor.create_control(self.window.control)
            editor.control.setObjectName(editor.id)

            editor.observe(self._qt4_editor_tab_spinner, "_loading")

            self.editor_opened = editor

        def on_name_changed(event):
            editor = event.object
            self._qt4_editor_area.setWidgetTitle(editor.control, editor.name)

        editor.observe(on_name_changed, "name")

        self._qt4_monitor(editor.control)

        return editor.control

    def _qt4_add_view(self, view, position, relative_to, size):
        """ Add a view. """

        # If no specific position is specified then use the view's default
        # position.
        if position is None:
            position = view.position

        dw = self._qt4_create_view_dock_widget(view, size)
        mw = self.window.control

        try:
            rel_dw = relative_to._qt4_dock
        except AttributeError:
            rel_dw = None

        if rel_dw is None:
            # If we are trying to add a view with a non-existent item, then
            # just default to the left of the editor area.
            if position == "with":
                position = "left"

            # Position the view relative to the editor area.
            try:
                dwa = _EDIT_AREA_MAP[position]
            except KeyError:
                raise ValueError("unknown view position: %s" % position)

            mw.addDockWidget(dwa, dw)
        elif position == "with":
            # FIXME v3: The Qt documentation says that the second should be
            # placed above the first, but it always seems to be underneath (ie.
            # hidden) which is not what the user is expecting.
            mw.tabifyDockWidget(rel_dw, dw)
        else:
            try:
                orient, swap = _VIEW_AREA_MAP[position]
            except KeyError:
                raise ValueError("unknown view position: %s" % position)

            mw.splitDockWidget(rel_dw, dw, orient)

            # The Qt documentation implies that the layout direction can be
            # used to position the new dock widget relative to the existing one
            # but I could only get the button positions to change.  Instead we
            # move things around afterwards if required.
            if swap:
                mw.removeDockWidget(rel_dw)
                mw.splitDockWidget(dw, rel_dw, orient)
                rel_dw.show()

    def _qt4_create_view_dock_widget(self, view, size=(-1, -1)):
        """ Create a dock widget that wraps a view. """

        # See if it has already been created.
        try:
            dw = view._qt4_dock
        except AttributeError:
            dw = QtGui.QDockWidget(view.name, self.window.control)
            dw.setWidget(_ViewContainer(size, self.window.control))
            dw.setObjectName(view.id)
            dw.toggleViewAction().toggled.connect(
                self._qt4_handle_dock_visibility
            )
            dw.visibilityChanged.connect(self._qt4_handle_dock_visibility)

            # Save the dock window.
            view._qt4_dock = dw

            def on_name_changed(event):
                view._qt4_dock.setWindowTitle(view.name)

            view.observe(on_name_changed, "name")

        # Make sure the view control exists.
        if view.control is None:
            # Make sure that the view knows which window it is in.
            view.window = self.window

            try:
                view.control = view.create_control(dw.widget())
            except:
                # Tidy up if the view couldn't be created.
                delattr(view, "_qt4_dock")
                self.window.control.removeDockWidget(dw)
                dw.deleteLater()
                del dw
                raise

        dw.widget().setCentralWidget(view.control)

        return dw

    def _qt4_delete_view_dock_widget(self, view):
        """ Delete a view's dock widget. """

        dw = view._qt4_dock

        # Disassociate the view from the dock.
        if view.control is not None:
            view.control.setParent(None)

        delattr(view, "_qt4_dock")

        # Delete the dock (and the view container).
        self.window.control.removeDockWidget(dw)
        dw.deleteLater()

    def _qt4_handle_dock_visibility(self, checked):
        """ Handle the visibility of a dock window changing. """

        # Find the dock window by its toggle action.
        for v in self.window.views:
            try:
                dw = v._qt4_dock
            except AttributeError:
                continue

            sender = dw.sender()
            if sender is dw.toggleViewAction() or sender in dw.children():
                # Toggling the action or pressing the close button on
                # the view
                v.visible = checked

    def _qt4_monitor(self, control):
        """ Install an event filter for a view or editor control to keep an eye
        on certain events.
        """

        # Create the monitoring object if needed.
        try:
            mon = self._qt4_mon
        except AttributeError:
            mon = self._qt4_mon = _Monitor(self)

        control.installEventFilter(mon)


class _Monitor(QtCore.QObject):
    """ This class monitors a view or editor control. """

    def __init__(self, layout):
        QtCore.QObject.__init__(self, layout.window.control)

        self._layout = layout

    def eventFilter(self, obj, e):
        if isinstance(e, QtGui.QCloseEvent):
            for editor in self._layout.window.editors:
                if editor.control is obj:
                    self._layout.editor_closing = editor
                    editor.destroy_control()
                    self._layout.editor_closed = editor

                    break

        return False


class _ViewContainer(QtGui.QMainWindow):
    """ This class is a container for a view that allows an initial size
    (specified as a tuple) to be set.
    """

    def __init__(self, size, main_window):
        """ Initialise the object. """

        QtGui.QMainWindow.__init__(self)

        # Save the size and main window.
        self._width, self._height = size
        self._main_window = main_window

    def sizeHint(self):
        """ Reimplemented to return the initial size or the view's current
        size.
        """

        sh = self.centralWidget().sizeHint()

        if self._width > 0:
            if self._width > 1:
                w = self._width
            else:
                w = self._main_window.width() * self._width

            sh.setWidth(int(w))

        if self._height > 0:
            if self._height > 1:
                h = self._height
            else:
                h = self._main_window.height() * self._height

            sh.setHeight(int(h))

        return sh

    def showEvent(self, e):
        """ Reimplemented to use the view's current size once shown. """

        self._width = self._height = -1

        QtGui.QMainWindow.showEvent(self, e)
