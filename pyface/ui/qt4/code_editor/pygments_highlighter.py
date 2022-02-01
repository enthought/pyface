# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from pyface.qt import QtGui

from pygments.lexer import RegexLexer, _TokenType, Text, Error
from pygments.lexers import CLexer, CppLexer, PythonLexer, get_lexer_by_name
from pygments.styles.default import DefaultStyle
from pygments.token import Comment


def get_tokens_unprocessed(self, text, stack=("root",)):
    """ Split ``text`` into (tokentype, text) pairs.

        Monkeypatched to store the final stack on the object itself.

        The `text` parameter that gets passed is only the current line, so to
        highlight things like multiline strings correctly, we need to retrieve
        the state from the previous line (this is done in PygmentsHighlighter,
        below), and use it to continue processing the current line.
    """
    pos = 0
    tokendefs = self._tokens
    if hasattr(self, "_saved_state_stack"):
        statestack = list(self._saved_state_stack)
    else:
        statestack = list(stack)
    statetokens = tokendefs[statestack[-1]]
    while 1:
        for rexmatch, action, new_state in statetokens:
            m = rexmatch(text, pos)
            if m:
                if action is not None:
                    if type(action) is _TokenType:
                        yield pos, action, m.group()
                    else:
                        for item in action(self, m):
                            yield item
                pos = m.end()
                if new_state is not None:
                    # state transition
                    if isinstance(new_state, tuple):
                        for state in new_state:
                            if state == "#pop":
                                statestack.pop()
                            elif state == "#push":
                                statestack.append(statestack[-1])
                            else:
                                statestack.append(state)
                    elif isinstance(new_state, int):
                        # pop
                        del statestack[new_state:]
                    elif new_state == "#push":
                        statestack.append(statestack[-1])
                    else:
                        assert False, "wrong state def: %r" % new_state
                    statetokens = tokendefs[statestack[-1]]
                break
        else:
            try:
                if text[pos] == "\n":
                    # at EOL, reset state to "root"
                    pos += 1
                    statestack = ["root"]
                    statetokens = tokendefs["root"]
                    yield pos, Text, "\n"
                    continue
                yield pos, Error, text[pos]
                pos += 1
            except IndexError:
                break
    self._saved_state_stack = list(statestack)


# Monkeypatch!
RegexLexer.get_tokens_unprocessed = get_tokens_unprocessed


# Even with the above monkey patch to store state, multiline comments do not
# work since they are stateless (Pygments uses a single multiline regex for
# these comments, but Qt lexes by line). So we need to add a state for comments
# to the C and C++ lexers. This means that nested multiline comments will appear
# to be valid C/C++, but this is better than the alternative for now.


def replace_pattern(tokens, new_pattern):
    """ Given a RegexLexer token dictionary 'tokens', replace all patterns that
        match the token specified in 'new_pattern' with 'new_pattern'.
    """
    for state in tokens.values():
        for index, pattern in enumerate(state):
            if isinstance(pattern, tuple) and pattern[1] == new_pattern[1]:
                state[index] = new_pattern


# More monkeypatching!
comment_start = (r"/\*", Comment.Multiline, "comment")
comment_state = [
    (r"[^*/]", Comment.Multiline),
    (r"/\*", Comment.Multiline, "#push"),
    (r"\*/", Comment.Multiline, "#pop"),
    (r"[*/]", Comment.Multiline),
]
replace_pattern(CLexer.tokens, comment_start)
replace_pattern(CppLexer.tokens, comment_start)
CLexer.tokens["comment"] = comment_state
CppLexer.tokens["comment"] = comment_state


class BlockUserData(QtGui.QTextBlockUserData):
    """ Storage for the user data associated with each line.
    """

    syntax_stack = ("root",)

    def __init__(self, **kwds):
        QtGui.QTextBlockUserData.__init__(self)
        for key, value in kwds.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ["syntax_stack"]
        kwds = ", ".join(
            ["%s=%r" % (attr, getattr(self, attr)) for attr in attrs]
        )
        return "BlockUserData(%s)" % kwds


class PygmentsHighlighter(QtGui.QSyntaxHighlighter):
    """ Syntax highlighter that uses Pygments for parsing. """

    def __init__(self, parent, lexer=None):
        super().__init__(parent)

        try:
            self._lexer = get_lexer_by_name(lexer)
        except:
            self._lexer = PythonLexer()

        self._style = DefaultStyle
        # Caches for formats and brushes.
        self._brushes = {}
        self._formats = {}

    def highlightBlock(self, qstring):
        """ Highlight a block of text.
        """
        qstring = str(qstring)
        prev_data = self.previous_block_data()

        if prev_data is not None:
            self._lexer._saved_state_stack = prev_data.syntax_stack
        elif hasattr(self._lexer, "_saved_state_stack"):
            del self._lexer._saved_state_stack

        index = 0
        # Lex the text using Pygments
        for token, text in self._lexer.get_tokens(qstring):
            l = len(text)
            format = self._get_format(token)
            if format is not None:
                self.setFormat(index, l, format)
            index += l

        if hasattr(self._lexer, "_saved_state_stack"):
            data = BlockUserData(syntax_stack=self._lexer._saved_state_stack)
            self.currentBlock().setUserData(data)

            # there is a bug in pyside and it will crash unless we
            # hold on to the reference a little longer
            data = self.currentBlock().userData()

            # Clean up for the next go-round.
            del self._lexer._saved_state_stack

    def previous_block_data(self):
        """ Convenience method for returning the previous block's user data.
        """
        return self.currentBlock().previous().userData()

    def _get_format(self, token):
        """ Returns a QTextCharFormat for token or None.
        """
        if token in self._formats:
            return self._formats[token]
        result = None
        while not self._style.styles_token(token):
            token = token.parent
        for key, value in self._style.style_for_token(token).items():
            if value:
                if result is None:
                    result = QtGui.QTextCharFormat()
                if key == "color":
                    result.setForeground(self._get_brush(value))
                elif key == "bgcolor":
                    result.setBackground(self._get_brush(value))
                elif key == "bold":
                    result.setFontWeight(QtGui.QFont.Weight.Bold)
                elif key == "italic":
                    result.setFontItalic(True)
                elif key == "underline":
                    result.setUnderlineStyle(
                        QtGui.QTextCharFormat.UnderlineStyle.SingleUnderline
                    )
                elif key == "sans":
                    result.setFontStyleHint(QtGui.QFont.SansSerif)
                elif key == "roman":
                    result.setFontStyleHint(QtGui.QFont.StyleHint.Times)
                elif key == "mono":
                    result.setFontStyleHint(QtGui.QFont.TypeWriter)
                elif key == "border":
                    # Borders are normally used for errors. We can't do a border
                    # so instead we do a wavy underline
                    result.setUnderlineStyle(
                        QtGui.QTextCharFormat.UnderlineStyle.WaveUnderline
                    )
                    result.setUnderlineColor(self._get_color(value))
        self._formats[token] = result
        return result

    def _get_brush(self, color):
        """ Returns a brush for the color.
        """
        result = self._brushes.get(color)
        if result is None:
            qcolor = self._get_color(color)
            result = QtGui.QBrush(qcolor)
            self._brushes[color] = result

        return result

    def _get_color(self, color):
        qcolor = QtGui.QColor()
        qcolor.setRgb(
            int(color[:2], base=16),
            int(color[2:4], base=16),
            int(color[4:6], base=16),
        )
        return qcolor
