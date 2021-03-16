# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import sys


from pyface.qt import QtCore, QtGui


from traits.api import Bool, Event, observe, provides, Str


from pyface.i_python_editor import IPythonEditor, MPythonEditor
from pyface.key_pressed_event import KeyPressedEvent
from pyface.widget import Widget
from pyface.ui.qt4.code_editor.code_widget import AdvancedCodeWidget


@provides(IPythonEditor)
class PythonEditor(MPythonEditor, Widget):
    """ The toolkit specific implementation of a PythonEditor.  See the
    IPythonEditor interface for the API documentation.
    """

    # 'IPythonEditor' interface --------------------------------------------

    dirty = Bool(False)

    path = Str()

    show_line_numbers = Bool(True)

    # Events ----

    changed = Event()

    key_pressed = Event(KeyPressedEvent)

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, **traits):
        super(PythonEditor, self).__init__(parent=parent, **traits)
        self._create()

    # ------------------------------------------------------------------------
    # 'PythonEditor' interface.
    # ------------------------------------------------------------------------

    def load(self, path=None):
        """ Loads the contents of the editor.
        """
        if path is None:
            path = self.path

        # We will have no path for a new script.
        if len(path) > 0:
            f = open(self.path, "r")
            text = f.read()
            f.close()
        else:
            text = ""

        self.control.code.setPlainText(text)
        self.dirty = False

    def save(self, path=None):
        """ Saves the contents of the editor.
        """
        if path is None:
            path = self.path

        f = open(path, "w")
        f.write(self.control.code.toPlainText())
        f.close()

        self.dirty = False

    def select_line(self, lineno):
        """ Selects the specified line.
        """
        self.control.code.set_line_column(lineno, 0)
        self.control.code.moveCursor(
            QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor
        )

    # ------------------------------------------------------------------------
    # 'Widget' interface.
    # ------------------------------------------------------------------------

    def _add_event_listeners(self):
        super(PythonEditor, self)._add_event_listeners()
        self.control.code.installEventFilter(self._event_filter)

        # Connect signals for text changes.
        self.control.code.modificationChanged.connect(self._on_dirty_changed)
        self.control.code.textChanged.connect(self._on_text_changed)

    def _remove_event_listeners(self):
        if self.control is not None:
            # Disconnect signals for text changes.
            self.control.code.modificationChanged.disconnect(
                self._on_dirty_changed
            )
            self.control.code.textChanged.disconnect(self._on_text_changed)
            # Disconnect signals from control and other dependent widgets
            self.control._remove_event_listeners()

            if self._event_filter is not None:
                self.control.code.removeEventFilter(self._event_filter)

        super(PythonEditor, self)._remove_event_listeners()

    def __event_filter_default(self):
        return PythonEditorEventFilter(self, self.control)

    # ------------------------------------------------------------------------
    # Trait handlers.
    # ------------------------------------------------------------------------

    @observe("path")
    def _handle_path_change(self, event):
        self._changed_path()

    @observe("show_line_numbers")
    def _update_visible_line_numbers(self, event=None):
        if self.control is not None:
            self.control.code.line_number_widget.setVisible(
                self.show_line_numbers
            )
            self.control.code.update_line_number_width()

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Creates the toolkit-specific control for the widget.
        """
        self.control = control = AdvancedCodeWidget(parent)
        self._update_visible_line_numbers()

        # Load the editor's contents.
        self.load()

        return control

    def _on_dirty_changed(self, dirty):
        """ Called whenever a change is made to the dirty state of the
            document.
        """
        self.dirty = dirty

    def _on_text_changed(self):
        """ Called whenever a change is made to the text of the document.
        """
        self.changed = True


class PythonEditorEventFilter(QtCore.QObject):
    """ A thin wrapper around the advanced code widget to handle the key_pressed
        Event.
    """

    def __init__(self, editor, parent):
        super(PythonEditorEventFilter, self).__init__(parent)
        self.__editor = editor

    def eventFilter(self, obj, event):
        """ Reimplemented to trap key presses.
        """
        if (
            self.__editor.control
            and obj == self.__editor.control
            and event.type() == QtCore.QEvent.FocusOut
        ):
            # Hack for Traits UI compatibility.
            self.__editor.control.lostFocus.emit()

        elif (
            self.__editor.control
            and obj == self.__editor.control.code
            and event.type() == QtCore.QEvent.KeyPress
        ):
            # Pyface doesn't seem to be Str aware.  Only keep the key code
            # if it corresponds to a single Latin1 character.
            kstr = event.text()
            try:
                kcode = ord(str(kstr))
            except:
                kcode = 0

            mods = event.modifiers()
            self.key_pressed = KeyPressedEvent(
                alt_down=(
                    (mods & QtCore.Qt.AltModifier) == QtCore.Qt.AltModifier
                ),
                control_down=(
                    (mods & QtCore.Qt.ControlModifier)
                    == QtCore.Qt.ControlModifier
                ),
                shift_down=(
                    (mods & QtCore.Qt.ShiftModifier) == QtCore.Qt.ShiftModifier
                ),
                key_code=kcode,
                event=event,
            )

        return super(PythonEditorEventFilter, self).eventFilter(obj, event)
