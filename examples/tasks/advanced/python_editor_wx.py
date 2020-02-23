# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import sys
from os.path import basename


import wx
import wx.stc


from traits.api import Bool, Event, Instance, File, Str, Property, provides
from pyface.tasks.api import Editor
from pyface.wx.python_stc import PythonSTC, faces


from i_python_editor import IPythonEditor
from pyface.key_pressed_event import KeyPressedEvent


@provides(IPythonEditor)
class PythonEditor(Editor):
    """ The toolkit specific implementation of a StyledTextEditor.  See the
    IStyledTextEditor interface for the API documentation.
    """

    # 'IPythonEditor' interface --------------------------------------------

    obj = Instance(File)

    path = Str()

    dirty = Bool(False)

    name = Property(Str, depends_on="path")

    tooltip = Property(Str, depends_on="path")

    show_line_numbers = Bool(True)

    # Events ----

    changed = Event()

    key_pressed = Event(KeyPressedEvent)

    def _get_tooltip(self):
        return self.path

    def _get_name(self):
        return basename(self.path) or "Untitled"

    # ------------------------------------------------------------------------
    # 'PythonEditor' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        self.control = self._create_control(parent)

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

        self.control.SetText(text)
        self.dirty = False

    def save(self, path=None):
        """ Saves the contents of the editor.
        """
        if path is None:
            path = self.path

        f = file(path, "w")
        f.write(self.control.GetText())
        f.close()

        self.dirty = False

    def select_line(self, lineno):
        """ Selects the specified line.
        """
        start = self.control.PositionFromLine(lineno)
        end = self.control.GetLineEndPosition(lineno)

        self.control.SetSelection(start, end)

    def set_style(self, n, fore, back):
        self.control.StyleSetForeground(n, fore)
        # self.StyleSetBackground(n, '#c0c0c0')
        # self.StyleSetBackground(n, '#ffffff')
        self.control.StyleSetBackground(n, back)
        self.control.StyleSetFaceName(n, "courier new")
        self.control.StyleSetSize(n, faces["size"])

    # ------------------------------------------------------------------------
    # Trait handlers.
    # ------------------------------------------------------------------------

    def _path_changed(self):
        if self.control is not None:
            self.load()

    def _show_line_numbers_changed(self):
        if self.control is not None:
            c = self.control
            if self.show_line_numbers:
                c.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
                c.SetMarginWidth(1, 45)
            else:
                c.SetMarginWidth(1, 4)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Creates the toolkit-specific control for the widget.
        """
        from pyface.ui.qt4.code_editor.code_widget import AdvancedCodeWidget

        self.control = control = AdvancedCodeWidget(parent)
        self._show_line_numbers_changed()

    def _create_control(self, parent):
        """ Creates the toolkit-specific control for the widget. """

        # Base-class constructor.
        self.control = stc = PythonSTC(parent, -1)

        # No folding!
        stc.SetProperty("fold", "0")

        # Mark the maximum line size.
        stc.SetEdgeMode(wx.stc.STC_EDGE_LINE)
        stc.SetEdgeColumn(79)

        stc.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        stc.SetMarginMask(1, ~wx.stc.STC_MASK_FOLDERS)
        # Display line numbers in the margin.
        if self.show_line_numbers:
            stc.SetMarginWidth(1, 45)
            self.set_style(wx.stc.STC_STYLE_LINENUMBER, "#000000", "#c0c0c0")
        else:
            stc.SetMarginWidth(1, 4)
            self.set_style(wx.stc.STC_STYLE_LINENUMBER, "#ffffff", "#ffffff")

        # Create 'tabs' out of spaces!
        stc.SetUseTabs(False)

        # One 'tab' is 4 spaces.
        stc.SetIndent(4)

        # Line ending mode.
        stc.SetEOLMode(wx.stc.STC_EOL_LF)  # Unix
        # self.SetEOLMode(wx.stc.STC_EOL_CR) # Apple Mac
        # self.SetEOLMode(wx.stc.STC_EOL_CRLF) # Windows

        # ----------------------------------------
        # Global styles for all languages.
        # ----------------------------------------

        self.set_style(wx.stc.STC_STYLE_DEFAULT, "#000000", "#ffffff")
        self.set_style(wx.stc.STC_STYLE_CONTROLCHAR, "#000000", "#ffffff")
        self.set_style(wx.stc.STC_STYLE_BRACELIGHT, "#000000", "#ffffff")
        self.set_style(wx.stc.STC_STYLE_BRACEBAD, "#000000", "#ffffff")

        # ----------------------------------------
        # Python styles.
        # ----------------------------------------

        # White space
        self.set_style(wx.stc.STC_P_DEFAULT, "#000000", "#ffffff")

        # Comment
        self.set_style(wx.stc.STC_P_COMMENTLINE, "#007f00", "#ffffff")

        # Number
        self.set_style(wx.stc.STC_P_NUMBER, "#007f7f", "#ffffff")

        # String
        self.set_style(wx.stc.STC_P_STRING, "#7f007f", "#ffffff")

        # Single quoted string
        self.set_style(wx.stc.STC_P_CHARACTER, "#7f007f", "#ffffff")

        # Keyword
        self.set_style(wx.stc.STC_P_WORD, "#00007f", "#ffffff")

        # Triple quotes
        self.set_style(wx.stc.STC_P_TRIPLE, "#7f0000", "#ffffff")

        # Triple double quotes
        self.set_style(wx.stc.STC_P_TRIPLEDOUBLE, "#ff0000", "#ffffff")

        # Class name definition
        self.set_style(wx.stc.STC_P_CLASSNAME, "#0000ff", "#ffffff")

        # Function or method name definition
        self.set_style(wx.stc.STC_P_DEFNAME, "#007f7f", "#ffffff")

        # Operators
        self.set_style(wx.stc.STC_P_OPERATOR, "#000000", "#ffffff")

        # Identifiers
        self.set_style(wx.stc.STC_P_IDENTIFIER, "#000000", "#ffffff")

        # Comment-blocks
        self.set_style(wx.stc.STC_P_COMMENTBLOCK, "#007f00", "#ffffff")

        # End of line where string is not closed
        self.set_style(wx.stc.STC_P_STRINGEOL, "#000000", "#ffffff")

        # ----------------------------------------
        # Events.
        # ----------------------------------------

        # By default, the will fire EVT_STC_CHANGE evented for all mask values
        # (STC_MODEVENTMASKALL). This generates too many events.
        stc.SetModEventMask(
            wx.stc.STC_MOD_INSERTTEXT
            | wx.stc.STC_MOD_DELETETEXT
            | wx.stc.STC_PERFORMED_UNDO
            | wx.stc.STC_PERFORMED_REDO
        )

        # Listen for changes to the file.
        wx.stc.EVT_STC_CHANGE(stc, stc.GetId(), self._on_stc_changed)

        # Listen for key press events.
        stc.Bind(wx.EVT_CHAR, self._on_char)

        # Load the editor's contents.
        self.load()

        return stc

    # wx event handlers ----------------------------------------------------

    def _on_stc_changed(self, event):
        """ Called whenever a change is made to the text of the document. """

        self.dirty = True
        self.changed = True

        # Give other event handlers a chance.
        event.Skip()

        return

    def _on_char(self, event):
        """ Called whenever a change is made to the text of the document. """

        self.key_pressed = KeyPressedEvent(
            alt_down=event.altDown,
            control_down=event.controlDown,
            shift_down=event.shiftDown,
            key_code=event.KeyCode,
            event=event,
        )

        # Give other event handlers a chance.
        event.Skip()

        return
