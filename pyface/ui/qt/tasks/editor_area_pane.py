# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import sys


from pyface.tasks.i_editor_area_pane import IEditorAreaPane, MEditorAreaPane
from traits.api import Any, Callable, List, observe, provides, Tuple


from pyface.qt import QtCore, QtGui, is_qt6, is_pyside


from .task_pane import TaskPane
from .util import set_focus

# ----------------------------------------------------------------------------
# 'EditorAreaPane' class.
# ----------------------------------------------------------------------------


@provides(IEditorAreaPane)
class EditorAreaPane(TaskPane, MEditorAreaPane):
    """ The toolkit-specific implementation of a EditorAreaPane.

    See the IEditorAreaPane interface for API documentation.
    """
    # Private interface ---------------------------------------------------#

    #: A list of connected Qt signals to be removed before destruction.
    #: First item in the tuple is the Qt signal. The second item is the event
    #: handler.
    _connections_to_remove = List(Tuple(Any, Callable))

    # ------------------------------------------------------------------------
    # 'TaskPane' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        # Create and configure the tab widget.
        self.control = control = EditorAreaWidget(self, parent)
        self._filter = EditorAreaDropFilter(self)
        control.installEventFilter(self._filter)
        control.tabBar().setVisible(not self.hide_tab_bar)

        # Connect to the widget's signals.
        control.currentChanged.connect(self._update_active_editor)
        self._connections_to_remove.append(
            (control.currentChanged, self._update_active_editor)
        )
        control.tabCloseRequested.connect(self._close_requested)
        self._connections_to_remove.append(
            (control.tabCloseRequested, self._close_requested)
        )

        # Add shortcuts for scrolling through tabs.
        if sys.platform == "darwin":
            next_seq = "Ctrl+}"
            prev_seq = "Ctrl+{"
        else:
            next_seq = "Ctrl+PgDown"
            prev_seq = "Ctrl+PgUp"
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(next_seq), self.control)
        shortcut.activated.connect(self._next_tab)
        self._connections_to_remove.append(
            (shortcut.activated, self._next_tab)
        )
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(prev_seq), self.control)
        shortcut.activated.connect(self._previous_tab)
        self._connections_to_remove.append(
            (shortcut.activated, self._previous_tab)
        )

        # Add shortcuts for switching to a specific tab.
        mod = "Ctrl+" if sys.platform == "darwin" else "Alt+"
        mapper = QtCore.QSignalMapper(self.control)
        if is_pyside and is_qt6:
            mapper.mappedInt.connect(self.control.setCurrentIndex)
            self._connections_to_remove.append(
                (mapper.mappedInt, self.control.setCurrentIndex)
            )
        else:
            mapper.mapped.connect(self.control.setCurrentIndex)
            self._connections_to_remove.append(
                (mapper.mapped, self.control.setCurrentIndex)
            )
        for i in range(1, 10):
            sequence = QtGui.QKeySequence(mod + str(i))
            shortcut = QtGui.QShortcut(sequence, self.control)
            shortcut.activated.connect(mapper.map)
            self._connections_to_remove.append(
                (shortcut.activated, mapper.map)
            )
            mapper.setMapping(shortcut, i - 1)

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        if self.control is not None:
            self.control.removeEventFilter(self._filter)
            self._filter = None

            for editor in self.editors:
                self.remove_editor(editor)

            while self._connections_to_remove:
                signal, handler = self._connections_to_remove.pop()
                signal.disconnect(handler)

        super().destroy()

    # ------------------------------------------------------------------------
    # 'IEditorAreaPane' interface.
    # ------------------------------------------------------------------------

    def activate_editor(self, editor):
        """ Activates the specified editor in the pane.
        """
        self.control.setCurrentWidget(editor.control)

    def add_editor(self, editor):
        """ Adds an editor to the pane.
        """
        editor.editor_area = self
        editor.create(self.control)
        index = self.control.addTab(editor.control, self._get_label(editor))
        self.control.setTabToolTip(index, editor.tooltip)
        self.editors.append(editor)
        self._update_tab_bar(event=None)

        # The 'currentChanged' signal, used below, is not emitted when the first
        # editor is added.
        if len(self.editors) == 1:
            self.active_editor = editor

    def remove_editor(self, editor):
        """ Removes an editor from the pane.
        """
        self.editors.remove(editor)
        self.control.removeTab(self.control.indexOf(editor.control))
        editor.destroy()
        editor.editor_area = None
        self._update_tab_bar(event=None)
        if not self.editors:
            self.active_editor = None

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _get_label(self, editor):
        """ Return a tab label for an editor.
        """
        label = editor.name
        if editor.dirty:
            label = "*" + label
        return label

    def _get_editor_with_control(self, control):
        """ Return the editor with the specified control.
        """
        for editor in self.editors:
            if editor.control == control:
                return editor
        return None

    def _next_tab(self):
        """ Activate the tab after the currently active tab.
        """
        self.control.setCurrentIndex(self.control.currentIndex() + 1)

    def _previous_tab(self):
        """ Activate the tab before the currently active tab.
        """
        self.control.setCurrentIndex(self.control.currentIndex() - 1)

    # Trait change handlers ------------------------------------------------

    @observe("editors:items:[dirty, name]")
    def _update_label(self, event):
        editor = event.object
        index = self.control.indexOf(editor.control)
        self.control.setTabText(index, self._get_label(editor))

    @observe("editors:items:tooltip")
    def _update_tooltip(self, event):
        editor = event.object
        index = self.control.indexOf(editor.control)
        self.control.setTabToolTip(index, editor.tooltip)

    # Signal handlers -----------------------------------------------------#

    def _close_requested(self, index):
        control = self.control.widget(index)
        editor = self._get_editor_with_control(control)
        editor.close()

    def _update_active_editor(self):
        index = self.control.currentIndex()
        if index == -1:
            self.active_editor = None
        else:
            control = self.control.widget(index)
            self.active_editor = self._get_editor_with_control(control)

    @observe("hide_tab_bar")
    def _update_tab_bar(self, event):
        if self.control is not None:
            visible = self.control.count() > 1 if self.hide_tab_bar else True
            self.control.tabBar().setVisible(visible)


# ----------------------------------------------------------------------------
# Auxillary classes.
# ----------------------------------------------------------------------------


class EditorAreaWidget(QtGui.QTabWidget):
    """ An auxillary widget for implementing AdvancedEditorAreaPane.
    """

    def __init__(self, editor_area, parent=None):
        super().__init__(parent)
        self.editor_area = editor_area

        # Configure the QTabWidget.
        self.setAcceptDrops(True)
        self.setDocumentMode(True)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.setFocusProxy(None)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setUsesScrollButtons(True)

    def focusInEvent(self, event):
        """ Assign focus to the active editor, if possible.
        """
        active_editor = self.editor_area.active_editor
        if active_editor:
            set_focus(active_editor.control)


class EditorAreaDropFilter(QtCore.QObject):
    """ Implements drag and drop support.
    """

    def __init__(self, editor_area):
        super().__init__()
        self.editor_area = editor_area

    def eventFilter(self, object, event):
        """ Handle drag and drop events with MIME type 'text/uri-list'.
        """
        if event.type() in (QtCore.QEvent.Type.DragEnter, QtCore.QEvent.Type.Drop):
            # Build list of accepted files.
            extensions = tuple(self.editor_area.file_drop_extensions)
            file_paths = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(extensions):
                    file_paths.append(file_path)

            # Accept the event if we have at least one accepted file.
            if event.type() == QtCore.QEvent.Type.DragEnter:
                if file_paths:
                    event.acceptProposedAction()

            # Dispatch the events.
            elif event.type() == QtCore.QEvent.Type.Drop:
                for file_path in file_paths:
                    self.editor_area.file_dropped = file_path

            return True

        return super().eventFilter(object, event)
