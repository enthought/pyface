# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An abstract base class for console-type widgets.
"""
# FIXME: This file and the others in this directory have been ripped, more or
#        less intact, out of IPython. At some point we should figure out a more
#        maintainable solution.

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------


import os
from os.path import commonprefix
import re
import sys
from textwrap import dedent
from unicodedata import category


from pyface.qt import QtCore, QtGui

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def is_letter_or_number(char):
    """ Returns whether the specified unicode character is a letter or a number.
    """
    cat = category(char)
    return cat.startswith("L") or cat.startswith("N")


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class ConsoleWidget(QtGui.QWidget):
    """ An abstract base class for console-type widgets. This class has
        functionality for:

            * Maintaining a prompt and editing region
            * Providing the traditional Unix-style console keyboard shortcuts
            * Performing tab completion
            * Paging text

        ConsoleWidget also provides a number of utility methods that will be
        convenient to implementors of a console-style widget.
    """

    # Configuration ------------------------------------------------------

    # The maximum number of lines of text before truncation. Specifying a
    # non-positive number disables text truncation (not recommended).
    buffer_size = 500

    # The type of underlying text widget to use. Valid values are 'plain', which
    # specifies a QPlainTextEdit, and 'rich', which specifies a QTextEdit.
    # NOTE: this value can only be specified during initialization.
    kind = "plain"

    # The type of paging to use. Valid values are:
    #     'inside' : The widget pages like a traditional terminal.
    #     'hsplit' : When paging is requested, the widget is split
    #                horizontally. The top pane contains the console, and the
    #                bottom pane contains the paged text.
    #     'vsplit' : Similar to 'hsplit', except that a vertical splitter used.
    #     'custom' : No action is taken by the widget beyond emitting a
    #                'custom_page_requested(str)' signal.
    #     'none'   : The text is written directly to the console.
    # NOTE: this value can only be specified during initialization.
    paging = "inside"

    # Whether to override ShortcutEvents for the keybindings defined by this
    # widget (Ctrl+n, Ctrl+a, etc). Enable this if you want this widget to take
    # priority (when it has focus) over, e.g., window-level menu shortcuts.
    override_shortcuts = False

    # Signals ------------------------------------------------------------

    # Signals that indicate ConsoleWidget state.
    copy_available = QtCore.Signal(bool)
    redo_available = QtCore.Signal(bool)
    undo_available = QtCore.Signal(bool)

    # Signal emitted when paging is needed and the paging style has been
    # specified as 'custom'.
    custom_page_requested = QtCore.Signal(object)

    # Signal emitted when the font is changed.
    font_changed = QtCore.Signal(QtGui.QFont)

    # Protected class variables ------------------------------------------

    # When the control key is down, these keys are mapped.
    _ctrl_down_remap = {
        QtCore.Qt.Key.Key_B: QtCore.Qt.Key.Key_Left,
        QtCore.Qt.Key.Key_F: QtCore.Qt.Key.Key_Right,
        QtCore.Qt.Key.Key_A: QtCore.Qt.Key.Key_Home,
        QtCore.Qt.Key.Key_P: QtCore.Qt.Key.Key_Up,
        QtCore.Qt.Key.Key_N: QtCore.Qt.Key.Key_Down,
        QtCore.Qt.Key.Key_D: QtCore.Qt.Key.Key_Delete,
    }
    if not sys.platform == "darwin":
        # On OS X, Ctrl-E already does the right thing, whereas End moves the
        # cursor to the bottom of the buffer.
        _ctrl_down_remap[QtCore.Qt.Key.Key_E] = QtCore.Qt.Key.Key_End

    # The shortcuts defined by this widget. We need to keep track of these to
    # support 'override_shortcuts' above.
    _shortcuts = set(_ctrl_down_remap.keys()) | set(
        [QtCore.Qt.Key.Key_C, QtCore.Qt.Key.Key_G, QtCore.Qt.Key.Key_O, QtCore.Qt.Key.Key_V]
    )

    # ---------------------------------------------------------------------------
    # 'QObject' interface
    # ---------------------------------------------------------------------------

    def __init__(self, parent=None):
        """ Create a ConsoleWidget.

        Parameters:
        -----------
        parent : QWidget, optional [default None]
            The parent for this widget.
        """
        super().__init__(parent)

        # A list of connected Qt signals to be removed before destruction.
        # First item in the tuple is the Qt signal. The second item is the
        # event handler.
        self._connections_to_remove = []

        # Create the layout and underlying text widget.
        layout = QtGui.QStackedLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._control = self._create_control()
        self._page_control = None
        self._splitter = None
        if self.paging in ("hsplit", "vsplit"):
            self._splitter = QtGui.QSplitter()
            if self.paging == "hsplit":
                self._splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
            else:
                self._splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
            self._splitter.addWidget(self._control)
            layout.addWidget(self._splitter)
        else:
            layout.addWidget(self._control)

        # Create the paging widget, if necessary.
        if self.paging in ("inside", "hsplit", "vsplit"):
            self._page_control = self._create_page_control()
            if self._splitter:
                self._page_control.hide()
                self._splitter.addWidget(self._page_control)
            else:
                layout.addWidget(self._page_control)

        # Initialize protected variables. Some variables contain useful state
        # information for subclasses; they should be considered read-only.
        self._continuation_prompt = "> "
        self._continuation_prompt_html = None
        self._executing = False
        self._filter_drag = False
        self._filter_resize = False
        self._prompt = ""
        self._prompt_html = None
        self._prompt_pos = 0
        self._prompt_sep = ""
        self._reading = False
        self._reading_callback = None
        self._tab_width = 8
        self._text_completing_pos = 0
        self._filename = "python.html"
        self._png_mode = None

        # Set a monospaced font.
        self.reset_font()

        # Configure actions.
        action = QtGui.QAction("Print", None)
        action.setEnabled(True)
        printkey = QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Print)
        if printkey.matches("Ctrl+P") and sys.platform != "darwin":
            # Only override the default if there is a collision.
            # Qt ctrl = cmd on OSX, so that the match gets a false positive.
            printkey = "Ctrl+Shift+P"
        action.setShortcut(printkey)
        action.triggered.connect(self.print_)
        self._connections_to_remove.append((action.triggered, self.print_))
        self.addAction(action)
        self._print_action = action

        action = QtGui.QAction("Save as HTML/XML", None)
        action.setEnabled(self.can_export())
        action.setShortcut(QtGui.QKeySequence.StandardKey.Save)
        action.triggered.connect(self.export)
        self._connections_to_remove.append((action.triggered, self.export))
        self.addAction(action)
        self._export_action = action

        action = QtGui.QAction("Select All", None)
        action.setEnabled(True)
        action.setShortcut(QtGui.QKeySequence.StandardKey.SelectAll)
        action.triggered.connect(self.select_all)
        self._connections_to_remove.append((action.triggered, self.select_all))
        self.addAction(action)
        self._select_all_action = action

    def eventFilter(self, obj, event):
        """ Reimplemented to ensure a console-like behavior in the underlying
            text widgets.
        """
        etype = event.type()
        if etype == QtCore.QEvent.Type.KeyPress:

            # Re-map keys for all filtered widgets.
            key = event.key()
            if (
                self._control_key_down(event.modifiers())
                and key in self._ctrl_down_remap
            ):
                new_event = QtGui.QKeyEvent(
                    QtCore.QEvent.Type.KeyPress,
                    self._ctrl_down_remap[key],
                    QtCore.Qt.KeyboardModifier.NoModifier,
                )
                QtGui.QApplication.sendEvent(obj, new_event)
                return True

            elif obj == self._control:
                return self._event_filter_console_keypress(event)

            elif obj == self._page_control:
                return self._event_filter_page_keypress(event)

        # Make middle-click paste safe.
        elif (
            etype == QtCore.QEvent.Type.MouseButtonRelease
            and event.button() == QtCore.Qt.MouseButton.MiddleButton
            and obj == self._control.viewport()
        ):
            cursor = self._control.cursorForPosition(event.pos())
            self._control.setTextCursor(cursor)
            self.paste(QtGui.QClipboard.Mode.Selection)
            return True

        # Manually adjust the scrollbars *after* a resize event is dispatched.
        elif etype == QtCore.QEvent.Type.Resize and not self._filter_resize:
            self._filter_resize = True
            QtGui.QApplication.sendEvent(obj, event)
            self._adjust_scrollbars()
            self._filter_resize = False
            return True

        # Override shortcuts for all filtered widgets.
        elif (
            etype == QtCore.QEvent.Type.ShortcutOverride
            and self.override_shortcuts
            and self._control_key_down(event.modifiers())
            and event.key() in self._shortcuts
        ):
            event.accept()

        # Ensure that drags are safe. The problem is that the drag starting
        # logic, which determines whether the drag is a Copy or Move, is locked
        # down in QTextControl. If the widget is editable, which it must be if
        # we're not executing, the drag will be a Move. The following hack
        # prevents QTextControl from deleting the text by clearing the selection
        # when a drag leave event originating from this widget is dispatched.
        # The fact that we have to clear the user's selection is unfortunate,
        # but the alternative--trying to prevent Qt from using its hardwired
        # drag logic and writing our own--is worse.
        elif (
            etype == QtCore.QEvent.Type.DragEnter
            and obj == self._control.viewport()
            and event.source() == self._control.viewport()
        ):
            self._filter_drag = True
        elif (
            etype == QtCore.QEvent.Type.DragLeave
            and obj == self._control.viewport()
            and self._filter_drag
        ):
            cursor = self._control.textCursor()
            cursor.clearSelection()
            self._control.setTextCursor(cursor)
            self._filter_drag = False

        # Ensure that drops are safe.
        elif etype == QtCore.QEvent.Type.Drop and obj == self._control.viewport():
            cursor = self._control.cursorForPosition(event.pos())
            if self._in_buffer(cursor.position()):
                text = event.mimeData().text()
                self._insert_plain_text_into_buffer(cursor, text)

            # Qt is expecting to get something here--drag and drop occurs in its
            # own event loop. Send a DragLeave event to end it.
            QtGui.QApplication.sendEvent(obj, QtGui.QDragLeaveEvent())
            return True

        return super().eventFilter(obj, event)

    def _remove_event_listeners(self):
        while self._connections_to_remove:
            signal, handler = self._connections_to_remove.pop()
            signal.disconnect(handler)

    # ---------------------------------------------------------------------------
    # 'QWidget' interface
    # ---------------------------------------------------------------------------

    def sizeHint(self):
        """ Reimplemented to suggest a size that is 80 characters wide and
            25 lines high.
        """
        font_metrics = QtGui.QFontMetrics(self.font)
        margin = (
            self._control.frameWidth()
            + self._control.document().documentMargin()
        ) * 2
        style = self.style()
        splitwidth = style.pixelMetric(QtGui.QStyle.PixelMetric.PM_SplitterWidth)

        # Note 1: Despite my best efforts to take the various margins into
        # account, the width is still coming out a bit too small, so we include
        # a fudge factor of one character here.
        # Note 2: QFontMetrics.maxWidth is not used here or anywhere else due
        # to a Qt bug on certain Mac OS systems where it returns 0.

        # QFontMetrics.width() is deprecated and Qt docs suggest using
        # horizontalAdvance() instead, but is only available since Qt 5.11
        if QtCore.__version_info__ >= (5, 11):
            width = font_metrics.horizontalAdvance(" ") * 81 + margin
        else:
            width = font_metrics.width(" ") * 81 + margin
        width += style.pixelMetric(QtGui.QStyle.PixelMetric.PM_ScrollBarExtent)
        if self.paging == "hsplit":
            width = width * 2 + splitwidth

        height = font_metrics.height() * 25 + margin
        if self.paging == "vsplit":
            height = height * 2 + splitwidth

        return QtCore.QSize(int(width), int(height))

    # ---------------------------------------------------------------------------
    # 'ConsoleWidget' public interface
    # ---------------------------------------------------------------------------

    def can_copy(self):
        """ Returns whether text can be copied to the clipboard.
        """
        return self._control.textCursor().hasSelection()

    def can_cut(self):
        """ Returns whether text can be cut to the clipboard.
        """
        cursor = self._control.textCursor()
        return (
            cursor.hasSelection()
            and self._in_buffer(cursor.anchor())
            and self._in_buffer(cursor.position())
        )

    def can_paste(self):
        """ Returns whether text can be pasted from the clipboard.
        """
        if self._control.textInteractionFlags() & QtCore.Qt.TextInteractionFlag.TextEditable:
            return bool(QtGui.QApplication.clipboard().text())
        return False

    def can_export(self):
        """Returns whether we can export. Currently only rich widgets
        can export html.
        """
        return self.kind == "rich"

    def clear(self, keep_input=True):
        """ Clear the console.

        Parameters:
        -----------
        keep_input : bool, optional (default True)
            If set, restores the old input buffer if a new prompt is written.
        """
        if self._executing:
            self._control.clear()
        else:
            if keep_input:
                input_buffer = self.input_buffer
            self._control.clear()
            self._show_prompt()
            if keep_input:
                self.input_buffer = input_buffer

    def copy(self):
        """ Copy the currently selected text to the clipboard.
        """
        self._control.copy()

    def cut(self):
        """ Copy the currently selected text to the clipboard and delete it
            if it's inside the input buffer.
        """
        self.copy()
        if self.can_cut():
            self._control.textCursor().removeSelectedText()

    def execute(self, source=None, hidden=False, interactive=False):
        """ Executes source or the input buffer, possibly prompting for more
        input.

        Parameters:
        -----------
        source : str, optional

            The source to execute. If not specified, the input buffer will be
            used. If specified and 'hidden' is False, the input buffer will be
            replaced with the source before execution.

        hidden : bool, optional (default False)

            If set, no output will be shown and the prompt will not be modified.
            In other words, it will be completely invisible to the user that
            an execution has occurred.

        interactive : bool, optional (default False)

            Whether the console is to treat the source as having been manually
            entered by the user. The effect of this parameter depends on the
            subclass implementation.

        Raises:
        -------
        RuntimeError
            If incomplete input is given and 'hidden' is True. In this case,
            it is not possible to prompt for more input.

        Returns:
        --------
        A boolean indicating whether the source was executed.
        """
        # WARNING: The order in which things happen here is very particular, in
        # large part because our syntax highlighting is fragile. If you change
        # something, test carefully!

        # Decide what to execute.
        if source is None:
            source = self.input_buffer
            if not hidden:
                # A newline is appended later, but it should be considered part
                # of the input buffer.
                source += "\n"
        elif not hidden:
            self.input_buffer = source

        # Execute the source or show a continuation prompt if it is incomplete.
        complete = self._is_complete(source, interactive)
        if hidden:
            if complete:
                self._execute(source, hidden)
            else:
                error = 'Incomplete noninteractive input: "%s"'
                raise RuntimeError(error % source)
        else:
            if complete:
                self._append_plain_text("\n")
                self._executing_input_buffer = self.input_buffer
                self._executing = True
                self._prompt_finished()

                # The maximum block count is only in effect during execution.
                # This ensures that _prompt_pos does not become invalid due to
                # text truncation.
                self._control.document().setMaximumBlockCount(self.buffer_size)

                # Setting a positive maximum block count will automatically
                # disable the undo/redo history, but just to be safe:
                self._control.setUndoRedoEnabled(False)

                # Perform actual execution.
                self._execute(source, hidden)

            else:
                # Do this inside an edit block so continuation prompts are
                # removed seamlessly via undo/redo.
                cursor = self._get_end_cursor()
                cursor.beginEditBlock()
                cursor.insertText("\n")
                self._insert_continuation_prompt(cursor)
                cursor.endEditBlock()

                # Do not do this inside the edit block. It works as expected
                # when using a QPlainTextEdit control, but does not have an
                # effect when using a QTextEdit. I believe this is a Qt bug.
                self._control.moveCursor(QtGui.QTextCursor.MoveOperation.End)

        return complete

    def _get_input_buffer(self):
        """ The text that the user has entered entered at the current prompt.
        """
        # If we're executing, the input buffer may not even exist anymore due to
        # the limit imposed by 'buffer_size'. Therefore, we store it.
        if self._executing:
            return self._executing_input_buffer

        cursor = self._get_end_cursor()
        cursor.setPosition(self._prompt_pos, QtGui.QTextCursor.MoveMode.KeepAnchor)
        input_buffer = cursor.selection().toPlainText()

        # Strip out continuation prompts.
        return input_buffer.replace("\n" + self._continuation_prompt, "\n")

    def _set_input_buffer(self, string):
        """ Replaces the text in the input buffer with 'string'.
        """
        # For now, it is an error to modify the input buffer during execution.
        if self._executing:
            raise RuntimeError("Cannot change input buffer during execution.")

        # Remove old text.
        cursor = self._get_end_cursor()
        cursor.beginEditBlock()
        cursor.setPosition(self._prompt_pos, QtGui.QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()

        # Insert new text with continuation prompts.
        self._insert_plain_text_into_buffer(self._get_prompt_cursor(), string)
        cursor.endEditBlock()
        self._control.moveCursor(QtGui.QTextCursor.MoveOperation.End)

    input_buffer = property(_get_input_buffer, _set_input_buffer)

    def _get_font(self):
        """ The base font being used by the ConsoleWidget.
        """
        return self._control.document().defaultFont()

    def _set_font(self, font):
        """ Sets the base font for the ConsoleWidget to the specified QFont.
        """
        font_metrics = QtGui.QFontMetrics(font)

        # QFontMetrics.width() is deprecated and Qt docs suggest using
        # horizontalAdvance() instead, but is only available since Qt 5.11
        if QtCore.__version_info__ >= (5, 11):
            width = font_metrics.horizontalAdvance(" ")
        else:
            width = font_metrics.width(" ")

        self._control.setTabStopDistance(self.tab_width * width)

        self._control.document().setDefaultFont(font)
        if self._page_control:
            self._page_control.document().setDefaultFont(font)

        self.font_changed.emit(font)

    font = property(_get_font, _set_font)

    def paste(self, mode=QtGui.QClipboard.Mode.Clipboard):
        """ Paste the contents of the clipboard into the input region.

        Parameters:
        -----------
        mode : QClipboard::Mode, optional [default QClipboard::Clipboard]

            Controls which part of the system clipboard is used. This can be
            used to access the selection clipboard in X11 and the Find buffer
            in Mac OS. By default, the regular clipboard is used.
        """
        if self._control.textInteractionFlags() & QtCore.Qt.TextInteractionFlag.TextEditable:
            # Make sure the paste is safe.
            self._keep_cursor_in_buffer()
            cursor = self._control.textCursor()

            # Remove any trailing newline, which confuses the GUI and forces the
            # user to backspace.
            text = QtGui.QApplication.clipboard().text(mode).rstrip()
            self._insert_plain_text_into_buffer(cursor, dedent(text))

    def print_(self, printer=None):
        """ Print the contents of the ConsoleWidget to the specified QPrinter.
        """
        if not printer:
            printer = QtGui.QPrinter()
            if QtGui.QPrintDialog(printer).exec_() != QtGui.QDialog.DialogCode.Accepted:
                return
        self._control.print_(printer)

    def export(self, parent=None):
        """Export HTML/XML in various modes from one Dialog."""
        parent = parent or None  # sometimes parent is False
        dialog = QtGui.QFileDialog(parent, "Save Console as...")
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptMode.AcceptSave)
        filters = [
            "HTML with PNG figures (*.html *.htm)",
            "XHTML with inline SVG figures (*.xhtml *.xml)",
        ]
        dialog.setNameFilters(filters)
        if self._filename:
            dialog.selectFile(self._filename)
            root, ext = os.path.splitext(self._filename)
            if ext.lower() in (".xml", ".xhtml"):
                dialog.selectNameFilter(filters[-1])
        if dialog.exec_():
            filename = str(dialog.selectedFiles()[0])
            self._filename = filename
            choice = str(dialog.selectedNameFilter())

            if choice.startswith("XHTML"):
                exporter = self.export_xhtml
            else:
                exporter = self.export_html

            try:
                return exporter(filename)
            except Exception as e:
                title = self.window().windowTitle()
                msg = "Error while saving to: %s\n" % filename + str(e)
                QtGui.QMessageBox.warning(
                    self,
                    title,
                    msg,
                    QtGui.QMessageBox.StandardButton.Ok,
                    QtGui.QMessageBox.StandardButton.Ok,
                )
        return None

    def export_html(self, filename):
        """ Export the contents of the ConsoleWidget as HTML.

        Parameters:
        -----------
        filename : str
            The file to be saved.
        inline : bool, optional [default True]
            If True, include images as inline PNGs.  Otherwise,
            include them as links to external PNG files, mimicking
            web browsers' "Web Page, Complete" behavior.
        """
        # N.B. this is overly restrictive, but Qt's output is
        # predictable...
        img_re = re.compile(r'<img src="(?P<name>[\d]+)" />')
        html = self.fix_html_encoding(str(self._control.toHtml().toUtf8()))
        if self._png_mode:
            # preference saved, don't ask again
            if img_re.search(html):
                inline = self._png_mode == "inline"
            else:
                inline = True
        elif img_re.search(html):
            # there are images
            widget = QtGui.QWidget()
            layout = QtGui.QVBoxLayout(widget)
            title = self.window().windowTitle()
            msg = "Exporting HTML with PNGs"
            info = (
                "Would you like inline PNGs (single large html file) or "
                + "external image files?"
            )
            checkbox = QtGui.QCheckBox("&Don't ask again")
            checkbox.setShortcut("D")
            ib = QtGui.QPushButton("&Inline", self)
            ib.setShortcut("I")
            eb = QtGui.QPushButton("&External", self)
            eb.setShortcut("E")
            box = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Question, title, msg)
            box.setInformativeText(info)
            box.addButton(ib, QtGui.QMessageBox.ButtonRole.NoRole)
            box.addButton(eb, QtGui.QMessageBox.ButtonRole.YesRole)
            box.setDefaultButton(ib)
            layout.setSpacing(0)
            layout.addWidget(box)
            layout.addWidget(checkbox)
            widget.setLayout(layout)
            widget.show()
            reply = box.exec_()
            inline = reply == 0
            if checkbox.checkState():
                # don't ask anymore, always use this choice
                if inline:
                    self._png_mode = "inline"
                else:
                    self._png_mode = "external"
        else:
            # no images
            inline = True

        if inline:
            path = None
        else:
            root, ext = os.path.splitext(filename)
            path = root + "_files"
            if os.path.isfile(path):
                raise OSError("%s exists, but is not a directory." % path)

        f = open(filename, "w")
        try:
            f.write(
                img_re.sub(
                    lambda x: self.image_tag(x, path=path, format="png"), html
                )
            )
        except Exception as e:
            f.close()
            raise e
        else:
            f.close()
        return filename

    def export_xhtml(self, filename):
        """ Export the contents of the ConsoleWidget as XHTML with inline SVGs.
        """
        f = open(filename, "w")
        try:
            # N.B. this is overly restrictive, but Qt's output is
            # predictable...
            img_re = re.compile(r'<img src="(?P<name>[\d]+)" />')
            html = str(self._control.toHtml().toUtf8())
            # Hack to make xhtml header -- note that we are not doing
            # any check for valid xml
            offset = html.find("<html>")
            assert offset > -1
            html = (
                '<html xmlns="http://www.w3.org/1999/xhtml">\n'
                + html[offset + 6:]
            )
            # And now declare UTF-8 encoding
            html = self.fix_html_encoding(html)
            f.write(
                img_re.sub(
                    lambda x: self.image_tag(x, path=None, format="svg"), html
                )
            )
        except Exception as e:
            f.close()
            raise e
        else:
            f.close()
        return filename

    def fix_html_encoding(self, html):
        """ Return html string, with a UTF-8 declaration added to <HEAD>.

        Assumes that html is Qt generated and has already been UTF-8 encoded
        and coerced to a python string.  If the expected head element is
        not found, the given object is returned unmodified.

        This patching is needed for proper rendering of some characters
        (e.g., indented commands) when viewing exported HTML on a local
        system (i.e., without seeing an encoding declaration in an HTTP
        header).

        C.f. http://www.w3.org/International/O-charset for details.
        """
        offset = html.find("<head>")
        if offset > -1:
            html = (
                html[: offset + 6]
                + '\n<meta http-equiv="Content-Type" '
                + 'content="text/html; charset=utf-8" />\n'
                + html[offset + 6:]
            )

        return html

    def image_tag(self, match, path=None, format="png"):
        """ Return (X)HTML mark-up for the image-tag given by match.

        Parameters
        ----------
        match : re.SRE_Match
            A match to an HTML image tag as exported by Qt, with
            match.group("Name") containing the matched image ID.

        path : string|None, optional [default None]
            If not None, specifies a path to which supporting files
            may be written (e.g., for linked images).
            If None, all images are to be included inline.

        format : "png"|"svg", optional [default "png"]
            Format for returned or referenced images.

        Subclasses supporting image display should override this
        method.
        """

        # Default case -- not enough information to generate tag
        return ""

    def prompt_to_top(self):
        """ Moves the prompt to the top of the viewport.
        """
        if not self._executing:
            prompt_cursor = self._get_prompt_cursor()
            if self._get_cursor().blockNumber() < prompt_cursor.blockNumber():
                self._set_cursor(prompt_cursor)
            self._set_top_cursor(prompt_cursor)

    def redo(self):
        """ Redo the last operation. If there is no operation to redo, nothing
            happens.
        """
        self._control.redo()

    def reset_font(self):
        """ Sets the font to the default fixed-width font for this platform.
        """
        if sys.platform == "win32":
            # Consolas ships with Vista/Win7, fallback to Courier if needed
            family, fallback = "Consolas", "Courier"
        elif sys.platform == "darwin":
            # OSX always has Monaco, no need for a fallback
            family, fallback = "Monaco", None
        else:
            # FIXME: remove Consolas as a default on Linux once our font
            # selections are configurable by the user.
            family, fallback = "Consolas", "Monospace"

        # Check whether we got what we wanted using QFontInfo, since
        # exactMatch() is overly strict and returns false in too many cases.
        font = QtGui.QFont(family)
        font_info = QtGui.QFontInfo(font)
        if fallback is not None and font_info.family() != family:
            font = QtGui.QFont(fallback)

        font.setPointSize(QtGui.QApplication.font().pointSize())
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self._set_font(font)

    def change_font_size(self, delta):
        """Change the font size by the specified amount (in points).
        """
        font = self.font
        font.setPointSize(font.pointSize() + delta)
        self._set_font(font)

    def select_all(self):
        """ Selects all the text in the buffer.
        """
        self._control.selectAll()

    def _get_tab_width(self):
        """ The width (in terms of space characters) for tab characters.
        """
        return self._tab_width

    def _set_tab_width(self, tab_width):
        """ Sets the width (in terms of space characters) for tab characters.
        """
        font_metrics = QtGui.QFontMetrics(self.font)

        # QFontMetrics.width() is deprecated and Qt docs suggest using
        # horizontalAdvance() instead, but is only available since Qt 5.11
        if QtCore.__version_info__ >= (5, 11):
            width = font_metrics.horizontalAdvance(" ")
        else:
            width = font_metrics.width(" ")

        self._control.setTabStopDistance(tab_width * width)

        self._tab_width = tab_width

    tab_width = property(_get_tab_width, _set_tab_width)

    def undo(self):
        """ Undo the last operation. If there is no operation to undo, nothing
            happens.
        """
        self._control.undo()

    # ---------------------------------------------------------------------------
    # 'ConsoleWidget' abstract interface
    # ---------------------------------------------------------------------------

    def _is_complete(self, source, interactive):
        """ Returns whether 'source' can be executed. When triggered by an
            Enter/Return key press, 'interactive' is True; otherwise, it is
            False.
        """
        raise NotImplementedError()

    def _execute(self, source, hidden):
        """ Execute 'source'. If 'hidden', do not show any output.
        """
        raise NotImplementedError()

    def _prompt_started_hook(self):
        """ Called immediately after a new prompt is displayed.
        """
        pass

    def _prompt_finished_hook(self):
        """ Called immediately after a prompt is finished, i.e. when some input
            will be processed and a new prompt displayed.
        """
        pass

    def _up_pressed(self):
        """ Called when the up key is pressed. Returns whether to continue
            processing the event.
        """
        return True

    def _down_pressed(self):
        """ Called when the down key is pressed. Returns whether to continue
            processing the event.
        """
        return True

    def _tab_pressed(self):
        """ Called when the tab key is pressed. Returns whether to continue
            processing the event.
        """
        return False

    # --------------------------------------------------------------------------
    # 'ConsoleWidget' protected interface
    # --------------------------------------------------------------------------

    def _append_html(self, html):
        """ Appends html at the end of the console buffer.
        """
        cursor = self._get_end_cursor()
        self._insert_html(cursor, html)

    def _append_html_fetching_plain_text(self, html):
        """ Appends 'html', then returns the plain text version of it.
        """
        cursor = self._get_end_cursor()
        return self._insert_html_fetching_plain_text(cursor, html)

    def _append_plain_text(self, text):
        """ Appends plain text at the end of the console buffer, processing
            ANSI codes if enabled.
        """
        cursor = self._get_end_cursor()
        self._insert_plain_text(cursor, text)

    def _append_plain_text_keeping_prompt(self, text):
        """ Writes 'text' after the current prompt, then restores the old prompt
            with its old input buffer.
        """
        input_buffer = self.input_buffer
        self._append_plain_text("\n")
        self._prompt_finished()

        self._append_plain_text(text)
        self._show_prompt()
        self.input_buffer = input_buffer

    def _cancel_text_completion(self):
        """ If text completion is progress, cancel it.
        """
        if self._text_completing_pos:
            self._clear_temporary_buffer()
            self._text_completing_pos = 0

    def _clear_temporary_buffer(self):
        """ Clears the "temporary text" buffer, i.e. all the text following
            the prompt region.
        """
        # Select and remove all text below the input buffer.
        cursor = self._get_prompt_cursor()
        prompt = self._continuation_prompt.lstrip()
        while cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextBlock):
            temp_cursor = QtGui.QTextCursor(cursor)
            temp_cursor.select(QtGui.QTextCursor.SelectionType.BlockUnderCursor)
            text = temp_cursor.selection().toPlainText().lstrip()
            if not text.startswith(prompt):
                break
        else:
            # We've reached the end of the input buffer and no text follows.
            return
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left)  # Grab the newline.
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.End, QtGui.QTextCursor.MoveMode.KeepAnchor
        )
        cursor.removeSelectedText()

        # After doing this, we have no choice but to clear the undo/redo
        # history. Otherwise, the text is not "temporary" at all, because it
        # can be recalled with undo/redo. Unfortunately, Qt does not expose
        # fine-grained control to the undo/redo system.
        if self._control.isUndoRedoEnabled():
            self._control.setUndoRedoEnabled(False)
            self._control.setUndoRedoEnabled(True)

    def _complete_with_items(self, cursor, items):
        """ Performs completion with 'items' at the specified cursor location.
        """
        self._cancel_text_completion()

        if len(items) == 1:
            cursor.setPosition(
                self._control.textCursor().position(),
                QtGui.QTextCursor.MoveMode.KeepAnchor,
            )
            cursor.insertText(items[0])

        elif len(items) > 1:
            current_pos = self._control.textCursor().position()
            prefix = commonprefix(items)
            if prefix:
                cursor.setPosition(current_pos, QtGui.QTextCursor.MoveMode.KeepAnchor)
                cursor.insertText(prefix)
                current_pos = cursor.position()

            cursor.beginEditBlock()
            self._append_plain_text("\n")
            self._page(self._format_as_columns(items))
            cursor.endEditBlock()

            cursor.setPosition(current_pos)
            self._control.moveCursor(QtGui.QTextCursor.MoveOperation.End)
            self._control.setTextCursor(cursor)
            self._text_completing_pos = current_pos

    def _context_menu_make(self, pos):
        """ Creates a context menu for the given QPoint (in widget coordinates).
        """
        menu = QtGui.QMenu(self)

        cut_action = menu.addAction("Cut", self.cut)
        cut_action.setEnabled(self.can_cut())
        cut_action.setShortcut(QtGui.QKeySequence.StandardKey.Cut)

        copy_action = menu.addAction("Copy", self.copy)
        copy_action.setEnabled(self.can_copy())
        copy_action.setShortcut(QtGui.QKeySequence.StandardKey.Copy)

        paste_action = menu.addAction("Paste", self.paste)
        paste_action.setEnabled(self.can_paste())
        paste_action.setShortcut(QtGui.QKeySequence.StandardKey.Paste)

        menu.addSeparator()
        menu.addAction(self._select_all_action)

        menu.addSeparator()
        menu.addAction(self._export_action)
        menu.addAction(self._print_action)

        return menu

    def _control_key_down(self, modifiers, include_command=False):
        """ Given a KeyboardModifiers flags object, return whether the Control
        key is down.

        Parameters:
        -----------
        include_command : bool, optional (default True)
            Whether to treat the Command key as a (mutually exclusive) synonym
            for Control when in Mac OS.
        """
        # Note that on Mac OS, ControlModifier corresponds to the Command key
        # while MetaModifier corresponds to the Control key.
        if sys.platform == "darwin":
            down = include_command and (modifiers & QtCore.Qt.KeyboardModifier.ControlModifier)
            return bool(down) ^ bool(modifiers & QtCore.Qt.KeyboardModifier.MetaModifier)
        else:
            return bool(modifiers & QtCore.Qt.KeyboardModifier.ControlModifier)

    def _create_control(self):
        """ Creates and connects the underlying text widget.
        """
        # Create the underlying control.
        if self.kind == "plain":
            control = QtGui.QPlainTextEdit()
        elif self.kind == "rich":
            control = QtGui.QTextEdit()
            control.setAcceptRichText(False)

        # Install event filters. The filter on the viewport is needed for
        # mouse events and drag events.
        control.installEventFilter(self)
        control.viewport().installEventFilter(self)

        # Connect signals.
        control.cursorPositionChanged.connect(self._cursor_position_changed)
        self._connections_to_remove.append(
            (control.cursorPositionChanged, self._cursor_position_changed)
        )
        control.customContextMenuRequested.connect(
            self._custom_context_menu_requested
        )
        self._connections_to_remove.append(
            (control.customContextMenuRequested,
             self._custom_context_menu_requested)
        )
        control.copyAvailable.connect(self.copy_available)
        self._connections_to_remove.append(
            (control.copyAvailable, self.copy_available)
        )
        control.redoAvailable.connect(self.redo_available)
        self._connections_to_remove.append(
            (control.redoAvailable, self.redo_available)
        )
        control.undoAvailable.connect(self.undo_available)
        self._connections_to_remove.append(
            (control.undoAvailable, self.undo_available)
        )

        # Hijack the document size change signal to prevent Qt from adjusting
        # the viewport's scrollbar. We are relying on an implementation detail
        # of Q(Plain)TextEdit here, which is potentially dangerous, but without
        # this functionality we cannot create a nice terminal interface.
        layout = control.document().documentLayout()
        layout.documentSizeChanged.disconnect()
        layout.documentSizeChanged.connect(self._adjust_scrollbars)
        # The document layout doesn't stay the same therefore its signal is
        # not explicitly disconnected on destruction

        # Configure the control.
        control.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        control.setReadOnly(True)
        control.setUndoRedoEnabled(False)
        control.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        return control

    def _create_page_control(self):
        """ Creates and connects the underlying paging widget.
        """
        if self.kind == "plain":
            control = QtGui.QPlainTextEdit()
        elif self.kind == "rich":
            control = QtGui.QTextEdit()
        control.installEventFilter(self)
        control.setReadOnly(True)
        control.setUndoRedoEnabled(False)
        control.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        return control

    def _event_filter_console_keypress(self, event):
        """ Filter key events for the underlying text widget to create a
            console-like interface.
        """
        intercepted = False
        cursor = self._control.textCursor()
        position = cursor.position()
        key = event.key()
        ctrl_down = self._control_key_down(event.modifiers())
        alt_down = event.modifiers() & QtCore.Qt.KeyboardModifier.AltModifier
        shift_down = event.modifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier

        # Special sequences ----------------------------------------------

        if event.matches(QtGui.QKeySequence.StandardKey.Copy):
            self.copy()
            intercepted = True

        elif event.matches(QtGui.QKeySequence.StandardKey.Cut):
            self.cut()
            intercepted = True

        elif event.matches(QtGui.QKeySequence.StandardKey.Paste):
            self.paste()
            intercepted = True

        # Special modifier logic -----------------------------------------

        elif key in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
            intercepted = True

            # Special handling when tab completing in text mode.
            self._cancel_text_completion()

            if self._in_buffer(position):
                if self._reading:
                    self._append_plain_text("\n")
                    self._reading = False
                    if self._reading_callback:
                        self._reading_callback()

                # If the input buffer is a single line or there is only
                # whitespace after the cursor, execute. Otherwise, split the
                # line with a continuation prompt.
                elif not self._executing:
                    cursor.movePosition(
                        QtGui.QTextCursor.MoveOperation.End, QtGui.QTextCursor.MoveMode.KeepAnchor
                    )
                    at_end = len(cursor.selectedText().strip()) == 0
                    single_line = (
                        self._get_end_cursor().blockNumber()
                        == self._get_prompt_cursor().blockNumber()
                    )
                    if (at_end or shift_down or single_line) and not ctrl_down:
                        self.execute(interactive=not shift_down)
                    else:
                        # Do this inside an edit block for clean undo/redo.
                        cursor.beginEditBlock()
                        cursor.setPosition(position)
                        cursor.insertText("\n")
                        self._insert_continuation_prompt(cursor)
                        cursor.endEditBlock()

                        # Ensure that the whole input buffer is visible.
                        # FIXME: This will not be usable if the input buffer is
                        # taller than the console widget.
                        self._control.moveCursor(QtGui.QTextCursor.MoveOperation.End)
                        self._control.setTextCursor(cursor)

        # Control/Cmd modifier -------------------------------------------

        elif ctrl_down:
            if key == QtCore.Qt.Key.Key_G:
                self._keyboard_quit()
                intercepted = True

            elif key == QtCore.Qt.Key.Key_K:
                if self._in_buffer(position):
                    cursor.movePosition(
                        QtGui.QTextCursor.MoveOperation.EndOfLine,
                        QtGui.QTextCursor.MoveMode.KeepAnchor,
                    )
                    if not cursor.hasSelection():
                        # Line deletion (remove continuation prompt)
                        cursor.movePosition(
                            QtGui.QTextCursor.MoveOperation.NextBlock,
                            QtGui.QTextCursor.MoveMode.KeepAnchor,
                        )
                        cursor.movePosition(
                            QtGui.QTextCursor.MoveOperation.Right,
                            QtGui.QTextCursor.MoveMode.KeepAnchor,
                            len(self._continuation_prompt),
                        )
                    cursor.removeSelectedText()
                intercepted = True

            elif key == QtCore.Qt.Key.Key_L:
                self.prompt_to_top()
                intercepted = True

            elif key == QtCore.Qt.Key.Key_O:
                if self._page_control and self._page_control.isVisible():
                    self._page_control.setFocus()
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Y:
                self.paste()
                intercepted = True

            elif key in (QtCore.Qt.Key.Key_Backspace, QtCore.Qt.Key.Key_Delete):
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Plus:
                self.change_font_size(1)
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Minus:
                self.change_font_size(-1)
                intercepted = True

        # Alt modifier ---------------------------------------------------

        elif alt_down:
            if key == QtCore.Qt.Key.Key_B:
                self._set_cursor(self._get_word_start_cursor(position))
                intercepted = True

            elif key == QtCore.Qt.Key.Key_F:
                self._set_cursor(self._get_word_end_cursor(position))
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Backspace:
                cursor = self._get_word_start_cursor(position)
                cursor.setPosition(position, QtGui.QTextCursor.MoveMode.KeepAnchor)
                cursor.removeSelectedText()
                intercepted = True

            elif key == QtCore.Qt.Key.Key_D:
                cursor = self._get_word_end_cursor(position)
                cursor.setPosition(position, QtGui.QTextCursor.MoveMode.KeepAnchor)
                cursor.removeSelectedText()
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Delete:
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Greater:
                self._control.moveCursor(QtGui.QTextCursor.MoveOperation.End)
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Less:
                self._control.setTextCursor(self._get_prompt_cursor())
                intercepted = True

        # No modifiers ---------------------------------------------------

        else:
            if shift_down:
                anchormode = QtGui.QTextCursor.MoveMode.KeepAnchor
            else:
                anchormode = QtGui.QTextCursor.MoveMode.MoveAnchor

            if key == QtCore.Qt.Key.Key_Escape:
                self._keyboard_quit()
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Up:
                if self._reading or not self._up_pressed():
                    intercepted = True
                else:
                    prompt_line = self._get_prompt_cursor().blockNumber()
                    intercepted = cursor.blockNumber() <= prompt_line

            elif key == QtCore.Qt.Key.Key_Down:
                if self._reading or not self._down_pressed():
                    intercepted = True
                else:
                    end_line = self._get_end_cursor().blockNumber()
                    intercepted = cursor.blockNumber() == end_line

            elif key == QtCore.Qt.Key.Key_Tab:
                if not self._reading:
                    intercepted = not self._tab_pressed()

            elif key == QtCore.Qt.Key.Key_Left:

                # Move to the previous line
                line, col = cursor.blockNumber(), cursor.columnNumber()
                if line > self._get_prompt_cursor().blockNumber() and col == len(
                    self._continuation_prompt
                ):
                    self._control.moveCursor(
                        QtGui.QTextCursor.MoveOperation.PreviousBlock, mode=anchormode
                    )
                    self._control.moveCursor(
                        QtGui.QTextCursor.MoveOperation.EndOfBlock, mode=anchormode
                    )
                    intercepted = True

                # Regular left movement
                else:
                    intercepted = not self._in_buffer(position - 1)

            elif key == QtCore.Qt.Key.Key_Right:
                original_block_number = cursor.blockNumber()
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right, mode=anchormode)
                if cursor.blockNumber() != original_block_number:
                    cursor.movePosition(
                        QtGui.QTextCursor.MoveOperation.Right,
                        n=len(self._continuation_prompt),
                        mode=anchormode,
                    )
                self._set_cursor(cursor)
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Home:
                start_line = cursor.blockNumber()
                if start_line == self._get_prompt_cursor().blockNumber():
                    start_pos = self._prompt_pos
                else:
                    cursor.movePosition(
                        QtGui.QTextCursor.MoveOperation.StartOfBlock,
                        QtGui.QTextCursor.MoveMode.KeepAnchor,
                    )
                    start_pos = cursor.position()
                    start_pos += len(self._continuation_prompt)
                    cursor.setPosition(position)
                if shift_down and self._in_buffer(position):
                    cursor.setPosition(start_pos, QtGui.QTextCursor.MoveMode.KeepAnchor)
                else:
                    cursor.setPosition(start_pos)
                self._set_cursor(cursor)
                intercepted = True

            elif key == QtCore.Qt.Key.Key_Backspace:

                # Line deletion (remove continuation prompt)
                line, col = cursor.blockNumber(), cursor.columnNumber()
                if (
                    not self._reading
                    and col == len(self._continuation_prompt)
                    and line > self._get_prompt_cursor().blockNumber()
                ):
                    cursor.beginEditBlock()
                    cursor.movePosition(
                        QtGui.QTextCursor.MoveOperation.StartOfBlock,
                        QtGui.QTextCursor.MoveMode.KeepAnchor,
                    )
                    cursor.removeSelectedText()
                    cursor.deletePreviousChar()
                    cursor.endEditBlock()
                    intercepted = True

                # Regular backwards deletion
                else:
                    anchor = cursor.anchor()
                    if anchor == position:
                        intercepted = not self._in_buffer(position - 1)
                    else:
                        intercepted = not self._in_buffer(
                            min(anchor, position)
                        )

            elif key == QtCore.Qt.Key.Key_Delete:

                # Line deletion (remove continuation prompt)
                if (
                    not self._reading
                    and self._in_buffer(position)
                    and cursor.atBlockEnd()
                    and not cursor.hasSelection()
                ):
                    cursor.movePosition(
                        QtGui.QTextCursor.MoveOperation.NextBlock,
                        QtGui.QTextCursor.MoveMode.KeepAnchor,
                    )
                    cursor.movePosition(
                        QtGui.QTextCursor.MoveOperation.Right,
                        QtGui.QTextCursor.MoveMode.KeepAnchor,
                        len(self._continuation_prompt),
                    )
                    cursor.removeSelectedText()
                    intercepted = True

                # Regular forwards deletion:
                else:
                    anchor = cursor.anchor()
                    intercepted = not self._in_buffer(
                        anchor
                    ) or not self._in_buffer(position)

        # Don't move the cursor if Control/Cmd is pressed to allow copy-paste
        # using the keyboard in any part of the buffer.
        if not self._control_key_down(event.modifiers(), include_command=True):
            self._keep_cursor_in_buffer()

        return intercepted

    def _event_filter_page_keypress(self, event):
        """ Filter key events for the paging widget to create console-like
            interface.
        """
        key = event.key()
        ctrl_down = self._control_key_down(event.modifiers())
        alt_down = event.modifiers() & QtCore.Qt.KeyboardModifier.AltModifier

        if ctrl_down:
            if key == QtCore.Qt.Key.Key_O:
                self._control.setFocus()
                return True

        elif alt_down:
            if key == QtCore.Qt.Key.Key_Greater:
                self._page_control.moveCursor(QtGui.QTextCursor.MoveOperation.End)
                return True

            elif key == QtCore.Qt.Key.Key_Less:
                self._page_control.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
                return True

        elif key in (QtCore.Qt.Key.Key_Q, QtCore.Qt.Key.Key_Escape):
            if self._splitter:
                self._page_control.hide()
            else:
                self.layout().setCurrentWidget(self._control)
            return True

        elif key in (QtCore.Qt.Key.Key_Enter, QtCore.Qt.Key.Key_Return):
            new_event = QtGui.QKeyEvent(
                QtCore.QEvent.Type.KeyPress,
                QtCore.Qt.Key.Key_PageDown,
                QtCore.Qt.KeyboardModifier.NoModifier,
            )
            QtGui.QApplication.sendEvent(self._page_control, new_event)
            return True

        elif key == QtCore.Qt.Key.Key_Backspace:
            new_event = QtGui.QKeyEvent(
                QtCore.QEvent.Type.KeyPress,
                QtCore.Qt.Key.Key_PageUp,
                QtCore.Qt.KeyboardModifier.NoModifier,
            )
            QtGui.QApplication.sendEvent(self._page_control, new_event)
            return True

        return False

    def _format_as_columns(self, items, separator="  "):
        """ Transform a list of strings into a single string with columns.

        Parameters
        ----------
        items : sequence of strings
            The strings to process.

        separator : str, optional [default is two spaces]
            The string that separates columns.

        Returns
        -------
        The formatted string.
        """
        # Note: this code is adapted from columnize 0.3.2.
        # See http://code.google.com/p/pycolumnize/

        # Calculate the number of characters available.
        width = self._control.viewport().width()
        char_width = QtGui.QFontMetrics(self.font).width(" ")
        displaywidth = max(10, (width / char_width) - 1)

        # Some degenerate cases.
        size = len(items)
        if size == 0:
            return "\n"
        elif size == 1:
            return "%s\n" % items[0]

        # Try every row count from 1 upwards
        array_index = lambda nrows, row, col: nrows * col + row
        for nrows in range(1, size):
            ncols = (size + nrows - 1) // nrows
            colwidths = []
            totwidth = -len(separator)
            for col in range(ncols):
                # Get max column width for this column
                colwidth = 0
                for row in range(nrows):
                    i = array_index(nrows, row, col)
                    if i >= size:
                        break
                    x = items[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + len(separator)
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break

        # The smallest number of rows computed and the max widths for each
        # column has been obtained. Now we just have to format each of the rows.
        string = ""
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows * col
                if i >= size:
                    texts.append("")
                else:
                    texts.append(items[i])
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            string += "%s\n" % separator.join(texts)
        return string

    def _get_block_plain_text(self, block):
        """ Given a QTextBlock, return its unformatted text.
        """
        cursor = QtGui.QTextCursor(block)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.EndOfBlock, QtGui.QTextCursor.MoveMode.KeepAnchor
        )
        return cursor.selection().toPlainText()

    def _get_cursor(self):
        """ Convenience method that returns a cursor for the current position.
        """
        return self._control.textCursor()

    def _get_end_cursor(self):
        """ Convenience method that returns a cursor for the last character.
        """
        cursor = self._control.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        return cursor

    def _get_input_buffer_cursor_column(self):
        """ Returns the column of the cursor in the input buffer, excluding the
            contribution by the prompt, or -1 if there is no such column.
        """
        prompt = self._get_input_buffer_cursor_prompt()
        if prompt is None:
            return -1
        else:
            cursor = self._control.textCursor()
            return cursor.columnNumber() - len(prompt)

    def _get_input_buffer_cursor_line(self):
        """ Returns the text of the line of the input buffer that contains the
            cursor, or None if there is no such line.
        """
        prompt = self._get_input_buffer_cursor_prompt()
        if prompt is None:
            return None
        else:
            cursor = self._control.textCursor()
            text = self._get_block_plain_text(cursor.block())
            return text[len(prompt):]

    def _get_input_buffer_cursor_prompt(self):
        """ Returns the (plain text) prompt for line of the input buffer that
            contains the cursor, or None if there is no such line.
        """
        if self._executing:
            return None
        cursor = self._control.textCursor()
        if cursor.position() >= self._prompt_pos:
            if cursor.blockNumber() == self._get_prompt_cursor().blockNumber():
                return self._prompt
            else:
                return self._continuation_prompt
        else:
            return None

    def _get_prompt_cursor(self):
        """ Convenience method that returns a cursor for the prompt position.
        """
        cursor = self._control.textCursor()
        cursor.setPosition(self._prompt_pos)
        return cursor

    def _get_selection_cursor(self, start, end):
        """ Convenience method that returns a cursor with text selected between
            the positions 'start' and 'end'.
        """
        cursor = self._control.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QtGui.QTextCursor.MoveMode.KeepAnchor)
        return cursor

    def _get_word_start_cursor(self, position):
        """ Find the start of the word to the left the given position. If a
            sequence of non-word characters precedes the first word, skip over
            them. (This emulates the behavior of bash, emacs, etc.)
        """
        document = self._control.document()
        position -= 1
        while position >= self._prompt_pos and not is_letter_or_number(
            document.characterAt(position)
        ):
            position -= 1
        while position >= self._prompt_pos and is_letter_or_number(
            document.characterAt(position)
        ):
            position -= 1
        cursor = self._control.textCursor()
        cursor.setPosition(position + 1)
        return cursor

    def _get_word_end_cursor(self, position):
        """ Find the end of the word to the right the given position. If a
            sequence of non-word characters precedes the first word, skip over
            them. (This emulates the behavior of bash, emacs, etc.)
        """
        document = self._control.document()
        end = self._get_end_cursor().position()
        while position < end and not is_letter_or_number(
            document.characterAt(position)
        ):
            position += 1
        while position < end and is_letter_or_number(
            document.characterAt(position)
        ):
            position += 1
        cursor = self._control.textCursor()
        cursor.setPosition(position)
        return cursor

    def _insert_continuation_prompt(self, cursor):
        """ Inserts new continuation prompt using the specified cursor.
        """
        if self._continuation_prompt_html is None:
            self._insert_plain_text(cursor, self._continuation_prompt)
        else:
            self._continuation_prompt = self._insert_html_fetching_plain_text(
                cursor, self._continuation_prompt_html
            )

    def _insert_html(self, cursor, html):
        """ Inserts HTML using the specified cursor in such a way that future
            formatting is unaffected.
        """
        cursor.beginEditBlock()
        cursor.insertHtml(html)

        # After inserting HTML, the text document "remembers" it's in "html
        # mode", which means that subsequent calls adding plain text will result
        # in unwanted formatting, lost tab characters, etc. The following code
        # hacks around this behavior, which I consider to be a bug in Qt, by
        # (crudely) resetting the document's style state.
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.Left, QtGui.QTextCursor.MoveMode.KeepAnchor
        )
        if cursor.selection().toPlainText() == " ":
            cursor.removeSelectedText()
        else:
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right)
        cursor.insertText(" ", QtGui.QTextCharFormat())
        cursor.endEditBlock()

    def _insert_html_fetching_plain_text(self, cursor, html):
        """ Inserts HTML using the specified cursor, then returns its plain text
            version.
        """
        cursor.beginEditBlock()
        cursor.removeSelectedText()

        start = cursor.position()
        self._insert_html(cursor, html)
        end = cursor.position()
        cursor.setPosition(start, QtGui.QTextCursor.MoveMode.KeepAnchor)
        text = cursor.selection().toPlainText()

        cursor.setPosition(end)
        cursor.endEditBlock()
        return text

    def _insert_plain_text(self, cursor, text):
        """ Inserts plain text using the specified cursor, processing ANSI codes
            if enabled.
        """
        cursor.insertText(text)

    def _insert_plain_text_into_buffer(self, cursor, text):
        """ Inserts text into the input buffer using the specified cursor (which
            must be in the input buffer), ensuring that continuation prompts are
            inserted as necessary.
        """
        lines = text.splitlines(True)
        if lines:
            cursor.beginEditBlock()
            cursor.insertText(lines[0])
            for line in lines[1:]:
                if self._continuation_prompt_html is None:
                    cursor.insertText(self._continuation_prompt)
                else:
                    self._continuation_prompt = self._insert_html_fetching_plain_text(
                        cursor, self._continuation_prompt_html
                    )
                cursor.insertText(line)
            cursor.endEditBlock()

    def _in_buffer(self, position=None):
        """ Returns whether the current cursor (or, if specified, a position) is
            inside the editing region.
        """
        cursor = self._control.textCursor()
        if position is None:
            position = cursor.position()
        else:
            cursor.setPosition(position)
        line = cursor.blockNumber()
        prompt_line = self._get_prompt_cursor().blockNumber()
        if line == prompt_line:
            return position >= self._prompt_pos
        elif line > prompt_line:
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
            prompt_pos = cursor.position() + len(self._continuation_prompt)
            return position >= prompt_pos
        return False

    def _keep_cursor_in_buffer(self):
        """ Ensures that the cursor is inside the editing region. Returns
            whether the cursor was moved.
        """
        moved = not self._in_buffer()
        if moved:
            cursor = self._control.textCursor()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
            self._control.setTextCursor(cursor)
        return moved

    def _keyboard_quit(self):
        """ Cancels the current editing task ala Ctrl-G in Emacs.
        """
        if self._text_completing_pos:
            self._cancel_text_completion()
        else:
            self.input_buffer = ""

    def _page(self, text, html=False):
        """ Displays text using the pager if it exceeds the height of the
        viewport.

        Parameters:
        -----------
        html : bool, optional (default False)
            If set, the text will be interpreted as HTML instead of plain text.
        """
        line_height = QtGui.QFontMetrics(self.font).height()
        minlines = self._control.viewport().height() / line_height
        if self.paging != "none" and re.match(
            "(?:[^\n]*\n){%i}" % minlines, text
        ):
            if self.paging == "custom":
                self.custom_page_requested.emit(text)
            else:
                self._page_control.clear()
                cursor = self._page_control.textCursor()
                if html:
                    self._insert_html(cursor, text)
                else:
                    self._insert_plain_text(cursor, text)
                self._page_control.moveCursor(QtGui.QTextCursor.MoveOperation.Start)

                self._page_control.viewport().resize(self._control.size())
                if self._splitter:
                    self._page_control.show()
                    self._page_control.setFocus()
                else:
                    self.layout().setCurrentWidget(self._page_control)
        elif html:
            self._append_plain_html(text)
        else:
            self._append_plain_text(text)

    def _prompt_finished(self):
        """ Called immediately after a prompt is finished, i.e. when some input
            will be processed and a new prompt displayed.
        """
        self._control.setReadOnly(True)
        self._prompt_finished_hook()

    def _prompt_started(self):
        """ Called immediately after a new prompt is displayed.
        """
        # Temporarily disable the maximum block count to permit undo/redo and
        # to ensure that the prompt position does not change due to truncation.
        self._control.document().setMaximumBlockCount(0)
        self._control.setUndoRedoEnabled(True)

        self._control.setReadOnly(False)
        self._control.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self._executing = False
        self._prompt_started_hook()

    def _readline(self, prompt="", callback=None):
        """ Reads one line of input from the user.

        Parameters
        ----------
        prompt : str, optional
            The prompt to print before reading the line.

        callback : callable, optional
            A callback to execute with the read line. If not specified, input is
            read *synchronously* and this method does not return until it has
            been read.

        Returns
        -------
        If a callback is specified, returns nothing. Otherwise, returns the
        input string with the trailing newline stripped.
        """
        if self._reading:
            raise RuntimeError(
                "Cannot read a line. Widget is already reading."
            )

        if not callback and not self.isVisible():
            # If the user cannot see the widget, this function cannot return.
            raise RuntimeError(
                "Cannot synchronously read a line if the widget "
                "is not visible!"
            )

        self._reading = True
        self._show_prompt(prompt, newline=False)

        if callback is None:
            self._reading_callback = None
            while self._reading:
                QtCore.QCoreApplication.processEvents()
            return self.input_buffer.rstrip("\n")

        else:
            self._reading_callback = lambda: callback(
                self.input_buffer.rstrip("\n")
            )

    def _set_continuation_prompt(self, prompt, html=False):
        """ Sets the continuation prompt.

        Parameters
        ----------
        prompt : str
            The prompt to show when more input is needed.

        html : bool, optional (default False)
            If set, the prompt will be inserted as formatted HTML. Otherwise,
            the prompt will be treated as plain text, though ANSI color codes
            will be handled.
        """
        if html:
            self._continuation_prompt_html = prompt
        else:
            self._continuation_prompt = prompt
            self._continuation_prompt_html = None

    def _set_cursor(self, cursor):
        """ Convenience method to set the current cursor.
        """
        self._control.setTextCursor(cursor)

    def _set_top_cursor(self, cursor):
        """ Scrolls the viewport so that the specified cursor is at the top.
        """
        scrollbar = self._control.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        original_cursor = self._control.textCursor()
        self._control.setTextCursor(cursor)
        self._control.ensureCursorVisible()
        self._control.setTextCursor(original_cursor)

    def _show_prompt(self, prompt=None, html=False, newline=True):
        """ Writes a new prompt at the end of the buffer.

        Parameters
        ----------
        prompt : str, optional
            The prompt to show. If not specified, the previous prompt is used.

        html : bool, optional (default False)
            Only relevant when a prompt is specified. If set, the prompt will
            be inserted as formatted HTML. Otherwise, the prompt will be treated
            as plain text, though ANSI color codes will be handled.

        newline : bool, optional (default True)
            If set, a new line will be written before showing the prompt if
            there is not already a newline at the end of the buffer.
        """
        # Insert a preliminary newline, if necessary.
        if newline:
            cursor = self._get_end_cursor()
            if cursor.position() > 0:
                cursor.movePosition(
                    QtGui.QTextCursor.MoveOperation.Left, QtGui.QTextCursor.MoveMode.KeepAnchor
                )
                if cursor.selection().toPlainText() != "\n":
                    self._append_plain_text("\n")

        # Write the prompt.
        self._append_plain_text(self._prompt_sep)
        if prompt is None:
            if self._prompt_html is None:
                self._append_plain_text(self._prompt)
            else:
                self._append_html(self._prompt_html)
        else:
            if html:
                self._prompt = self._append_html_fetching_plain_text(prompt)
                self._prompt_html = prompt
            else:
                self._append_plain_text(prompt)
                self._prompt = prompt
                self._prompt_html = None

        self._prompt_pos = self._get_end_cursor().position()
        self._prompt_started()

    # Signal handlers ----------------------------------------------------

    def _adjust_scrollbars(self):
        """ Expands the vertical scrollbar beyond the range set by Qt.
        """
        # This code is adapted from _q_adjustScrollbars in qplaintextedit.cpp
        # and qtextedit.cpp.
        document = self._control.document()
        scrollbar = self._control.verticalScrollBar()
        viewport_height = self._control.viewport().height()
        if isinstance(self._control, QtGui.QPlainTextEdit):
            maximum = max(0, document.lineCount() - 1)
            step = viewport_height / self._control.fontMetrics().lineSpacing()
        else:
            # QTextEdit does not do line-based layout and blocks will not in
            # general have the same height. Therefore it does not make sense to
            # attempt to scroll in line height increments.
            maximum = document.size().height()
            step = viewport_height
        diff = maximum - scrollbar.maximum()
        scrollbar.setRange(0, maximum)
        scrollbar.setPageStep(int(step))
        # Compensate for undesirable scrolling that occurs automatically due to
        # maximumBlockCount() text truncation.
        if diff < 0 and document.blockCount() == document.maximumBlockCount():
            scrollbar.setValue(scrollbar.value() + diff)

    def _cursor_position_changed(self):
        """ Clears the temporary buffer based on the cursor position.
        """
        if self._text_completing_pos:
            document = self._control.document()
            if self._text_completing_pos < document.characterCount():
                cursor = self._control.textCursor()
                pos = cursor.position()
                text_cursor = self._control.textCursor()
                text_cursor.setPosition(self._text_completing_pos)
                if (
                    pos < self._text_completing_pos
                    or cursor.blockNumber() > text_cursor.blockNumber()
                ):
                    self._clear_temporary_buffer()
                    self._text_completing_pos = 0
            else:
                self._clear_temporary_buffer()
                self._text_completing_pos = 0

    def _custom_context_menu_requested(self, pos):
        """ Shows a context menu at the given QPoint (in widget coordinates).
        """
        menu = self._context_menu_make(pos)
        menu.exec_(self._control.mapToGlobal(pos))
