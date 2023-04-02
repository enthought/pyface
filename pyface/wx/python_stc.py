# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import wx
from wx import stc

import keyword

# ----------------------------------------------------------------------

demoText = """\
## This version of the editor has been set up to edit Python source
## code.  Here is a copy of wxPython/demo/Main.py to play with.


"""

# ----------------------------------------------------------------------


if wx.Platform == "__WXMSW__":
    faces = {
        "times": "Times New Roman",
        "mono": "Courier New",
        "helv": "Arial",
        "other": "Comic Sans MS",
        "size": 10,
        "size2": 8,
    }
else:
    faces = {
        "times": "Times",
        "mono": "Courier",
        "helv": "Helvetica",
        "other": "new century schoolbook",
        "size": 12,
        "size2": 10,
    }


# ----------------------------------------------------------------------


class PythonSTC(stc.StyledTextCtrl):
    def __init__(self, parent, ID):
        stc.StyledTextCtrl.__init__(
            self, parent, ID, style=wx.NO_FULL_REPAINT_ON_RESIZE
        )

        self.CmdKeyAssign(ord("B"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord("N"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0, 0)

        self.SetViewWhiteSpace(False)
        # self.SetBufferedDraw(False)

        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)

        # Setup a margin to hold fold markers
        #  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetFoldFlags(16)
        # mic
        # self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        # self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        # self.SetMarginSensitive(2, True)
        # self.SetMarginWidth(2, 12)
        # line numbers in the margin
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 25)

        if 0:  # simple folder marks, like the old version
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDER, stc.STC_MARK_ARROW, "navy", "navy"
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDEROPEN,
                stc.STC_MARK_ARROWDOWN,
                "navy",
                "navy",
            )
            # Set these to an invisible mark
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDEROPENMID,
                stc.STC_MARK_BACKGROUND,
                "white",
                "black",
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDERMIDTAIL,
                stc.STC_MARK_BACKGROUND,
                "white",
                "black",
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDERSUB,
                stc.STC_MARK_BACKGROUND,
                "white",
                "black",
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDERTAIL,
                stc.STC_MARK_BACKGROUND,
                "white",
                "black",
            )

        elif 0:  # more involved "outlining" folder marks
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDEREND,
                stc.STC_MARK_BOXPLUSCONNECTED,
                "white",
                "black",
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDEROPENMID,
                stc.STC_MARK_BOXMINUSCONNECTED,
                "white",
                "black",
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDERMIDTAIL,
                stc.STC_MARK_TCORNER,
                "white",
                "black",
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDERTAIL,
                stc.STC_MARK_LCORNER,
                "white",
                "black",
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "black"
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "black"
            )
            self.MarkerDefine(
                stc.STC_MARKNUM_FOLDEROPEN,
                stc.STC_MARK_BOXMINUS,
                "white",
                "black",
            )

        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)

        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted
        # from Scintilla sample property files.

        self.StyleClearAll()

        # Global default styles for all languages
        self.StyleSetSpec(
            stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces
        )
        self.StyleSetSpec(
            stc.STC_STYLE_LINENUMBER,
            "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces,
        )
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(
            stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold"
        )
        self.StyleSetSpec(
            stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold"
        )

        # Python styles
        # White space
        self.StyleSetSpec(
            stc.STC_P_DEFAULT,
            "fore:#808080,face:%(helv)s,size:%(size)d" % faces,
        )
        # Comment
        self.StyleSetSpec(
            stc.STC_P_COMMENTLINE,
            "fore:#007F00,face:%(other)s,size:%(size)d" % faces,
        )
        # Number
        self.StyleSetSpec(
            stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces
        )
        # String
        self.StyleSetSpec(
            stc.STC_P_STRING,
            "fore:#7F007F,italic,face:%(times)s,size:%(size)d" % faces,
        )
        # Single quoted string
        self.StyleSetSpec(
            stc.STC_P_CHARACTER,
            "fore:#7F007F,italic,face:%(times)s,size:%(size)d" % faces,
        )
        # Keyword
        self.StyleSetSpec(
            stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces
        )
        # Triple quotes
        self.StyleSetSpec(
            stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces
        )
        # Triple double quotes
        self.StyleSetSpec(
            stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces
        )
        # Class name definition
        self.StyleSetSpec(
            stc.STC_P_CLASSNAME,
            "fore:#0000FF,bold,underline,size:%(size)d" % faces,
        )
        # Function or method name definition
        self.StyleSetSpec(
            stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces
        )
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(
            stc.STC_P_IDENTIFIER,
            "fore:#808080,face:%(helv)s,size:%(size)d" % faces,
        )
        # Comment-blocks
        self.StyleSetSpec(
            stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces
        )
        # End of line where string is not closed
        self.StyleSetSpec(
            stc.STC_P_STRINGEOL,
            "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d"
            % faces,
        )

        self.SetCaretForeground("BLUE")

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)

    def OnKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()

        key = event.KeyCode

        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()
            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, "param1, param2")
            # Code completion
            else:
                # fixme: What is this mess!!!

                # lst = []
                # for x in range(50000):
                #    lst.append('%05d' % x)
                # st = " ".join(lst)
                # print len(st)
                # self.AutoCompShow(0, st)

                # fixme: What is this mess!!!
                kw = keyword.kwlist[:]
                kw.append("zzzzzz")
                kw.append("aaaaa")
                kw.append("__init__")
                kw.append("zzaaaaa")
                kw.append("zzbaaaa")
                kw.append("this_is_a_longer_value")
                kw.append("this_is_a_much_much_much_much_longer_value")

                kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(False)  # so this needs to match

                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()

    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if (
            charBefore
            and chr(charBefore) in "[]{}()"
            and styleBefore == stc.STC_P_OPERATOR
        ):
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if (
                charAfter
                and chr(charAfter) in "[]{}()"
                and styleAfter == stc.STC_P_OPERATOR
            ):
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            # pt = self.PointFromPosition(braceOpposite)
            # self.Refresh(True, Rect(pt.x, pt.y, 5,5))
            # print pt
            # self.Refresh(False)

    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())
                if (
                    self.GetFoldLevel(lineClicked)
                    & stc.STC_FOLDLEVELHEADERFLAG
                ):
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if (
                level & stc.STC_FOLDLEVELHEADERFLAG
                and (level & stc.STC_FOLDLEVELNUMBERMASK)
                == stc.STC_FOLDLEVELBASE
            ):

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)
                    if lastChild > lineNum:
                        self.HideLines(lineNum + 1, lastChild)

            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, doExpand, force, visLevels - 1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels - 1)
                    else:
                        line = self.Expand(line, False, force, visLevels - 1)
            else:
                line = line + 1

        return line


# ----------------------------------------------------------------------

_USE_PANEL = 1


def runTest(frame, nb, log):
    if not _USE_PANEL:
        ed = p = stc.PythonSTC(nb, -1)
    else:
        p = wx.Panel(nb, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        ed = PythonSTC(p, -1)
        s = wx.BoxSizer(wx.HORIZONTAL)
        s.Add(ed, 1, wx.EXPAND)
        p.SetSizer(s)
        p.SetAutoLayout(True)

    ed.SetText(demoText + open("Main.py").read())
    ed.EmptyUndoBuffer()
    ed.Colourise(0, -1)

    # line numbers in the margin
    ed.SetMarginType(1, stc.STC_MARGIN_NUMBER)
    ed.SetMarginWidth(1, 25)

    return p


# ----------------------------------------------------------------------


overview = """\
<html><body>
Once again, no docs yet.  <b>Sorry.</b>  But <a href="data/stc.h.html">this</a>
and <a href="http://www.scintilla.org/ScintillaDoc.html">this</a> should
be helpful.
</body><html>
"""
