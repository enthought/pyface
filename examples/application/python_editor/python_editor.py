# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Example Python Editor
=====================

This is a TraitsUI-based Tasks Editor that edits a Python file using the
standard TraitsUI CodeEditor.  Most of the code handles loading and saving
of text, and binding traits to the code editor to give user feedback, but
this editor also demonstrates how to expose TraitsUI's undo/redo mechanisms
and use that to tell whether the file needs to be saved or not.
"""

import os
from io import open

from pyface.tasks.api import TraitsEditor
from traits.api import (
    Bool,
    File,
    HasStrictTraits,
    Int,
    Property,
    Str,
    cached_property,
)
from traitsui.api import (
    CodeEditor,
    Item,
    OKCancelButtons,
    RangeEditor,
    UndoHistory,
    View,
)


class LineNumberDialog(HasStrictTraits):
    """ A simple line number dialog. """

    #: The total number of lines.
    max_line = Int()

    #: The entered line.
    line = Int()

    traits_view = View(
        Item(
            "line",
            label="Line Number:",
            editor=RangeEditor(low=1, high_name="max_line", mode="spinner"),
        ),
        buttons=OKCancelButtons,
    )


class PythonEditor(TraitsEditor):
    """ Tasks Editor that provides a code editor via TraitsUI """

    #: The Python code being edited.
    code = Str()

    #: Whether or not undo operation is possible.
    can_undo = Property(Bool, depends_on="ui.history.undoable")

    #: Whether or not redo operation is possible.
    can_redo = Property(Bool, depends_on="ui.history.redoable")

    #: The current cursor line.
    line = Int(1)

    #: The current cursor column.
    column = Int(1)

    #: The currently selected text, if any.
    selection = Str()

    #: The length of the currently selected text.
    selection_length = Property(Int, depends_on="selection")

    #: The start of the currently selected text, if any.
    selection_start = Int()

    #: The end of the currently selected text, if any.
    selection_end = Int()

    #: The position of the last save in the history.
    _last_save = Int()

    # IEditor traits ---------------------------------------------------------

    #: The file being edited.
    obj = File()

    #: The editor's user-visible name.
    name = Property(Str, depends_on="obj")

    #: The tooltip for the editor.
    tooltip = Property(Str, depends_on="obj")

    dirty = Property(Bool, depends_on=["obj", "_last_save", "ui.history.now"])

    # -------------------------------------------------------------------------
    # PythonTextEditor interface
    # -------------------------------------------------------------------------

    def load(self, path=None):
        """ Load text from a path, or set text empty if no path.

        This method uses the default encoding for io.open, which may or may
        not make sense; a real, robust editor should use tokenize.open or
        equivalent to detect file encodings.

        Parameters
        ----------
        path : path or '' or None
            The path of the file to load.  If the path is None, use the path
            providied via self.obj.
        """
        if path is None:
            path = self.obj

        if path:
            with open(path) as fp:
                self.code = fp.read()
            self.obj = path
        else:
            self.code = ""

        if self.ui is not None:
            # reset history
            self.ui.history = UndoHistory()
            self._last_save = 0

    def save(self, path=None):
        """ Load text from a path, or set text empty if no path.

        This method uses the default encoding for io.open, which may or may
        not make sense; a real, robust editor should detect the encoding
        using the mechanisms described in `PEP 263
        <https://www.python.org/dev/peps/pep-0263/>`_.

        Parameters
        ----------
        path : path or '' or None
            The path of the file to load.  If the path is None, use the path
            providied via self.obj.
        """
        if path is None:
            path = self.obj

        with open(path) as fp:
            fp.write(self.code)

        if self.ui is not None:
            # update save marker
            self._last_save = self.ui.history.now

    def go_to_line(self):
        """ Ask the use for a line number and jump to that line. """
        max_line = len(self.code.splitlines()) + 1
        dialog = LineNumberDialog(max_line=max_line, line=self.line)
        ui = dialog.edit_traits(kind="livemodal")
        if ui.result:
            self.column = 1
            self.line = dialog.line

    def undo(self):
        """ Undo an operation. """
        if self.ui is not None and self.ui.history is not None:
            self.ui.history.undo()

    def redo(self):
        """ Redo an operation. """
        if self.ui is not None and self.ui.history is not None:
            self.ui.history.redo()

    def create(self, parent):
        """ Create and set the toolkit-specific contents of the editor.
        """
        super(PythonEditor, self).create(parent)
        self.ui.history = UndoHistory()
        self._last_save = 0

    # -------------------------------------------------------------------------
    # HasTraits interface
    # -------------------------------------------------------------------------

    def _get_dirty(self):
        """ Whether or not the editor is matches saved data.

        This is True if there is no file path, or history is not at last
        save point.
        """
        return self.obj == "" or self._last_save != self.ui.history.now

    def _get_can_undo(self):
        """ Whether or not undo operations can be performed.
        """
        if self.ui is not None and self.ui.history is not None:
            return self.ui.history.can_undo
        return False

    def _get_can_redo(self):
        """ Whether or not redo operations can be performed.
        """
        if self.ui is not None and self.ui.history is not None:
            return self.ui.history.can_redo
        return False

    @cached_property
    def _get_selection_length(self):
        return len(self.selection)

    @cached_property
    def _get_name(self):
        """ The current name for the editor.

        Either the last component of the path
        """
        if self.obj:
            return os.path.basename(self.obj)
        else:
            return "untitled.py"

    @cached_property
    def _get_tooltip(self):
        """ The tooltip for the editor tab.

        The full path name or "untitiled.py".
        """
        if self.obj:
            return self.obj
        else:
            return "untitled.py"

    traits_view = View(
        Item(
            "code",
            show_label=False,
            editor=CodeEditor(
                selected_text="selection",
                selected_start_pos="selection_start",
                selected_end_pos="selection_end",
                line="line",
                column="column",
            ),
        )
    )
