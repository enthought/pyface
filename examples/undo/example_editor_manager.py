# -----------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited
# Description: <Enthought undo package component>
# -----------------------------------------------------------------------------


# Enthought library imports.
from traits.etsconfig.api import ETSConfig
from pyface.workbench.api import Editor, EditorManager


class _wxLabelEditor(Editor):
    """ _wxLabelEditor is the wx implementation of a label editor. """

    def create_control(self, parent):
        import wx

        w = wx.TextCtrl(parent, style=wx.TE_RICH2)
        style = w.GetDefaultStyle()
        style.SetAlignment(wx.TEXT_ALIGNMENT_CENTER)
        w.SetDefaultStyle(style)

        self._set_text(w)
        self._set_size_and_style(w)

        self.obj.on_trait_change(self._update_text, 'text')
        self.obj.on_trait_change(self._update_size, 'size')
        self.obj.on_trait_change(self._update_style, 'style')

        return w

    def _name_default(self):
        return self.obj.text

    def _update_text(self):
        self._set_text(self.control)

    def _set_text(self, w):
        w.SetValue("")
        w.WriteText(
            "%s(%d points, %s)" % (
                self.obj.text,
                self.obj.size,
                self.obj.style
            )
        )

    def _update_size(self):
        self._set_size_and_style(self.control)

    def _update_style(self):
        self._set_size_and_style(self.control)

    def _set_size_and_style(self, w):
        import wx
        if self.obj.style == 'normal':
            style, weight = wx.NORMAL, wx.NORMAL
        elif self.obj.style == 'italic':
            style, weight = wx.ITALIC, wx.NORMAL
        elif self.obj.style == 'bold':
            style, weight = wx.NORMAL, wx.BOLD
        else:
            raise NotImplementedError(
                "style '%s' not supported" % self.obj.style
            )

        f = wx.Font(self.obj.size, wx.ROMAN, style, weight, False)
        style = wx.TextAttr("BLACK", wx.NullColour, f)
        w.SetDefaultStyle(style)
        self._set_text(w)


class _PyQt4LabelEditor(Editor):
    """ _PyQt4LabelEditor is the PyQt implementation of a label editor. """

    def create_control(self, parent):

        from pyface.qt import QtCore, QtGui

        w = QtGui.QLabel(parent)
        w.setAlignment(QtCore.Qt.AlignCenter)

        self._set_text(w)
        self._set_size(w)
        self._set_style(w)

        self.obj.on_trait_change(self._update_text, 'text')
        self.obj.on_trait_change(self._update_size, 'size')
        self.obj.on_trait_change(self._update_style, 'style')

        return w

    def _name_default(self):
        return self.obj.text

    def _update_text(self):
        self._set_text(self.control)

    def _set_text(self, w):
        w.setText(
            "%s\n(%d points, %s)" % (
                self.obj.text,
                self.obj.size,
                self.obj.style
            )
        )

    def _update_size(self):
        self._set_size(self.control)

    def _set_size(self, w):
        f = w.font()
        f.setPointSize(self.obj.size)
        w.setFont(f)

        self._set_text(w)

    def _update_style(self):
        self._set_style(self.control)

    def _set_style(self, w):
        f = w.font()
        f.setBold(self.obj.style == 'bold')
        f.setItalic(self.obj.style == 'italic')
        w.setFont(f)

        self._set_text(w)


class ExampleEditorManager(EditorManager):
    """ The ExampleEditorManager class creates the example editors. """

    def create_editor(self, window, obj, kind):

        # Create the toolkit specific editor.
        tk_name = ETSConfig.toolkit

        if tk_name == 'wx':
            ed = _wxLabelEditor(window=window, obj=obj)
        elif tk_name == 'qt4' or tk_name == 'qt':
            ed = _PyQt4LabelEditor(window=window, obj=obj)
        else:
            raise NotImplementedError(
                "unsupported toolkit: %s" % tk_name
            )

        return ed
