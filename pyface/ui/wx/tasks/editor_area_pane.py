# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import logging


from pyface.tasks.i_editor_area_pane import IEditorAreaPane, MEditorAreaPane
from traits.api import observe, provides


import wx
from pyface.wx.aui import aui, PyfaceAuiNotebook


from .task_pane import TaskPane

# Logging
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# 'EditorAreaPane' class.
# ----------------------------------------------------------------------------


@provides(IEditorAreaPane)
class EditorAreaPane(TaskPane, MEditorAreaPane):
    """ The toolkit-specific implementation of a EditorAreaPane.

    See the IEditorAreaPane interface for API documentation.
    """

    style = (
        aui.AUI_NB_WINDOWLIST_BUTTON
        | aui.AUI_NB_TAB_MOVE
        | aui.AUI_NB_SCROLL_BUTTONS
        | aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
    )

    # ------------------------------------------------------------------------
    # 'TaskPane' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        logger.debug("editor pane parent: %s" % parent)
        # Create and configure the tab widget.
        self.control = control = PyfaceAuiNotebook(parent, agwStyle=self.style)

        # Connect to the widget's signals.
        control.Bind(
            aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self._update_active_editor
        )
        control.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self._close_requested)

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        for editor in self.editors:
            self.remove_editor(editor)

        super().destroy()

    # ------------------------------------------------------------------------
    # 'IEditorAreaPane' interface.
    # ------------------------------------------------------------------------

    def activate_editor(self, editor):
        """ Activates the specified editor in the pane.
        """
        index = self.control.GetPageIndex(editor.control)
        self.control.SetSelection(index)

    def add_editor(self, editor):
        """ Adds an editor to the pane.
        """
        editor.editor_area = self
        editor.create(self.control)
        self.control.AddPage(editor.control, self._get_label(editor))
        try:
            index = self.control.GetPageIndex(editor.control)
            self.control.SetPageToolTip(index, editor.tooltip)
        except AttributeError:
            pass
        self.editors.append(editor)
        self._update_tab_bar(event=None)

        # The EVT_AUINOTEBOOK_PAGE_CHANGED event is not sent when the first
        # editor is added.
        if len(self.editors) == 1:
            self.active_editor = editor

    def remove_editor(self, editor):
        """ Removes an editor from the pane.
        """
        self.editors.remove(editor)
        index = self.control.GetPageIndex(editor.control)
        logger.debug("Removing page %d" % index)
        self.control.RemovePage(index)
        editor.destroy()
        editor.editor_area = None
        self._update_tab_bar(event=None)
        if not self.editors:
            self.active_editor = None

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _get_label(self, editor):
        """ Return a tab label for an editor.
        """
        label = editor.name
        if editor.dirty:
            label = "*" + label
        if not label:
            label = " "  # bug in agw that fails on empty label
        return label

    def _get_editor_with_control(self, control):
        """ Return the editor with the specified control.
        """
        for editor in self.editors:
            if editor.control == control:
                return editor
        return None

    # Trait change handlers ------------------------------------------------

    @observe("editors:items:[dirty, name]")
    def _update_label(self, event):
        editor = event.object
        index = self.control.GetPageIndex(editor.control)
        self.control.SetPageText(index, self._get_label(editor))

    @observe("editors:items:tooltip")
    def _update_tooltip(self, event):
        editor = event.object
        self.control.SetPageToolTip(editor.control, editor.tooltip)

    # Signal handlers -----------------------------------------------------#

    def _close_requested(self, evt):
        index = evt.GetSelection()
        logger.debug("_close_requested: index=%d" % index)
        control = self.control.GetPage(index)
        editor = self._get_editor_with_control(control)

        # Veto the event even though we are going to delete the tab, otherwise
        # the notebook will delete the editor wx control and the call to
        # editor.close() will fail.  IEditorAreaPane.remove_editor() needs
        # the control to exist so it can remove it from the list of managed
        # editors.
        evt.Veto()
        editor.close()

    def _update_active_editor(self, evt):
        index = evt.GetSelection()
        logger.debug("index=%d" % index)
        if index == wx.NOT_FOUND:
            self.active_editor = None
        else:
            logger.debug("num pages=%d" % self.control.GetPageCount())
            control = self.control.GetPage(index)
            self.active_editor = self._get_editor_with_control(control)

    @observe("hide_tab_bar")
    def _update_tab_bar(self, event):
        if self.control is not None:
            pass  # Can't actually hide the tab bar on wx.aui
