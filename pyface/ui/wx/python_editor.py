# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""

import warnings

import wx.stc


from traits.api import Bool, Event, provides, Str


from pyface.i_python_editor import IPythonEditor, MPythonEditor
from pyface.key_pressed_event import KeyPressedEvent
from pyface.wx.python_stc import PythonSTC, faces
from .layout_widget import LayoutWidget


@provides(IPythonEditor)
class PythonEditor(MPythonEditor, LayoutWidget):
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

    def __init__(self, parent=None, **traits):
        """ Creates a new pager. """

        create = traits.pop("create", None)

        # Base class constructor.
        super().__init__(parent=parent, **traits)

        if create:
            # Create the widget's toolkit-specific control.
            self.create()
            warnings.warn(
                "automatic widget creation is deprecated and will be removed "
                "in a future Pyface version, code should not pass the create "
                "parameter and should instead call create() explicitly",
                DeprecationWarning,
                stacklevel=2,
            )
        elif create is not None:
            warnings.warn(
                "setting create=False is no longer required",
                DeprecationWarning,
                stacklevel=2,
            )

    # ------------------------------------------------------------------------
    # 'PythonEditor' interface.
    # ------------------------------------------------------------------------

    def load(self, path=None):
        """ Loads the contents of the editor. """

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
        """ Saves the contents of the editor. """

        if path is None:
            path = self.path

        f = open(path, "w")
        f.write(self.control.GetText())
        f.close()

        self.dirty = False

    def set_style(self, n, fore, back):

        self.control.StyleSetForeground(n, fore)
        self.control.StyleSetBackground(n, back)
        self.control.StyleSetFaceName(n, "courier new")
        self.control.StyleSetSize(n, faces["size"])

    def select_line(self, lineno):
        """ Selects the specified line. """

        start = self.control.PositionFromLine(lineno)
        end = self.control.GetLineEndPosition(lineno)

        self.control.SetSelection(start, end)

        return

    # ------------------------------------------------------------------------
    # Trait handlers.
    # ------------------------------------------------------------------------

    def _path_changed(self):
        """ Handle a change to path. """

        self._changed_path()

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Creates the toolkit-specific control for the widget. """

        # Base-class constructor.
        self.control = stc = PythonSTC(parent, -1)

        # No folding!
        stc.SetProperty("fold", "0")

        # Mark the maximum line size.
        stc.SetEdgeMode(wx.stc.STC_EDGE_LINE)
        stc.SetEdgeColumn(79)

        # Display line numbers in the margin.
        if self.show_line_numbers:
            stc.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
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

        # ------------------------------------------------------------------------
        # Global styles for all languages.
        # ------------------------------------------------------------------------

        self.set_style(wx.stc.STC_STYLE_DEFAULT, "#000000", "#ffffff")
        self.set_style(wx.stc.STC_STYLE_CONTROLCHAR, "#000000", "#ffffff")
        self.set_style(wx.stc.STC_STYLE_BRACELIGHT, "#000000", "#ffffff")
        self.set_style(wx.stc.STC_STYLE_BRACEBAD, "#000000", "#ffffff")

        # ------------------------------------------------------------------------
        # Python styles.
        # ------------------------------------------------------------------------

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

        # ------------------------------------------------------------------------
        # Events.
        # ------------------------------------------------------------------------

        # By default, the will fire EVT_STC_CHANGE evented for all mask values
        # (STC_MODEVENTMASKALL). This generates too many events.
        stc.SetModEventMask(
            wx.stc.STC_MOD_INSERTTEXT
            | wx.stc.STC_MOD_DELETETEXT
            | wx.stc.STC_PERFORMED_UNDO
            | wx.stc.STC_PERFORMED_REDO
        )

        # Listen for changes to the file.
        stc.Bind(wx.stc.EVT_STC_CHANGE, self._on_stc_changed)

        # Listen for key press events.
        stc.Bind(wx.EVT_CHAR, self._on_char)

        # Load the editor's contents.
        self.load()

        return stc

    def destroy(self):
        """ Destroy the toolkit control. """
        if self.control is not None:
            self.control.Unbind(wx.stc.EVT_STC_CHANGE)
            self.control.Unbind(wx.EVT_CHAR)
        super().destroy()

    # wx event handlers ----------------------------------------------------

    def _on_stc_changed(self, event):
        """ Called whenever a change is made to the text of the document. """

        self.dirty = True
        self.changed = True

        # Give other event handlers a chance.
        event.Skip()

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
