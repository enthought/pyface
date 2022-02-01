# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
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


from .find_widget import FindWidget
from .gutters import LineNumberWidget, StatusGutterWidget
from .replace_widget import ReplaceWidget
from .pygments_highlighter import PygmentsHighlighter


class CodeWidget(QtGui.QPlainTextEdit):
    """ A widget for viewing and editing code.
    """

    # ------------------------------------------------------------------------
    # CodeWidget interface
    # ------------------------------------------------------------------------
    focus_lost = QtCore.Signal()

    def __init__(
        self, parent, should_highlight_current_line=False, font=None, lexer=None
    ):
        super().__init__(parent)

        self.highlighter = PygmentsHighlighter(self.document(), lexer)
        self.line_number_widget = LineNumberWidget(self)
        self.status_widget = StatusGutterWidget(self)

        if font is None:
            # Set a decent fixed width font for this platform.
            font = QtGui.QFont()
            if sys.platform == "win32":
                # Prefer Consolas, but fall back to Courier if necessary.
                font.setFamily("Consolas")
                if not font.exactMatch():
                    font.setFamily("Courier")
            elif sys.platform == "darwin":
                font.setFamily("Monaco")
            else:
                font.setFamily("Monospace")
            font.setStyleHint(QtGui.QFont.TypeWriter)
        self.set_font(font)

        # Whether we should highlight the current line or not.
        self.should_highlight_current_line = should_highlight_current_line

        # What that highlight color should be.
        self.line_highlight_color = self.palette().alternateBase()

        # Auto-indentation behavior
        self.auto_indent = True
        self.smart_backspace = True

        # Tab settings
        self.tabs_as_spaces = True
        self.tab_width = 4

        self.indent_character = ":"
        self.comment_character = "#"

        # Set up gutter widget and current line highlighting
        self.blockCountChanged.connect(self.update_line_number_width)
        self.updateRequest.connect(self.update_line_numbers)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_width()
        self.highlight_current_line()

        # Don't wrap text
        self.setLineWrapMode(QtGui.QPlainTextEdit.LineWrapMode.NoWrap)

        # Key bindings
        self.indent_key = QtGui.QKeySequence(QtCore.Qt.Key.Key_Tab)
        self.unindent_key = QtGui.QKeySequence(
            QtCore.Qt.Modifier.SHIFT + QtCore.Qt.Key.Key_Backtab
        )
        self.comment_key = QtGui.QKeySequence(
            QtCore.Qt.Modifier.CTRL + QtCore.Qt.Key.Key_Slash
        )
        self.backspace_key = QtGui.QKeySequence(QtCore.Qt.Key.Key_Backspace)

    def _remove_event_listeners(self):
        self.blockCountChanged.disconnect(self.update_line_number_width)
        self.updateRequest.disconnect(self.update_line_numbers)
        self.cursorPositionChanged.disconnect(self.highlight_current_line)

    def lines(self):
        """ Return the number of lines.
        """
        return self.blockCount()

    def set_line_column(self, line, column):
        """ Move the cursor to a particular line/column number.

        These line and column numbers are 1-indexed.
        """
        # Allow the caller to ignore either line or column by passing None.
        line0, col0 = self.get_line_column()
        if line is None:
            line = line0
        if column is None:
            column = col0
        line -= 1
        column -= 1
        block = self.document().findBlockByLineNumber(line)
        line_start = block.position()
        position = line_start + column
        cursor = self.textCursor()
        cursor.setPosition(position)
        self.setTextCursor(cursor)

    def get_line_column(self):
        """ Get the current line and column numbers.

        These line and column numbers are 1-indexed.
        """
        cursor = self.textCursor()
        pos = cursor.position()
        line = cursor.blockNumber() + 1
        line_start = cursor.block().position()
        column = pos - line_start + 1
        return line, column

    def get_selected_text(self):
        """ Return the currently selected text.
        """
        return str(self.textCursor().selectedText())

    def set_font(self, font):
        """ Set the new QFont.
        """
        self.document().setDefaultFont(font)
        self.line_number_widget.set_font(font)
        self.update_line_number_width()

    def update_line_number_width(self, nblocks=0):
        """ Update the width of the line number widget.
        """
        left = 0
        if not self.line_number_widget.isHidden():
            left = self.line_number_widget.digits_width()
        self.setViewportMargins(left, 0, 0, 0)

    def update_line_numbers(self, rect, dy):
        """ Update the line numbers.
        """
        if dy:
            self.line_number_widget.scroll(0, dy)
        self.line_number_widget.update(
            0, rect.y(), self.line_number_widget.width(), rect.height()
        )
        if rect.contains(self.viewport().rect()):
            self.update_line_number_width()

    def set_info_lines(self, info_lines):
        self.status_widget.info_lines = info_lines
        self.status_widget.update()

    def set_warn_lines(self, warn_lines):
        self.status_widget.warn_lines = warn_lines
        self.status_widget.update()

    def set_error_lines(self, error_lines):
        self.status_widget.error_lines = error_lines
        self.status_widget.update()

    def highlight_current_line(self):
        """ Highlight the line with the cursor.
        """
        if self.should_highlight_current_line:
            selection = QtGui.QTextEdit.ExtraSelection()
            selection.format.setBackground(self.line_highlight_color)
            selection.format.setProperty(
                QtGui.QTextFormat.Property.FullWidthSelection, True
            )
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            self.setExtraSelections([selection])

    def autoindent_newline(self):
        tab = "\t"
        if self.tabs_as_spaces:
            tab = " " * self.tab_width

        cursor = self.textCursor()
        text = cursor.block().text()
        trimmed = text.rstrip()
        current_indent_pos = self._get_indent_position(text)

        cursor.beginEditBlock()

        # Create the new line. There is no need to move to the new block, as
        # the insertBlock will do that automatically
        cursor.insertBlock()

        # Remove any leading whitespace from the current line
        after = cursor.block().text()
        trimmed_after = after.rstrip()
        pos = after.index(trimmed_after)
        for i in range(pos):
            cursor.deleteChar()

        if self.indent_character and trimmed.endswith(self.indent_character):
            # indent one level
            indent = text[:current_indent_pos] + tab
        else:
            # indent to the same level
            indent = text[:current_indent_pos]
        cursor.insertText(indent)

        cursor.endEditBlock()
        self.ensureCursorVisible()

    def block_indent(self):
        cursor = self.textCursor()

        if not cursor.hasSelection():
            # Insert a tabulator
            self.line_indent(cursor)

        else:
            # Indent every selected line
            sel_blocks = self._get_selected_blocks()

            cursor.clearSelection()
            cursor.beginEditBlock()

            for block in sel_blocks:
                cursor.setPosition(block.position())
                self.line_indent(cursor)

            cursor.endEditBlock()
            self._show_selected_blocks(sel_blocks)

    def block_unindent(self):
        cursor = self.textCursor()

        if not cursor.hasSelection():
            # Unindent current line
            position = cursor.position()
            cursor.beginEditBlock()

            removed = self.line_unindent(cursor)
            position = max(position - removed, 0)

            cursor.endEditBlock()
            cursor.setPosition(position)
            self.setTextCursor(cursor)

        else:
            # Unindent every selected line
            sel_blocks = self._get_selected_blocks()

            cursor.clearSelection()
            cursor.beginEditBlock()

            for block in sel_blocks:
                cursor.setPosition(block.position())
                self.line_unindent(cursor)

            cursor.endEditBlock()
            self._show_selected_blocks(sel_blocks)

    def block_comment(self):
        """the comment char will be placed at the first non-whitespace
            char of the first line. For example:
                if foo:
                    bar
            will be commented as:
                #if foo:
                #    bar
        """
        cursor = self.textCursor()

        if not cursor.hasSelection():
            text = cursor.block().text()
            current_indent_pos = self._get_indent_position(text)

            if text[current_indent_pos] == self.comment_character:
                self.line_uncomment(cursor, current_indent_pos)
            else:
                self.line_comment(cursor, current_indent_pos)

        else:
            sel_blocks = self._get_selected_blocks()
            text = sel_blocks[0].text()
            indent_pos = self._get_indent_position(text)

            comment = True
            for block in sel_blocks:
                text = block.text()
                if (
                    len(text) > indent_pos
                    and text[indent_pos] == self.comment_character
                ):
                    # Already commented.
                    comment = False
                    break

            cursor.clearSelection()
            cursor.beginEditBlock()

            for block in sel_blocks:
                cursor.setPosition(block.position())
                if comment:
                    if block.length() < indent_pos:
                        cursor.insertText(" " * indent_pos)
                    self.line_comment(cursor, indent_pos)
                else:
                    self.line_uncomment(cursor, indent_pos)
            cursor.endEditBlock()
            self._show_selected_blocks(sel_blocks)

    def line_comment(self, cursor, position):
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.Right, QtGui.QTextCursor.MoveMode.MoveAnchor, position
        )
        cursor.insertText(self.comment_character)

    def line_uncomment(self, cursor, position=0):
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        text = cursor.block().text()
        new_text = text[:position] + text[position + 1:]
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.EndOfBlock, QtGui.QTextCursor.MoveMode.KeepAnchor
        )
        cursor.removeSelectedText()
        cursor.insertText(new_text)

    def line_indent(self, cursor):
        tab = "\t"
        if self.tabs_as_spaces:
            tab = "    "

        cursor.insertText(tab)

    def line_unindent(self, cursor):
        """ Unindents the cursor's line. Returns the number of characters
            removed.
        """
        tab = "\t"
        if self.tabs_as_spaces:
            tab = "    "

        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        if cursor.block().text().startswith(tab):
            new_text = cursor.block().text()[len(tab):]
            cursor.movePosition(
                QtGui.QTextCursor.MoveOperation.EndOfBlock, QtGui.QTextCursor.MoveMode.KeepAnchor
            )
            cursor.removeSelectedText()
            cursor.insertText(new_text)
            return len(tab)
        else:
            return 0

    def word_under_cursor(self):
        """ Return the word under the cursor.
        """
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)
        return str(cursor.selectedText())

    # ------------------------------------------------------------------------
    # QWidget interface
    # ------------------------------------------------------------------------

    # FIXME: This is a quick hack to be able to access the keyPressEvent
    # from the rest editor. This should be changed to work within the traits
    # framework.
    def keyPressEvent_action(self, event):
        pass

    def keyPressEvent(self, event):
        if self.isReadOnly():
            return super().keyPressEvent(event)

        key_sequence = QtGui.QKeySequence(event.key() + int(event.modifiers()))

        self.keyPressEvent_action(event)  # FIXME: see above

        # If the cursor is in the middle of the first line, pressing the "up"
        # key causes the cursor to go to the start of the first line, i.e. the
        # beginning of the document. Likewise, if the cursor is somewhere in the
        # last line, the "down" key causes it to go to the end.
        cursor = self.textCursor()
        if key_sequence.matches(QtGui.QKeySequence(QtCore.Qt.Key.Key_Up)):
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
            if cursor.atStart():
                self.setTextCursor(cursor)
                event.accept()
        elif key_sequence.matches(QtGui.QKeySequence(QtCore.Qt.Key.Key_Down)):
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine)
            if cursor.atEnd():
                self.setTextCursor(cursor)
                event.accept()

        elif self.auto_indent and key_sequence.matches(
            QtGui.QKeySequence(QtCore.Qt.Key.Key_Return)
        ):
            event.accept()
            return self.autoindent_newline()
        elif key_sequence.matches(self.indent_key):
            event.accept()
            return self.block_indent()
        elif key_sequence.matches(self.unindent_key):
            event.accept()
            return self.block_unindent()
        elif key_sequence.matches(self.comment_key):
            event.accept()
            return self.block_comment()
        elif (
            self.auto_indent
            and self.smart_backspace
            and key_sequence.matches(self.backspace_key)
            and self._backspace_should_unindent()
        ):
            event.accept()
            return self.block_unindent()

        return super().keyPressEvent(event)

    def resizeEvent(self, event):
        QtGui.QPlainTextEdit.resizeEvent(self, event)
        contents = self.contentsRect()
        self.line_number_widget.setGeometry(
            QtCore.QRect(
                contents.left(),
                contents.top(),
                self.line_number_widget.digits_width(),
                contents.height(),
            )
        )

        # use the viewport width to determine the right edge. This allows for
        # the propper placement w/ and w/o the scrollbar
        right_pos = (
            self.viewport().width()
            + self.line_number_widget.width()
            + 1
            - self.status_widget.sizeHint().width()
        )
        self.status_widget.setGeometry(
            QtCore.QRect(
                right_pos,
                contents.top(),
                self.status_widget.sizeHint().width(),
                contents.height(),
            )
        )

    def focusOutEvent(self, event):
        QtGui.QPlainTextEdit.focusOutEvent(self, event)
        self.focus_lost.emit()

    def sizeHint(self):
        # Suggest a size that is 80 characters wide and 40 lines tall.
        style = self.style()
        opt = QtGui.QStyleOptionHeader()
        font_metrics = QtGui.QFontMetrics(self.document().defaultFont())
        # QFontMetrics.width() is deprecated and Qt docs suggest using
        # horizontalAdvance() instead, but is only available since Qt 5.11
        if QtCore.__version_info__ >= (5, 11):
            width = font_metrics.horizontalAdvance(" ") * 80
        else:
            width = font_metrics.width(" ") * 80
        width += self.line_number_widget.sizeHint().width()
        width += self.status_widget.sizeHint().width()
        width += style.pixelMetric(QtGui.QStyle.PixelMetric.PM_ScrollBarExtent, opt, self)
        height = font_metrics.height() * 40
        return QtCore.QSize(width, height)

    # ------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------

    def _get_indent_position(self, line):
        trimmed = line.rstrip()
        if len(trimmed) != 0:
            return line.index(trimmed)
        else:
            # if line is all spaces, treat it as the indent position
            return len(line)

    def _show_selected_blocks(self, selected_blocks):
        """ Assumes contiguous blocks
        """
        cursor = self.textCursor()
        cursor.clearSelection()
        cursor.setPosition(selected_blocks[0].position())
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.NextBlock,
            QtGui.QTextCursor.MoveMode.KeepAnchor,
            len(selected_blocks),
        )
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.EndOfBlock, QtGui.QTextCursor.MoveMode.KeepAnchor
        )

        self.setTextCursor(cursor)

    def _get_selected_blocks(self):
        cursor = self.textCursor()
        if cursor.position() > cursor.anchor():
            start_pos = cursor.anchor()
            end_pos = cursor.position()
        else:
            start_pos = cursor.position()
            end_pos = cursor.anchor()

        cursor.setPosition(start_pos)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        blocks = [cursor.block()]

        while cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextBlock):
            block = cursor.block()
            if block.position() < end_pos:
                blocks.append(block)

        return blocks

    def _backspace_should_unindent(self):
        cursor = self.textCursor()
        # Don't unindent if we have a selection.
        if cursor.hasSelection():
            return False
        column = cursor.columnNumber()
        # Don't unindent if we are at the beggining of the line
        if column < self.tab_width:
            return False
        else:
            # Unindent if we are at the indent position
            return column == self._get_indent_position(cursor.block().text())


class AdvancedCodeWidget(QtGui.QWidget):
    """ Advanced widget for viewing and editing code, with support
        for search & replace
    """

    # ------------------------------------------------------------------------
    # AdvancedCodeWidget interface
    # ------------------------------------------------------------------------

    def __init__(self, parent, font=None, lexer=None):
        super().__init__(parent)

        self.code = CodeWidget(self, font=font, lexer=lexer)
        self.find = FindWidget(self)
        self.find.hide()
        self.replace = ReplaceWidget(self)
        self.replace.hide()
        self.replace.replace_button.setEnabled(False)
        self.replace.replace_all_button.setEnabled(False)

        self.active_find_widget = None
        self.previous_find_widget = None

        self.code.selectionChanged.connect(self._update_replace_enabled)

        self.find.line_edit.returnPressed.connect(self.find_next)
        self.find.next_button.clicked.connect(self.find_next)
        self.find.prev_button.clicked.connect(self.find_prev)

        self.replace.line_edit.returnPressed.connect(self.find_next)
        self.replace.line_edit.textChanged.connect(
            self._update_replace_all_enabled
        )
        self.replace.next_button.clicked.connect(self.find_next)
        self.replace.prev_button.clicked.connect(self.find_prev)
        self.replace.replace_button.clicked.connect(self.replace_next)
        self.replace.replace_all_button.clicked.connect(self.replace_all)

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.code)
        layout.addWidget(self.find)
        layout.addWidget(self.replace)

        self.setLayout(layout)

    def _remove_event_listeners(self):
        self.code.selectionChanged.disconnect(self._update_replace_enabled)

        self.find.line_edit.returnPressed.disconnect(self.find_next)
        self.find.next_button.clicked.disconnect(self.find_next)
        self.find.prev_button.clicked.disconnect(self.find_prev)

        self.replace.line_edit.returnPressed.disconnect(self.find_next)
        self.replace.line_edit.textChanged.disconnect(
            self._update_replace_all_enabled
        )
        self.replace.next_button.clicked.disconnect(self.find_next)
        self.replace.prev_button.clicked.disconnect(self.find_prev)
        self.replace.replace_button.clicked.disconnect(self.replace_next)
        self.replace.replace_all_button.clicked.disconnect(self.replace_all)

        self.code._remove_event_listeners()

    def lines(self):
        """ Return the number of lines.
        """
        return self.code.lines()

    def set_line_column(self, line, column):
        """ Move the cursor to a particular line/column position.
        """
        self.code.set_line_column(line, column)

    def get_line_column(self):
        """ Get the current line and column numbers.
        """
        return self.code.get_line_column()

    def get_selected_text(self):
        """ Return the currently selected text.
        """
        return self.code.get_selected_text()

    def set_info_lines(self, info_lines):
        self.code.set_info_lines(info_lines)

    def set_warn_lines(self, warn_lines):
        self.code.set_warn_lines(warn_lines)

    def set_error_lines(self, error_lines):
        self.code.set_error_lines(error_lines)

    def enable_find(self):
        self.replace.hide()
        self.find.show()
        self.find.setFocus()
        if self.active_find_widget == self.replace or (
            not self.active_find_widget
            and self.previous_find_widget == self.replace
        ):
            self.find.line_edit.setText(self.replace.line_edit.text())
        self.find.line_edit.selectAll()
        self.active_find_widget = self.find

    def enable_replace(self):
        self.find.hide()
        self.replace.show()
        self.replace.setFocus()
        if self.active_find_widget == self.find or (
            not self.active_find_widget
            and self.previous_find_widget == self.find
        ):
            self.replace.line_edit.setText(self.find.line_edit.text())
        self.replace.line_edit.selectAll()
        self.active_find_widget = self.replace

    def find_in_document(self, search_text, direction="forward", replace=None):
        """ Finds the next occurance of the desired text and optionally
            replaces it. If 'replace' is None, a regular search will
            be executed, otherwise it will replace the occurance with
            the value of 'replace'.

            Returns the number of occurances found (0 or 1)
        """

        if not search_text:
            return
        wrap = self.active_find_widget.wrap_action.isChecked()

        document = self.code.document()
        find_cursor = None

        flags = QtGui.QTextDocument.FindFlags(0)
        if self.active_find_widget.case_action.isChecked():
            flags |= QtGui.QTextDocument.FindFlag.FindCaseSensitively
        if self.active_find_widget.word_action.isChecked():
            flags |= QtGui.QTextDocument.FindFlag.FindWholeWords
        if direction == "backward":
            flags |= QtGui.QTextDocument.FindFlag.FindBackward

        find_cursor = document.find(search_text, self.code.textCursor(), flags)
        if find_cursor.isNull() and wrap:
            if direction == "backward":
                find_cursor = document.find(
                    search_text, document.characterCount() - 1, flags
                )
            else:
                find_cursor = document.find(search_text, 0, flags)

        if not find_cursor.isNull():
            if replace is not None:
                find_cursor.beginEditBlock()
                find_cursor.removeSelectedText()
                find_cursor.insertText(replace)
                find_cursor.endEditBlock()
                find_cursor.movePosition(
                    QtGui.QTextCursor.MoveOperation.Left,
                    QtGui.QTextCursor.MoveMode.MoveAnchor,
                    len(replace),
                )
                find_cursor.movePosition(
                    QtGui.QTextCursor.MoveOperation.Right,
                    QtGui.QTextCursor.MoveMode.KeepAnchor,
                    len(replace),
                )
                self.code.setTextCursor(find_cursor)
            else:
                self.code.setTextCursor(find_cursor)
            return find_cursor
        else:
            # else not found: beep or indicate?
            return None

    def find_next(self):
        if not self.active_find_widget:
            self.enable_find()
        search_text = str(self.active_find_widget.line_edit.text())
        cursor = self.find_in_document(search_text=search_text)

        if cursor:
            return 1
        return 0

    def find_prev(self):
        if not self.active_find_widget:
            self.enable_find()
        search_text = str(self.active_find_widget.line_edit.text())
        cursor = self.find_in_document(
            search_text=search_text, direction="backward"
        )
        if cursor:
            return 1
        return 0

    def replace_next(self):
        search_text = self.replace.line_edit.text()
        replace_text = self.replace.replace_edit.text()

        cursor = self.code.textCursor()
        if cursor.selectedText() == search_text:
            cursor.beginEditBlock()
            cursor.removeSelectedText()
            cursor.insertText(replace_text)
            cursor.endEditBlock()
            return self.find_next()
        return 0

    def replace_all(self):
        search_text = str(self.replace.line_edit.text())
        replace_text = str(self.replace.replace_edit.text())

        count = 0
        cursor = self.code.textCursor()
        cursor.beginEditBlock()
        while (
            self.find_in_document(
                search_text=search_text, replace=replace_text
            ) is not None
        ):
            count += 1
        cursor.endEditBlock()
        return count

    def print_(self, printer):
        """ Convenience method to call 'print_' on the CodeWidget.
        """
        self.code.print_(printer)

    def ensureCursorVisible(self):
        self.code.ensureCursorVisible()

    def centerCursor(self):
        self.code.centerCursor()

    # ------------------------------------------------------------------------
    # QWidget interface
    # ------------------------------------------------------------------------

    def keyPressEvent(self, event):
        key_sequence = QtGui.QKeySequence(event.key() + int(event.modifiers()))
        if key_sequence.matches(QtGui.QKeySequence.StandardKey.Find):
            self.enable_find()
        elif key_sequence.matches(QtGui.QKeySequence.StandardKey.Replace):
            if not self.code.isReadOnly():
                self.enable_replace()
        elif key_sequence.matches(QtGui.QKeySequence(QtCore.Qt.Key.Key_Escape)):
            if self.active_find_widget:
                self.find.hide()
                self.replace.hide()
                self.code.setFocus()
                self.previous_find_widget = self.active_find_widget
                self.active_find_widget = None

        return super().keyPressEvent(event)

    # ------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------

    def _update_replace_enabled(self):
        selection = self.code.textCursor().selectedText()
        find_text = self.replace.line_edit.text()
        self.replace.replace_button.setEnabled(selection == find_text)

    def _update_replace_all_enabled(self, text):
        self.replace.replace_all_button.setEnabled(len(text))


if __name__ == "__main__":

    def set_trace():
        from PyQt4.QtCore import pyqtRemoveInputHook

        pyqtRemoveInputHook()
        import pdb

        pdb.Pdb().set_trace(sys._getframe().f_back)

    app = QtGui.QApplication(sys.argv)
    window = AdvancedCodeWidget(None)

    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")
        window.code.setPlainText(f.read())

    window.code.set_info_lines([3, 4, 8])

    window.resize(640, 640)
    window.show()
    sys.exit(app.exec_())
