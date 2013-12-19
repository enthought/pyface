# Standard library imports.
import sys

# Enthought library imports.
from pyface.tasks.i_editor_area_pane import IEditorAreaPane, \
    MEditorAreaPane
from traits.api import on_trait_change, provides

# System library imports.
from wx.lib.agw import aui

# Local imports.
from task_pane import TaskPane
from util import set_focus

###############################################################################
# 'EditorAreaPane' class.
###############################################################################

@provides(IEditorAreaPane)
class EditorAreaPane(TaskPane, MEditorAreaPane):
    """ The toolkit-specific implementation of a EditorAreaPane.

    See the IEditorAreaPane interface for API documentation.
    """

    style = aui.AUI_NB_WINDOWLIST_BUTTON|aui.AUI_NB_TAB_MOVE|aui.AUI_NB_SCROLL_BUTTONS|aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
    
    ###########################################################################
    # 'TaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        print "editor pane parent: %s" % parent
        # Create and configure the tab widget.
        self.control = control = aui.AuiNotebook(parent, agwStyle=self.style, size=(1000, 1000))
#        control.tabBar().setVisible(not self.hide_tab_bar)

        # Connect to the widget's signals.
        control.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self._update_active_editor)
        control.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self._close_requested)
#        control.Bind(aui.EVT_AUINOTEBOOK_TAB_RIGHT_DOWN, self.OnTabContextMenu)
#        control.Bind(aui.EVT_AUINOTEBOOK_BG_RIGHT_DOWN, self.OnTabBackgroundContextMenu)

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        for editor in self.editors:
            self.remove_editor(editor)

        super(EditorAreaPane, self).destroy()

    ###########################################################################
    # 'IEditorAreaPane' interface.
    ###########################################################################

    def activate_editor(self, editor):
        """ Activates the specified editor in the pane.
        """
        self.control.SetSelectionToWindow(editor.control)
        
    def add_editor(self, editor):
        """ Adds an editor to the pane.
        """
        editor.editor_area = self
        editor.create(self.control)
        self.control.AddPage(editor.control, self._get_label(editor))
        self.control.SetPageToolTip(editor.control, editor.tooltip)
        self.editors.append(editor)
        self._update_tab_bar()

        # The 'currentChanged' signal, used below, is not emitted when the first
        # editor is added.
        if len(self.editors) == 1:
            self.active_editor = editor

    def remove_editor(self, editor):
        """ Removes an editor from the pane.
        """
        self.editors.remove(editor)
        self.control.removeTab(self.control.indexOf(editor.control))
        editor.destroy()
        editor.editor_area = None
        self._update_tab_bar()
        if not self.editors:
            self.active_editor = None

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_label(self, editor):
        """ Return a tab label for an editor.
        """
        label = editor.name
        if editor.dirty:
            label = '*' + label
        return label

    def _get_editor_with_control(self, control):
        """ Return the editor with the specified control.
        """
        for editor in self.editors:
            if editor.control == control:
                return editor
        return None

    def _next_tab(self):
        """ Activate the tab after the currently active tab.
        """
        self.control.setCurrentIndex(self.control.currentIndex() + 1)

    def _previous_tab(self):
        """ Activate the tab before the currently active tab.
        """
        self.control.setCurrentIndex(self.control.currentIndex() - 1)

    #### Trait change handlers ################################################

    @on_trait_change('editors:[dirty, name]')
    def _update_label(self, editor, name, new):
        self.control.SetPageText(editor.control, self._get_label(editor))

    @on_trait_change('editors:tooltip')
    def _update_tooltip(self, editor, name, new):
        self.control.SetPageToolTip(editor.control, editor.tooltip)

    #### Signal handlers ######################################################

    def _close_requested(self, index):
        control = self.control.GetPage(index)
        editor = self._get_editor_with_control(control)
        editor.close()
        
    def _update_active_editor(self, evt):
        index = evt.GetSelection()
        if index == -1:
            self.active_editor = None
        else:
            control = self.control.GetPage(index)
            self.active_editor = self._get_editor_with_control(control)

    @on_trait_change('hide_tab_bar')
    def _update_tab_bar(self):
        if self.control is not None:
            visible = self.control.GetPageCount() > 1 if self.hide_tab_bar else True
            self.control.tabBar().setVisible(visible)
