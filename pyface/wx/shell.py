# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""The PyCrust Shell is an interactive text control in which a user types in
commands to be sent to the interpreter. This particular shell is based on
wxPython's wxStyledTextCtrl. The latest files are always available at the
SourceForge project page at http://sourceforge.net/projects/pycrust/.
Sponsored by Orbtech - Your source for Python programming expertise."""


__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: shell.py,v 1.2 2003/06/13 17:59:34 dmorrill Exp $"
__revision__ = "$Revision: 1.2 $"[11:-2]

import wx
import wx.stc
from wx import *
from wx.stc import *

wx.StyledTextCtrl = wx.stc.StyledTextCtrl
import keyword
import os
import sys
from wx.py.pseudo import PseudoFileIn, PseudoFileOut, PseudoFileErr
from wx.py.version import VERSION


from .drag_and_drop import PythonObject
from .drag_and_drop import clipboard as enClipboard

sys.ps3 = "<-- "  # Input prompt.

NAVKEYS = (
    wx.WXK_END,
    wx.WXK_LEFT,
    wx.WXK_RIGHT,
    wx.WXK_UP,
    wx.WXK_DOWN,
    wx.WXK_PAGEUP,
    wx.WXK_PAGEDOWN
)

if wxPlatform == "__WXMSW__":
    faces = {
        "times": "Times New Roman",
        "mono": "Courier New",
        "helv": "Lucida Console",
        "lucida": "Lucida Console",
        "other": "Comic Sans MS",
        "size": 10,
        "lnsize": 9,
        "backcol": "#FFFFFF",
    }
    # Versions of wxPython prior to 2.3.2 had a sizing bug on Win platform.
    # The font was 2 points too large. So we need to reduce the font size.
    if (wxMAJOR_VERSION, wxMINOR_VERSION, wxRELEASE_NUMBER) < (2, 3, 2):
        faces["size"] -= 2
        faces["lnsize"] -= 2
else:  # GTK
    faces = {
        "times": "Times",
        "mono": "Courier",
        "helv": "Helvetica",
        "other": "new century schoolbook",
        "size": 12,
        "lnsize": 10,
        "backcol": "#FFFFFF",
    }


class ShellFacade(object):
    """Simplified interface to all shell-related functionality.

    This is a semi-transparent facade, in that all attributes of other are
    still accessible, even though only some are visible to the user."""

    name = "PyCrust Shell Interface"
    revision = __revision__

    def __init__(self, other):
        """Create a ShellFacade instance."""
        methods = [
            "ask",
            "clear",
            "pause",
            "prompt",
            "quit",
            "redirectStderr",
            "redirectStdin",
            "redirectStdout",
            "run",
            "runfile",
            "wrap",
            "zoom",
        ]
        for method in methods:
            self.__dict__[method] = getattr(other, method)
        d = self.__dict__
        d["other"] = other
        d[
            "helpText"
        ] = """
* Key bindings:
Home              Go to the beginning of the command or line.
Shift+Home        Select to the beginning of the command or line.
Shift+End         Select to the end of the line.
End               Go to the end of the line.
Ctrl+C            Copy selected text, removing prompts.
Ctrl+Shift+C      Copy selected text, retaining prompts.
Ctrl+X            Cut selected text.
Ctrl+V            Paste from clipboard.
Ctrl+Shift+V      Paste and run multiple commands from clipboard.
Ctrl+Up Arrow     Retrieve Previous History item.
Alt+P             Retrieve Previous History item.
Ctrl+Down Arrow   Retrieve Next History item.
Alt+N             Retrieve Next History item.
Shift+Up Arrow    Insert Previous History item.
Shift+Down Arrow  Insert Next History item.
F8                Command-completion of History item.
                  (Type a few characters of a previous command and then press F8.)
F9                Pop-up window of matching History items.
                  (Type a few characters of a previous command and then press F9.)
"""

    def help(self):
        """Display some useful information about how to use the shell."""
        self.write(self.helpText)

    def __getattr__(self, name):
        if hasattr(self.other, name):
            return getattr(self.other, name)
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        elif hasattr(self.other, name):
            return setattr(self.other, name, value)
        else:
            raise AttributeError(name)

    def _getAttributeNames(self):
        """Return list of magic attributes to extend introspection."""
        list = [
            "autoCallTip",
            "autoComplete",
            "autoCompleteCaseInsensitive",
            "autoCompleteIncludeDouble",
            "autoCompleteIncludeMagic",
            "autoCompleteIncludeSingle",
        ]
        list.sort()
        return list


class Shell(wx.StyledTextCtrl):
    """PyCrust Shell based on wxStyledTextCtrl."""

    name = "PyCrust Shell"
    revision = __revision__

    def __init__(
        self,
        parent,
        id=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.CLIP_CHILDREN,
        introText="",
        locals=None,
        InterpClass=None,
        *args,
        **kwds
    ):
        """Create a PyCrust Shell instance."""
        wx.StyledTextCtrl.__init__(self, parent, id, pos, size, style)
        # Grab these so they can be restored by self.redirect* methods.
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.handlers = []
        self.python_obj_paste_handler = None
        # Add the current working directory "." to the search path.
        sys.path.insert(0, os.curdir)
        # Import a default interpreter class if one isn't provided.
        if InterpClass is None:
            from wx.py.interpreter import Interpreter
        else:
            Interpreter = InterpClass
        # Create default locals so we have something interesting.
        shellLocals = {
            "__name__": "PyCrust-Shell",
            "__doc__": "PyCrust-Shell, The PyCrust Python Shell.",
            "__version__": VERSION,
        }
        # Add the dictionary that was passed in.
        if locals:
            shellLocals.update(locals)
        # Create a replacement for stdin.
        self.reader = PseudoFileIn(self.readline)
        self.reader.input = ""
        self.reader.isreading = 0
        # Set up the interpreter.
        self.interp = Interpreter(
            locals=shellLocals,
            rawin=self.raw_input,
            stdin=self.reader,
            stdout=PseudoFileOut(self.writeOut),
            stderr=PseudoFileErr(self.writeErr),
            *args,
            **kwds
        )
        # Find out for which keycodes the interpreter will autocomplete.
        self.autoCompleteKeys = self.interp.getAutoCompleteKeys()
        # Keep track of the last non-continuation prompt positions.
        self.promptPosStart = 0
        self.promptPosEnd = 0
        # Keep track of multi-line commands.
        self.more = 0
        # Create the command history.  Commands are added into the front of
        # the list (ie. at index 0) as they are entered. self.historyIndex
        # is the current position in the history; it gets incremented as you
        # retrieve the previous command, decremented as you retrieve the
        # next, and reset when you hit Enter. self.historyIndex == -1 means
        # you're on the current command, not in the history.
        self.history = []
        self.historyIndex = -1
        self.historyPrefix = 0
        # Assign handlers for keyboard events.
        self.Bind(EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(EVT_CHAR, self.OnChar)
        # Assign handlers for wxSTC events.
        self.Bind(EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(EVT_STC_USERLISTSELECTION, self.OnHistorySelected)
        # Configure various defaults and user preferences.
        self.config()
        # Display the introductory banner information.
        try:
            self.showIntro(introText)
        except:
            pass
        # Assign some pseudo keywords to the interpreter's namespace.
        try:
            self.setBuiltinKeywords()
        except:
            pass
        # Add 'shell' to the interpreter's local namespace.
        try:
            self.setLocalShell()
        except:
            pass
        # Do this last so the user has complete control over their
        # environment. They can override anything they want.
        try:
            self.execStartupScript(self.interp.startupScript)
        except:
            pass

    def destroy(self):
        # del self.interp
        pass

    def config(self):
        """Configure shell based on user preferences."""
        self.SetMarginType(1, wx.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 40)

        self.SetLexer(wx.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.setStyles(faces)
        self.SetViewWhiteSpace(0)
        self.SetTabWidth(4)
        self.SetUseTabs(0)
        # Do we want to automatically pop up command completion options?
        self.autoComplete = 1
        self.autoCompleteIncludeMagic = 1
        self.autoCompleteIncludeSingle = 1
        self.autoCompleteIncludeDouble = 1
        self.autoCompleteCaseInsensitive = 1
        self.AutoCompSetIgnoreCase(self.autoCompleteCaseInsensitive)
        self.AutoCompSetSeparator(ord("\n"))
        # Do we want to automatically pop up command argument help?
        self.autoCallTip = 1
        self.CallTipSetBackground(wxColour(255, 255, 232))
        self.wrap()
        try:
            self.SetEndAtLastLine(false)
        except AttributeError:
            pass

    def showIntro(self, text=""):
        """Display introductory text in the shell."""
        if text:
            if not text.endswith(os.linesep):
                text += os.linesep
            self.write(text)
        try:
            self.write(self.interp.introText)
        except AttributeError:
            pass
        wxCallAfter(self.ScrollToLine, 0)

    def setBuiltinKeywords(self):
        """Create pseudo keywords as part of builtins.

        This simply sets "close", "exit" and "quit" to a helpful string.
        """
        import builtins

        builtins.close = (
            builtins.exit
        ) = (
            builtins.quit
        ) = "Click on the close button to leave the application."

    def quit(self):
        """Quit the application."""

        # XXX Good enough for now but later we want to send a close event.

        # In the close event handler we can make sure they want to quit.
        # Other applications, like PythonCard, may choose to hide rather than
        # quit so we should just post the event and let the surrounding app
        # decide what it wants to do.
        self.write("Click on the close button to leave the application.")

    def setLocalShell(self):
        """Add 'shell' to locals as reference to ShellFacade instance."""
        self.interp.locals["shell"] = ShellFacade(other=self)

    def execStartupScript(self, startupScript):
        """Execute the user's PYTHONSTARTUP script if they have one."""
        if startupScript and os.path.isfile(startupScript):
            startupText = "Startup script executed: " + startupScript
            self.push(
                "print(%s);exec(open(%s).read())"
                % (repr(startupText), repr(startupScript))
            )
        else:
            self.push("")

    def setStyles(self, faces):
        """Configure font size, typeface and color for lexer."""

        # Default style
        self.StyleSetSpec(
            wxSTC_STYLE_DEFAULT,
            "face:%(mono)s,size:%(size)d,back:%(backcol)s" % faces,
        )

        self.StyleClearAll()

        # Built in styles
        self.StyleSetSpec(
            wxSTC_STYLE_LINENUMBER,
            "back:#C0C0C0,face:%(mono)s,size:%(lnsize)d" % faces,
        )
        self.StyleSetSpec(wxSTC_STYLE_CONTROLCHAR, "face:%(mono)s" % faces)
        self.StyleSetSpec(wxSTC_STYLE_BRACELIGHT, "fore:#0000FF,back:#FFFF88")
        self.StyleSetSpec(wxSTC_STYLE_BRACEBAD, "fore:#FF0000,back:#FFFF88")

        # Python styles
        self.StyleSetSpec(wxSTC_P_DEFAULT, "face:%(mono)s" % faces)
        self.StyleSetSpec(
            wxSTC_P_COMMENTLINE, "fore:#007F00,face:%(mono)s" % faces
        )
        self.StyleSetSpec(wxSTC_P_NUMBER, "")
        self.StyleSetSpec(wxSTC_P_STRING, "fore:#7F007F,face:%(mono)s" % faces)
        self.StyleSetSpec(
            wxSTC_P_CHARACTER, "fore:#7F007F,face:%(mono)s" % faces
        )
        self.StyleSetSpec(wxSTC_P_WORD, "fore:#00007F,bold")
        self.StyleSetSpec(wxSTC_P_TRIPLE, "fore:#7F0000")
        self.StyleSetSpec(wxSTC_P_TRIPLEDOUBLE, "fore:#000033,back:#FFFFE8")
        self.StyleSetSpec(wxSTC_P_CLASSNAME, "fore:#0000FF,bold")
        self.StyleSetSpec(wxSTC_P_DEFNAME, "fore:#007F7F,bold")
        self.StyleSetSpec(wxSTC_P_OPERATOR, "")
        self.StyleSetSpec(wxSTC_P_IDENTIFIER, "")
        self.StyleSetSpec(wxSTC_P_COMMENTBLOCK, "fore:#7F7F7F")
        self.StyleSetSpec(
            wxSTC_P_STRINGEOL,
            "fore:#000000,face:%(mono)s,back:#E0C0E0,eolfilled" % faces,
        )

    def OnUpdateUI(self, evt):
        """Check for matching braces."""
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            # *** Patch to fix bug in wxSTC for wxPython < 2.3.3.
            if charBefore < 0:
                charBefore = 32  # Mimic a space.
            # ***
            styleBefore = self.GetStyleAt(caretPos - 1)

        # Check before.
        if (
            charBefore
            and chr(charBefore) in "[]{}()"
            and styleBefore == wx.STC_P_OPERATOR
        ):
            braceAtCaret = caretPos - 1

        # Check after.
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            # *** Patch to fix bug in wxSTC for wxPython < 2.3.3.
            if charAfter < 0:
                charAfter = 32  # Mimic a space.
            # ***
            styleAfter = self.GetStyleAt(caretPos)
            if (
                charAfter
                and chr(charAfter) in "[]{}()"
                and styleAfter == wxSTC_P_OPERATOR
            ):
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

    def OnChar(self, event):
        """Keypress event handler.

        Only receives an event if OnKeyDown calls event.Skip() for
        the corresponding event."""

        # Prevent modification of previously submitted commands/responses.
        if not self.CanEdit():
            return
        key = event.KeyCode()
        currpos = self.GetCurrentPos()
        stoppos = self.promptPosEnd
        # Return (Enter) needs to be ignored in this handler.
        if key == WXK_RETURN:
            pass
        elif key in self.autoCompleteKeys:
            # Usually the dot (period) key activates auto completion.
            # Get the command between the prompt and the cursor.
            # Add the autocomplete character to the end of the command.
            command = self.GetTextRange(stoppos, currpos)
            if command == "":
                self.historyShow()
            else:
                command += chr(key)
                self.write(chr(key))
                if self.autoComplete:
                    self.autoCompleteShow(command)
        elif key == ord("("):
            # The left paren activates a call tip and cancels
            # an active auto completion.
            if self.AutoCompActive():
                self.AutoCompCancel()
            # Get the command between the prompt and the cursor.
            # Add the '(' to the end of the command.
            self.ReplaceSelection("")
            command = self.GetTextRange(stoppos, currpos) + "("
            self.write("(")
            if self.autoCallTip:
                self.autoCallTipShow(command)
        else:
            # Allow the normal event handling to take place.
            event.Skip()

    def OnKeyDown(self, event):
        """Key down event handler."""

        # Prevent modification of previously submitted commands/responses.
        key = event.KeyCode()
        controlDown = event.ControlDown()
        altDown = event.AltDown()
        shiftDown = event.ShiftDown()
        currpos = self.GetCurrentPos()
        selecting = self.GetSelectionStart() != self.GetSelectionEnd()
        # Return (Enter) is used to submit a command to the interpreter.
        if not controlDown and key == WXK_RETURN:
            if self.AutoCompActive():
                event.Skip()
                return
            if self.CallTipActive():
                self.CallTipCancel()
            self.processLine()
        # Ctrl+Return (Cntrl+Enter) is used to insert a line break.
        elif controlDown and key == WXK_RETURN:
            if self.AutoCompActive():
                self.AutoCompCancel()
            if self.CallTipActive():
                self.CallTipCancel()
            if not self.more and (
                self.GetTextRange(self.promptPosEnd, self.GetCurrentPos())
                == ""
            ):
                self.historyShow()
            else:
                self.insertLineBreak()
        # If the auto-complete window is up let it do its thing.
        elif self.AutoCompActive():
            event.Skip()
        # Let Ctrl-Alt-* get handled normally.
        elif controlDown and altDown:
            event.Skip()
        # Clear the current, unexecuted command.
        elif key == WXK_ESCAPE:
            if self.CallTipActive():
                event.Skip()
            else:
                self.clearCommand()
        # Cut to the clipboard.
        elif (controlDown and key in (ord("X"), ord("x"))) or (
            shiftDown and key == WXK_DELETE
        ):
            self.Cut()
        # Copy to the clipboard.
        elif (
            controlDown
            and not shiftDown
            and key in (ord("C"), ord("c"), WXK_INSERT)
        ):
            self.Copy()
        # Copy to the clipboard, including prompts.
        elif (
            controlDown
            and shiftDown
            and key in (ord("C"), ord("c"), WXK_INSERT)
        ):
            self.CopyWithPrompts()
        # Home needs to be aware of the prompt.
        elif key == WXK_HOME:
            home = self.promptPosEnd
            if currpos > home:
                self.SetCurrentPos(home)
                if not selecting and not shiftDown:
                    self.SetAnchor(home)
                    self.EnsureCaretVisible()
            else:
                event.Skip()
        #
        # The following handlers modify text, so we need to see if there
        # is a selection that includes text prior to the prompt.
        #
        # Don't modify a selection with text prior to the prompt.
        elif selecting and key not in NAVKEYS and not self.CanEdit():
            pass
        # Paste from the clipboard.
        elif (
            controlDown and not shiftDown and key in (ord("V"), ord("v"))
        ) or (shiftDown and not controlDown and key == WXK_INSERT):
            self.Paste()
        # Paste from the clipboard, run commands.
        elif controlDown and shiftDown and key in (ord("V"), ord("v")):
            self.PasteAndRun()
        # Replace with the previous command from the history buffer.
        elif (controlDown and key == WXK_UP) or (
            altDown and key in (ord("P"), ord("p"))
        ):
            self.OnHistoryReplace(step=+1)
        # Replace with the next command from the history buffer.
        elif (controlDown and key == WXK_DOWN) or (
            altDown and key in (ord("N"), ord("n"))
        ):
            self.OnHistoryReplace(step=-1)
        # Insert the previous command from the history buffer.
        elif (shiftDown and key == WXK_UP) and self.CanEdit():
            self.OnHistoryInsert(step=+1)
        # Insert the next command from the history buffer.
        elif (shiftDown and key == WXK_DOWN) and self.CanEdit():
            self.OnHistoryInsert(step=-1)
        # Search up the history for the text in front of the cursor.
        elif key == WXK_F8:
            self.OnHistorySearch()
        # Show all history entries that match the command typed so far:
        elif key == WXK_F9:
            self.historyShow(self.getCommand(rstrip=0))
        # Don't backspace over the latest non-continuation prompt.
        elif key == WXK_BACK:
            if selecting and self.CanEdit():
                event.Skip()
            elif currpos > self.promptPosEnd:
                event.Skip()
        # Only allow these keys after the latest prompt.
        elif key == WXK_DELETE:
            if self.CanEdit():
                event.Skip()
        elif key == WXK_TAB:
            if self.CanEdit() and not self.topLevelComplete():
                event.Skip()
        # Don't toggle between insert mode and overwrite mode.
        elif key == WXK_INSERT:
            pass
        # Don't allow line deletion.
        elif controlDown and key in (ord("L"), ord("l")):
            pass
        # Don't allow line transposition.
        elif controlDown and key in (ord("T"), ord("t")):
            pass
        # Basic navigation keys should work anywhere.
        elif key in NAVKEYS:
            event.Skip()
        # Protect the readonly portion of the shell.
        elif not self.CanEdit():
            pass
        else:
            event.Skip()

    def clearCommand(self):
        """Delete the current, unexecuted command."""
        startpos = self.promptPosEnd
        endpos = self.GetTextLength()
        self.SetSelection(startpos, endpos)
        self.ReplaceSelection("")
        self.more = 0

    def OnHistoryReplace(self, step):
        """Replace with the previous/next command from the history buffer."""
        if not self.historyPrefix:
            self.historyPrefix = 1
            self.historyMatches = None
            prefix = self.getCommand(rstrip=0)
            n = len(prefix)
            if n > 0:
                self.historyMatches = matches = []
                for command in self.history:
                    if command[:n] == prefix and command not in matches:
                        matches.append(command)
        self.clearCommand()
        self.replaceFromHistory(step, self.historyMatches)

    def replaceFromHistory(self, step, history=None):
        """Replace selection with command from the history buffer."""
        self.ReplaceSelection("")
        if history is None:
            history = self.history
        newindex = self.historyIndex + step
        if -1 <= newindex <= len(history):
            self.historyIndex = newindex
        if 0 <= newindex <= len(history) - 1:
            command = history[self.historyIndex]
            command = command.replace("\n", os.linesep + sys.ps2)
            self.ReplaceSelection(command)

    def OnHistoryInsert(self, step):
        """Insert the previous/next command from the history buffer."""
        if not self.CanEdit():
            return
        startpos = self.GetCurrentPos()
        self.replaceFromHistory(step)
        endpos = self.GetCurrentPos()
        self.SetSelection(endpos, startpos)

    def OnHistorySearch(self):
        """Search up the history buffer for the text in front of the cursor."""
        if not self.CanEdit():
            return
        startpos = self.GetCurrentPos()
        # The text up to the cursor is what we search for.
        numCharsAfterCursor = self.GetTextLength() - startpos
        searchText = self.getCommand(rstrip=0)
        if numCharsAfterCursor > 0:
            searchText = searchText[:-numCharsAfterCursor]
        if not searchText:
            return
        # Search upwards from the current history position and loop back
        # to the beginning if we don't find anything.
        if (self.historyIndex <= -1) or (
            self.historyIndex >= len(self.history) - 2
        ):
            searchOrder = list(range(len(self.history)))
        else:
            searchOrder = list(
                range(self.historyIndex + 1, len(self.history))
            ) + list(range(self.historyIndex))
        for i in searchOrder:
            command = self.history[i]
            if command[: len(searchText)] == searchText:
                # Replace the current selection with the one we've found.
                self.ReplaceSelection(command[len(searchText):])
                endpos = self.GetCurrentPos()
                self.SetSelection(endpos, startpos)
                # We've now warped into middle of the history.
                self.historyIndex = i
                break

    def setStatusText(self, text):
        """Display status information."""

        # This method will most likely be replaced by the enclosing app
        # to do something more interesting, like write to a status bar.
        print(text)

    def insertLineBreak(self):
        """Insert a new line break."""
        if self.CanEdit():
            self.write(os.linesep)
            self.more = 1
            self.prompt()

    def processLine(self):
        """Process the line of text at which the user hit Enter."""

        # The user hit ENTER and we need to decide what to do. They could be
        # sitting on any line in the shell.

        thepos = self.GetCurrentPos()
        startpos = self.promptPosEnd
        endpos = self.GetTextLength()
        # If they hit RETURN inside the current command, execute the command.
        if self.CanEdit():
            self.SetCurrentPos(endpos)
            self.interp.more = 0
            command = self.GetTextRange(startpos, endpos)
            lines = command.split(os.linesep + sys.ps2)
            lines = [line.rstrip() for line in lines]
            command = "\n".join(lines)
            if self.reader.isreading:
                if not command:
                    # Match the behavior of the standard Python shell when
                    # the user hits return without entering a value.
                    command = "\n"
                self.reader.input = command
                self.write(os.linesep)
            else:
                self.push(command)
        # Or replace the current command with the other command.
        else:
            # If the line contains a command (even an invalid one).
            if self.getCommand(rstrip=0):
                command = self.getMultilineCommand()
                self.clearCommand()
                self.write(command)
            # Otherwise, put the cursor back where we started.
            else:
                self.SetCurrentPos(thepos)
                self.SetAnchor(thepos)

    def getMultilineCommand(self, rstrip=1):
        """Extract a multi-line command from the editor.

        The command may not necessarily be valid Python syntax."""
        # XXX Need to extract real prompts here. Need to keep track of the
        # prompt every time a command is issued.
        ps1 = str(sys.ps1)
        ps1size = len(ps1)
        ps2 = str(sys.ps2)
        ps2size = len(ps2)
        # This is a total hack job, but it works.
        text = self.GetCurLine()[0]
        line = self.GetCurrentLine()
        while text[:ps2size] == ps2 and line > 0:
            line -= 1
            self.GotoLine(line)
            text = self.GetCurLine()[0]
        if text[:ps1size] == ps1:
            line = self.GetCurrentLine()
            self.GotoLine(line)
            startpos = self.GetCurrentPos() + ps1size
            line += 1
            self.GotoLine(line)
            while self.GetCurLine()[0][:ps2size] == ps2:
                line += 1
                self.GotoLine(line)
            stoppos = self.GetCurrentPos()
            command = self.GetTextRange(startpos, stoppos)
            command = command.replace(os.linesep + sys.ps2, "\n")
            command = command.rstrip()
            command = command.replace("\n", os.linesep + sys.ps2)
        else:
            command = ""
        if rstrip:
            command = command.rstrip()
        return command

    def getCommand(self, text=None, rstrip=1):
        """Extract a command from text which may include a shell prompt.

        The command may not necessarily be valid Python syntax."""
        if not text:
            text = self.GetCurLine()[0]
        # Strip the prompt off the front of text leaving just the command.
        command = self.lstripPrompt(text)
        if command == text:
            command = ""  # Real commands have prompts.
        if rstrip:
            command = command.rstrip()
        return command

    def lstripPrompt(self, text):
        """Return text without a leading prompt."""
        ps1 = str(sys.ps1)
        ps1size = len(ps1)
        ps2 = str(sys.ps2)
        ps2size = len(ps2)
        # Strip the prompt off the front of text.
        if text[:ps1size] == ps1:
            text = text[ps1size:]
        elif text[:ps2size] == ps2:
            text = text[ps2size:]
        return text

    def push(self, command):
        """Send command to the interpreter for execution."""
        self.write(os.linesep)
        busy = wxBusyCursor()
        self.more = self.interp.push(command)
        del busy
        if not self.more:
            self.addHistory(command.rstrip())
            for handler in self.handlers:
                handler()
        self.prompt()

    def addHistory(self, command):
        """Add command to the command history."""
        # Reset the history position.
        self.historyIndex = -1
        self.historyPrefix = 0
        # Insert this command into the history, unless it's a blank
        # line or the same as the last command.
        if command != "" and (
            len(self.history) == 0 or command != self.history[0]
        ):
            self.history.insert(0, command)

    def write(self, text):
        """Display text in the shell.

        Replace line endings with OS-specific endings."""
        text = self.fixLineEndings(text)
        self.AddText(text)
        self.EnsureCaretVisible()

    def fixLineEndings(self, text):
        """Return text with line endings replaced by OS-specific endings."""
        lines = text.split("\r\n")
        for l in range(len(lines)):
            chunks = lines[l].split("\r")
            for c in range(len(chunks)):
                chunks[c] = os.linesep.join(chunks[c].split("\n"))
            lines[l] = os.linesep.join(chunks)
        text = os.linesep.join(lines)
        return text

    def prompt(self):
        """Display appropriate prompt for the context, either ps1, ps2 or ps3.

        If this is a continuation line, autoindent as necessary."""
        isreading = self.reader.isreading
        skip = 0
        if isreading:
            prompt = str(sys.ps3)
        elif self.more:
            prompt = str(sys.ps2)
        else:
            prompt = str(sys.ps1)
        pos = self.GetCurLine()[1]
        if pos > 0:
            if isreading:
                skip = 1
            else:
                self.write(os.linesep)
        if not self.more:
            self.promptPosStart = self.GetCurrentPos()
        if not skip:
            self.write(prompt)
        if not self.more:
            self.promptPosEnd = self.GetCurrentPos()
            # Keep the undo feature from undoing previous responses.
            self.EmptyUndoBuffer()
        # XXX Add some autoindent magic here if more.
        if self.more:
            self.write(" " * 4)  # Temporary hack indentation.
        self.EnsureCaretVisible()
        self.ScrollToColumn(0)

    def readline(self):
        """Replacement for stdin.readline()."""
        input = ""
        reader = self.reader
        reader.isreading = 1
        self.prompt()
        try:
            while not reader.input:
                wx.Yield()
            input = reader.input
        finally:
            reader.input = ""
            reader.isreading = 0
        return input

    def raw_input(self, prompt=""):
        """Return string based on user input."""
        if prompt:
            self.write(prompt)
        return self.readline()

    def ask(self, prompt="Please enter your response:"):
        """Get response from the user using a dialog box."""
        dialog = wx.TextEntryDialog(None, prompt, "Input Dialog (Raw)", "")
        try:
            if dialog.ShowModal() == wxID_OK:
                text = dialog.GetValue()
                return text
        finally:
            dialog.Destroy()
        return ""

    def pause(self):
        """Halt execution pending a response from the user."""
        self.ask("Press enter to continue:")

    def clear(self):
        """Delete all text from the shell."""
        self.ClearAll()

    def run(self, command, prompt=1, verbose=1):
        """Execute command within the shell as if it was typed in directly.
        >>> shell.run('print "this"')
        >>> print "this"
        this
        >>>
        """
        # Go to the very bottom of the text.
        endpos = self.GetTextLength()
        self.SetCurrentPos(endpos)
        command = command.rstrip()
        if prompt:
            self.prompt()
        if verbose:
            self.write(command)
        self.push(command)

    def runfile(self, filename):
        """Execute all commands in file as if they were typed into the shell."""
        file = open(filename)
        try:
            self.prompt()
            for command in file.readlines():
                if command[:6] == "shell.":  # Run shell methods silently.
                    self.run(command, prompt=0, verbose=0)
                else:
                    self.run(command, prompt=0, verbose=1)
        finally:
            file.close()

    def autoCompleteShow(self, command):
        """Display auto-completion popup list."""
        list = self.interp.getAutoCompleteList(
            command,
            includeMagic=self.autoCompleteIncludeMagic,
            includeSingle=self.autoCompleteIncludeSingle,
            includeDouble=self.autoCompleteIncludeDouble,
        )
        if list:
            options = "\n".join(list)
            offset = 0
            self.AutoCompShow(offset, options)

    def autoCallTipShow(self, command):
        """Display argument spec and docstring in a popup bubble thingie."""
        if self.CallTipActive:
            self.CallTipCancel()
        (name, argspec, tip) = self.interp.getCallTip(command)
        if argspec:
            startpos = self.GetCurrentPos()
            self.write(argspec + ")")
            endpos = self.GetCurrentPos()
            self.SetSelection(endpos, startpos)
        if tip:
            curpos = self.GetCurrentPos()
            tippos = curpos - (len(name) + 1)
            fallback = curpos - self.GetColumn(curpos)
            # In case there isn't enough room, only go back to the fallback.
            tippos = max(tippos, fallback)
            self.CallTipShow(tippos, tip)

    def historyShow(self, prefix=""):
        items = []
        for item in self.history:
            item = item.replace("\n", "\\n")
            if (prefix == item[: len(prefix)]) and item not in items:
                items.append(item)
        self.UserListShow(1, "\n".join(items))

    def OnHistorySelected(self, event):
        command = event.GetText()
        if command.find("\\n") >= 0:
            command += "\\n"
            command = command.replace("\\n", os.linesep + sys.ps2)
        self.clearCommand()
        self.write(command)
        # Process the command if the 'Enter' key was pressed:
        key = event.GetKey()
        if key == 28 or key == 1241712:  # Is there a 'name' for the Enter key?
            self.processLine()

    def topLevelComplete(self):
        command = self.getCommand(rstrip=0)
        completions = self.interp.getTopLevelCompletions(command)
        if len(completions) == 0:
            return 0
        if len(completions) == 1:
            self.write(completions[0][len(command):])
        else:
            self.AutoCompShow(len(command), "\n".join(completions))
        return 1

    def writeOut(self, text):
        """Replacement for stdout."""
        self.write(text)

    def writeErr(self, text):
        """Replacement for stderr."""
        self.write(text)

    def redirectStdin(self, redirect=1):
        """If redirect is true then sys.stdin will come from the shell."""
        if redirect:
            sys.stdin = self.reader
        else:
            sys.stdin = self.stdin

    def redirectStdout(self, redirect=1):
        """If redirect is true then sys.stdout will go to the shell."""
        if redirect:
            sys.stdout = PseudoFileOut(self.writeOut)
        else:
            sys.stdout = self.stdout

    def redirectStderr(self, redirect=1):
        """If redirect is true then sys.stderr will go to the shell."""
        if redirect:
            sys.stderr = PseudoFileErr(self.writeErr)
        else:
            sys.stderr = self.stderr

    def CanCut(self):
        """Return true if text is selected and can be cut."""
        if (
            self.GetSelectionStart() != self.GetSelectionEnd()
            and self.GetSelectionStart() >= self.promptPosEnd
            and self.GetSelectionEnd() >= self.promptPosEnd
        ):
            return 1
        else:
            return 0

    def CanCopy(self):
        """Return true if text is selected and can be copied."""
        return self.GetSelectionStart() != self.GetSelectionEnd()

    def CanPaste(self):
        """Return true if a paste should succeed."""
        if self.CanEdit() and (
            wx.StyledTextCtrl.CanPaste(self)
            or wx.TheClipboard.IsSupported(PythonObject)
        ):
            return 1
        else:
            return 0

    def CanEdit(self):
        """Return true if editing should succeed."""
        if self.GetSelectionStart() != self.GetSelectionEnd():
            if (
                self.GetSelectionStart() >= self.promptPosEnd
                and self.GetSelectionEnd() >= self.promptPosEnd
            ):
                return 1
            else:
                return 0
        else:
            return self.GetCurrentPos() >= self.promptPosEnd

    def Cut(self):
        """Remove selection and place it on the clipboard."""
        if self.CanCut() and self.CanCopy():
            if self.AutoCompActive():
                self.AutoCompCancel()
            if self.CallTipActive:
                self.CallTipCancel()
            self.Copy()
            self.ReplaceSelection("")

    def Copy(self):
        """Copy selection and place it on the clipboard."""
        if self.CanCopy():
            command = self.GetSelectedText()
            command = command.replace(os.linesep + sys.ps2, os.linesep)
            command = command.replace(os.linesep + sys.ps1, os.linesep)
            command = self.lstripPrompt(text=command)
            data = wxTextDataObject(command)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(data)
                wx.TheClipboard.Close()

    def CopyWithPrompts(self):
        """Copy selection, including prompts, and place it on the clipboard."""
        if self.CanCopy():
            command = self.GetSelectedText()

            data = wx.TextDataObject(command)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(data)
                wx.TheClipboard.Close()

    def Paste(self):
        """Replace selection with clipboard contents."""
        if self.CanPaste() and wxTheClipboard.Open():
            try:
                if wxTheClipboard.IsSupported(wxDataFormat(wxDF_TEXT)):
                    data = wxTextDataObject()
                    if wx.TheClipboard.GetData(data):
                        self.ReplaceSelection("")
                        command = data.GetText()
                        command = command.rstrip()
                        command = self.fixLineEndings(command)
                        command = self.lstripPrompt(text=command)
                        command = command.replace(os.linesep + sys.ps2, "\n")
                        command = command.replace(os.linesep, "\n")
                        command = command.replace("\n", os.linesep + sys.ps2)
                        self.write(command)
                if (
                    wx.TheClipboard.IsSupported(PythonObject)
                    and self.python_obj_paste_handler is not None
                ):
                    # note that the presence of a PythonObject on the
                    # clipboard is really just a signal to grab the data
                    # from our singleton clipboard instance
                    data = enClipboard.data
                    self.python_obj_paste_handler(data)
            finally:
                wx.TheClipboard.Close()

    def PasteAndRun(self):
        """Replace selection with clipboard contents, run commands."""
        if wx.TheClipboard.Open():
            if wx.TheClipboard.IsSupported(wxDataFormat(wxDF_TEXT)):
                data = wx.TextDataObject()
                if wx.TheClipboard.GetData(data):
                    endpos = self.GetTextLength()
                    self.SetCurrentPos(endpos)
                    startpos = self.promptPosEnd
                    self.SetSelection(startpos, endpos)
                    self.ReplaceSelection("")
                    text = data.GetText()
                    text = text.strip()
                    text = self.fixLineEndings(text)
                    text = self.lstripPrompt(text=text)
                    text = text.replace(os.linesep + sys.ps1, "\n")
                    text = text.replace(os.linesep + sys.ps2, "\n")
                    text = text.replace(os.linesep, "\n")
                    lines = text.split("\n")
                    commands = []
                    command = ""
                    for line in lines:
                        if line.strip() != "" and line.lstrip() == line:
                            # New command.
                            if command:
                                # Add the previous command to the list.
                                commands.append(command)
                            # Start a new command, which may be multiline.
                            command = line
                        else:
                            # Multiline command. Add to the command.
                            command += "\n"
                            command += line
                    commands.append(command)
                    for command in commands:
                        command = command.replace("\n", os.linesep + sys.ps2)
                        self.write(command)
                        self.processLine()
            wx.TheClipboard.Close()

    def wrap(self, wrap=1):
        """Sets whether text is word wrapped."""
        try:
            self.SetWrapMode(wrap)
        except AttributeError:
            return "Wrapping is not available in this version of PyCrust."

    def zoom(self, points=0):
        """Set the zoom level.

        This number of points is added to the size of all fonts.
        It may be positive to magnify or negative to reduce."""
        self.SetZoom(points)


wxID_SELECTALL = wx.NewId()
ID_AUTOCOMP = wx.NewId()
ID_AUTOCOMP_SHOW = wx.NewId()
ID_AUTOCOMP_INCLUDE_MAGIC = wx.NewId()
ID_AUTOCOMP_INCLUDE_SINGLE = wx.NewId()
ID_AUTOCOMP_INCLUDE_DOUBLE = wx.NewId()
ID_CALLTIPS = wx.NewId()
ID_CALLTIPS_SHOW = wx.NewId()

ID_FILLING = wx.NewId()
ID_FILLING_AUTO_UPDATE = wx.NewId()
ID_FILLING_SHOW_METHODS = wx.NewId()
ID_FILLING_SHOW_CLASS = wx.NewId()
ID_FILLING_SHOW_DICT = wx.NewId()
ID_FILLING_SHOW_DOC = wx.NewId()
ID_FILLING_SHOW_MODULE = wx.NewId()


class ShellMenu(object):
    """Mixin class to add standard menu items."""

    def createMenus(self):
        m = self.fileMenu = wxMenu()
        m.AppendSeparator()
        m.Append(wxID_EXIT, "E&xit", "Exit PyCrust")

        m = self.editMenu = wxMenu()
        m.Append(wxID_UNDO, "&Undo \tCtrl+Z", "Undo the last action")
        m.Append(wxID_REDO, "&Redo \tCtrl+Y", "Redo the last undone action")
        m.AppendSeparator()
        m.Append(wxID_CUT, "Cu&t \tCtrl+X", "Cut the selection")
        m.Append(wxID_COPY, "&Copy \tCtrl+C", "Copy the selection")
        m.Append(wxID_PASTE, "&Paste \tCtrl+V", "Paste")
        m.AppendSeparator()
        m.Append(wxID_CLEAR, "Cle&ar", "Delete the selection")
        m.Append(wxID_SELECTALL, "Select A&ll", "Select all text")

        m = self.autocompMenu = wxMenu()
        m.Append(
            ID_AUTOCOMP_SHOW,
            "Show Auto Completion",
            "Show auto completion during dot syntax",
            1,
        )
        m.Append(
            ID_AUTOCOMP_INCLUDE_MAGIC,
            "Include Magic Attributes",
            "Include attributes visible to __getattr__ and __setattr__",
            1,
        )
        m.Append(
            ID_AUTOCOMP_INCLUDE_SINGLE,
            "Include Single Underscores",
            "Include attibutes prefixed by a single underscore",
            1,
        )
        m.Append(
            ID_AUTOCOMP_INCLUDE_DOUBLE,
            "Include Double Underscores",
            "Include attibutes prefixed by a double underscore",
            1,
        )

        m = self.calltipsMenu = wxMenu()
        m.Append(
            ID_CALLTIPS_SHOW,
            "Show Call Tips",
            "Show call tips with argument specifications",
            1,
        )

        m = self.optionsMenu = wxMenu()
        m.AppendMenu(
            ID_AUTOCOMP,
            "&Auto Completion",
            self.autocompMenu,
            "Auto Completion Options",
        )
        m.AppendMenu(
            ID_CALLTIPS, "&Call Tips", self.calltipsMenu, "Call Tip Options"
        )

        if hasattr(self, "crust"):
            fm = self.fillingMenu = wxMenu()
            fm.Append(
                ID_FILLING_AUTO_UPDATE,
                "Automatic Update",
                "Automatically update tree view after each command",
                1,
            )
            fm.Append(
                ID_FILLING_SHOW_METHODS,
                "Show Methods",
                "Show methods and functions in the tree view",
                1,
            )
            fm.Append(
                ID_FILLING_SHOW_CLASS,
                "Show __class__",
                "Show __class__ entries in the tree view",
                1,
            )
            fm.Append(
                ID_FILLING_SHOW_DICT,
                "Show __dict__",
                "Show __dict__ entries in the tree view",
                1,
            )
            fm.Append(
                ID_FILLING_SHOW_DOC,
                "Show __doc__",
                "Show __doc__ entries in the tree view",
                1,
            )
            fm.Append(
                ID_FILLING_SHOW_MODULE,
                "Show __module__",
                "Show __module__ entries in the tree view",
                1,
            )
            m.AppendMenu(ID_FILLING, "&Filling", fm, "Filling Options")

        m = self.helpMenu = wxMenu()
        m.AppendSeparator()
        m.Append(wxID_ABOUT, "&About...", "About PyCrust")

        b = self.menuBar = wxMenuBar()
        b.Append(self.fileMenu, "&File")
        b.Append(self.editMenu, "&Edit")
        b.Append(self.optionsMenu, "&Options")
        b.Append(self.helpMenu, "&Help")
        self.SetMenuBar(b)

        self.Bind(EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(EVT_MENU, self.OnUndo, id=wx.ID_UNDO)
        self.Bind(EVT_MENU, self.OnRedo, id=wx.ID_REDO)
        self.Bind(EVT_MENU, self.OnCut, id=wx.ID_CUT)
        self.Bind(EVT_MENU, self.OnCopy, id=wx.ID_COPY)
        self.Bind(EVT_MENU, self.OnPaste, id=wx.ID_PASTE)
        self.Bind(EVT_MENU, self.OnClear, id=wx.ID_CLEAR)
        self.Bind(EVT_MENU, self.OnSelectAll, id=wx.ID_SELECTALL)
        self.Bind(EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(EVT_MENU, self.OnAutoCompleteShow, ID_AUTOCOMP_SHOW)
        self.Bind(
            EVT_MENU,
            self.OnAutoCompleteIncludeMagic,
            id=ID_AUTOCOMP_INCLUDE_MAGIC,
        )
        self.Bind(
            EVT_MENU,
            self.OnAutoCompleteIncludeSingle,
            id=ID_AUTOCOMP_INCLUDE_SINGLE,
        )
        self.Bind(
            EVT_MENU,
            self.OnAutoCompleteIncludeDouble,
            id=ID_AUTOCOMP_INCLUDE_DOUBLE,
        )
        self.Bind(EVT_MENU, self.OnCallTipsShow, id=ID_CALLTIPS_SHOW)

        self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=wx.ID_UNDO)
        self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=wx.ID_REDO)
        self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=wx.ID_CUT)
        self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=wx.ID_COPY)
        self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=wx.ID_PASTE)
        self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=wx.ID_CLEAR)
        self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTOCOMP_SHOW)
        self.Bind(
            EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTOCOMP_INCLUDE_MAGIC
        )
        self.Bind(
            EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTOCOMP_INCLUDE_SINGLE
        )
        self.Bind(
            EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_AUTOCOMP_INCLUDE_DOUBLE
        )
        self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_CALLTIPS_SHOW)

        if hasattr(self, "crust"):
            self.Bind(
                EVT_MENU, self.OnFillingAutoUpdate, id=ID_FILLING_AUTO_UPDATE
            )
            self.Bind(
                EVT_MENU, self.OnFillingShowMethods, id=ID_FILLING_SHOW_METHODS
            )
            self.Bind(
                EVT_MENU, self.OnFillingShowClass, id=ID_FILLING_SHOW_CLASS
            )
            self.Bind(
                EVT_MENU, self.OnFillingShowDict, id=ID_FILLING_SHOW_DICT
            )
            self.Bind(EVT_MENU, self.OnFillingShowDoc, id=ID_FILLING_SHOW_DOC)
            self.Bind(
                EVT_MENU, self.OnFillingShowModule, id=ID_FILLING_SHOW_MODULE
            )
            self.Bind(
                EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FILLING_AUTO_UPDATE
            )
            self.Bind(
                EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FILLING_SHOW_METHODS
            )
            self.Bind(
                EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FILLING_SHOW_CLASS
            )
            self.Bind(
                EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FILLING_SHOW_DICT
            )
            self.Bind(EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FILLING_SHOW_DOC)
            self.Bind(
                EVT_UPDATE_UI, self.OnUpdateMenu, id=ID_FILLING_SHOW_MODULE
            )

    def OnExit(self, event):
        self.Close(True)

    def OnUndo(self, event):
        self.shell.Undo()

    def OnRedo(self, event):
        self.shell.Redo()

    def OnCut(self, event):
        self.shell.Cut()

    def OnCopy(self, event):
        self.shell.Copy()

    def OnPaste(self, event):
        self.shell.Paste()

    def OnClear(self, event):
        self.shell.Clear()

    def OnSelectAll(self, event):
        self.shell.SelectAll()

    def OnAbout(self, event):
        """Display an About PyCrust window."""
        import sys

        title = "About PyCrust"
        text = (
            "PyCrust %s\n\n" % VERSION
            + "Yet another Python shell, only flakier.\n\n"
            + "Half-baked by Patrick K. O'Brien,\n"
            + "the other half is still in the oven.\n\n"
            + "Shell Revision: %s\n" % self.shell.revision
            + "Interpreter Revision: %s\n\n" % self.shell.interp.revision
            + "Python Version: %s\n" % sys.version.split()[0]
            + "wxPython Version: %s\n" % wx.__version__
            + "Platform: %s\n" % sys.platform
        )
        dialog = wxMessageDialog(self, text, title, wxOK | wxICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()

    def OnAutoCompleteShow(self, event):
        self.shell.autoComplete = event.IsChecked()

    def OnAutoCompleteIncludeMagic(self, event):
        self.shell.autoCompleteIncludeMagic = event.IsChecked()

    def OnAutoCompleteIncludeSingle(self, event):
        self.shell.autoCompleteIncludeSingle = event.IsChecked()

    def OnAutoCompleteIncludeDouble(self, event):
        self.shell.autoCompleteIncludeDouble = event.IsChecked()

    def OnCallTipsShow(self, event):
        self.shell.autoCallTip = event.IsChecked()

    def OnFillingAutoUpdate(self, event):
        tree = self.crust.filling.fillingTree
        tree.autoUpdate = event.IsChecked()
        tree.if_autoUpdate()

    def OnFillingShowMethods(self, event):
        tree = self.crust.filling.fillingTree
        tree.showMethods = event.IsChecked()
        tree.update()

    def OnFillingShowClass(self, event):
        tree = self.crust.filling.fillingTree
        tree.showClass = event.IsChecked()
        tree.update()

    def OnFillingShowDict(self, event):
        tree = self.crust.filling.fillingTree
        tree.showDict = event.IsChecked()
        tree.update()

    def OnFillingShowDoc(self, event):
        tree = self.crust.filling.fillingTree
        tree.showDoc = event.IsChecked()
        tree.update()

    def OnFillingShowModule(self, event):
        tree = self.crust.filling.fillingTree
        tree.showModule = event.IsChecked()
        tree.update()

    def OnUpdateMenu(self, event):
        """Update menu items based on current status."""
        id = event.GetId()
        if id == wxID_UNDO:
            event.Enable(self.shell.CanUndo())
        elif id == wxID_REDO:
            event.Enable(self.shell.CanRedo())
        elif id == wxID_CUT:
            event.Enable(self.shell.CanCut())
        elif id == wxID_COPY:
            event.Enable(self.shell.CanCopy())
        elif id == wxID_PASTE:
            event.Enable(self.shell.CanPaste())
        elif id == wxID_CLEAR:
            event.Enable(self.shell.CanCut())
        elif id == ID_AUTOCOMP_SHOW:
            event.Check(self.shell.autoComplete)
        elif id == ID_AUTOCOMP_INCLUDE_MAGIC:
            event.Check(self.shell.autoCompleteIncludeMagic)
        elif id == ID_AUTOCOMP_INCLUDE_SINGLE:
            event.Check(self.shell.autoCompleteIncludeSingle)
        elif id == ID_AUTOCOMP_INCLUDE_DOUBLE:
            event.Check(self.shell.autoCompleteIncludeDouble)
        elif id == ID_CALLTIPS_SHOW:
            event.Check(self.shell.autoCallTip)
        elif id == ID_FILLING_AUTO_UPDATE:
            event.Check(self.crust.filling.fillingTree.autoUpdate)
        elif id == ID_FILLING_SHOW_METHODS:
            event.Check(self.crust.filling.fillingTree.showMethods)
        elif id == ID_FILLING_SHOW_CLASS:
            event.Check(self.crust.filling.fillingTree.showClass)
        elif id == ID_FILLING_SHOW_DICT:
            event.Check(self.crust.filling.fillingTree.showDict)
        elif id == ID_FILLING_SHOW_DOC:
            event.Check(self.crust.filling.fillingTree.showDoc)
        elif id == ID_FILLING_SHOW_MODULE:
            event.Check(self.crust.filling.fillingTree.showModule)
