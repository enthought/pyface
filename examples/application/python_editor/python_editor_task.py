# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Example Python Editor Task
==========================

This is a Task that provides an editor pane and file browser, along with
support for opening and editing Python files.  Much of this class is simply
creating and hooking up menus and toolbars to appropriate methods, but the
task also handles checking for unsaved files before closing and updating
window name and status bar depending on the state of the task and editor.
"""

import os
import sys
import webbrowser

from pyface.api import (
    CANCEL,
    ConfirmationDialog,
    FileDialog,
    ImageResource,
    OK,
    YES,
    error,
)
from pyface.action.api import Action, StatusBarManager
from pyface.tasks.api import (
    EditorAreaPane,
    IEditor,
    IEditorAreaPane,
    PaneItem,
    Task,
    TaskLayout,
)
from pyface.tasks.action.api import (
    DockPaneToggleGroup,
    EditorAction,
    SGroup,
    SMenu,
    SMenuBar,
    SToolBar,
    TaskAction,
)
from traits.api import (
    Instance,
    Property,
    Str,
    cached_property,
    observe,
)

from python_browser_pane import PythonBrowserPane
from python_editor import PythonEditor

PYTHON_DOCS = "https://docs.python.org/{}.{}".format(*sys.version_info[:2])


class OpenURLAction(Action):
    """ An action that opens a web page in the system's default browser. """

    #: The URL to open.
    url = Str()

    def perform(self, event=None):
        """ Open a URL in a web browser. """
        try:
            webbrowser.open(self.url)
        except webbrowser.Error as exc:
            error(None, str(exc))


class PythonEditorTask(Task):
    """ A simple task for editing Python code.
    """

    # 'Task' traits -----------------------------------------------------------

    #: The unique id of the task.
    id = "example.python_editor_task"

    #: The human-readable name of the task.
    name = "Python Editor"

    #: The currently active editor in the editor area, if any.
    active_editor = Property(
        Instance(IEditor), observe="editor_area.active_editor"
    )

    #: The editor area for this task.
    editor_area = Instance(IEditorAreaPane)

    #: The menu bar for the task.
    menu_bar = SMenuBar(
        SMenu(
            SGroup(
                TaskAction(name="New", method="new", accelerator="Ctrl+N"),
                id="new_group",
            ),
            SGroup(
                TaskAction(
                    name="Open...", method="open", accelerator="Ctrl+O"
                ),
                id="open_group",
            ),
            SGroup(
                TaskAction(
                    name="Save",
                    method="save",
                    accelerator="Ctrl+S",
                    enabled_name="active_editor.dirty",
                ),
                TaskAction(
                    name="Save As...",
                    method="save_as",
                    accelerator="Ctrl+Shift+S",
                ),
                id="save_group",
            ),
            SGroup(
                TaskAction(
                    name="Close Editor",
                    method="close_editor",
                    accelerator="Ctrl+W",
                ),
                id="close_group",
            ),
            id="File",
            name="&File",
        ),
        SMenu(
            SGroup(
                EditorAction(
                    name="Undo",
                    method="undo",
                    enabled_name="can_undo",
                    accelerator="Ctrl+Z",
                ),
                EditorAction(
                    name="Redo",
                    method="redo",
                    enabled_name="can_redo",
                    accelerator="Ctrl+Shift+Z",
                ),
                id="undo_group",
            ),
            SGroup(
                EditorAction(
                    name="Go to Line...",
                    method="go_to_line",
                    accelerator="Ctrl+G",
                ),
                id="search_group",
            ),
            id="Edit",
            name="&Edit",
        ),
        SMenu(DockPaneToggleGroup(), id="View", name="&View"),
        SMenu(
            SGroup(
                OpenURLAction(
                    name="Python Documentation",
                    id="python_docs",
                    url=PYTHON_DOCS,
                ),
                id="documentation_group",
            ),
            id="Help",
            name="&Help",
        ),
    )

    #: The tool bars for the task.
    tool_bars = [
        SToolBar(
            TaskAction(
                method="new",
                tooltip="New file",
                image=ImageResource("document_new"),
            ),
            TaskAction(
                method="open",
                tooltip="Open a file",
                image=ImageResource("document_open"),
            ),
            TaskAction(
                method="save",
                tooltip="Save the current file",
                image=ImageResource("document_save"),
                enabled_name="active_editor.dirty",
            ),
            image_size=(16, 16),
            show_tool_names=False,
        )
    ]

    #: The status bar for the window when this task is active.
    status_bar = Instance(StatusBarManager, ())

    # -------------------------------------------------------------------------
    # 'PythonEditorTask' interface.
    # -------------------------------------------------------------------------

    def create_editor(self, path=""):
        """ Create a new editor in the editor pane.

        Parameters
        ----------
        path : path or ''
            The path to the file to edit, or '' for an empty editor.
        """
        if path:
            path = os.path.abspath(path)
        use_existing = path != ""
        self.editor_area.edit(
            path, factory=PythonEditor, use_existing=use_existing
        )
        if path:
            self.active_editor.load()

    def close_editor(self):
        """ Close the active editor, or if no editors, close the Task window.
        """
        if self.editor_area.active_editor is not None:
            self.editor_area.remove_editor(self.editor_area.active_editor)
        else:
            self.window.close()

    def new(self):
        """ Open a new empty window
        """
        self.create_editor()

    def open(self):
        """ Shows a dialog to open a Python file.
        """
        dialog = FileDialog(parent=self.window.control, wildcard="*.py")
        if dialog.open() == OK:
            self.create_editor(dialog.path)

    def save(self):
        """ Save the current file.

        If needed, this code prompts for a path.

        Returns
        -------
        saved : bool
            Whether or not the file was saved.
        """
        editor = self.active_editor
        try:
            editor.save()
        except IOError:
            # If you are trying to save to a file that doesn't exist, open up a
            # FileDialog with a 'save as' action.
            dialog = FileDialog(
                parent=self.window.control, action="save as", wildcard="*.py"
            )
            if dialog.open() == OK:
                editor.save(dialog.path)
            else:
                return False
        return True

    # -------------------------------------------------------------------------
    # 'Task' interface.
    # -------------------------------------------------------------------------

    def _default_layout_default(self):
        """ The default layout with the browser pane on the left.
        """
        return TaskLayout(
            left=PaneItem("example.python_browser_pane", width=200)
        )

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        self.editor_area = EditorAreaPane()
        return self.editor_area

    def create_dock_panes(self):
        """ Create the file browser and connect to its double click event.
        """
        browser = PythonBrowserPane()

        def handler(event):
            path = event.new
            if os.path.isfile(path):
                return self.create_editor(path)

        browser.observe(handler, "activated")
        return [browser]

    # -------------------------------------------------------------------------
    # Protected interface.
    # -------------------------------------------------------------------------

    def _prompt_for_save(self):
        """ Prompts the user to save if necessary. Returns whether the dialog
            was cancelled.
        """
        dirty_editors = {
            editor.name: editor
            for editor in self.editor_area.editors
            if editor.dirty and (editor.obj or editor.code)
        }
        if not dirty_editors:
            return True

        message = "You have unsaved files. Would you like to save them?"
        dialog = ConfirmationDialog(
            parent=self.window.control,
            message=message,
            cancel=True,
            default=CANCEL,
            title="Save Changes?",
        )
        result = dialog.open()
        if result == CANCEL:
            return False
        elif result == YES:
            for name, editor in dirty_editors.items():
                editor.save(editor.path)
        return True

    # Trait change handlers --------------------------------------------------

    @observe("window:closing")
    def _prompt_on_close(self, event):
        """ Prompt the user to save when exiting.
        """
        close = self._prompt_for_save()
        window = event.new
        window.veto = not close

    @observe("active_editor.name")
    def _change_title(self, event):
        """ Update the window title when the active editor changes.
        """
        if self.window.active_task == self:
            if self.active_editor is not None:
                self.window.title = self.active_editor.name
            else:
                self.window.title = self.name

    @observe("active_editor.[line,column,selection_length]")
    def _update_status(self, event):
        if self.active_editor is not None:
            editor = self.active_editor
            if editor.selection_length:
                self.status_bar.messages = [
                    "Ln {}, Col {} ({} selected)".format(
                        editor.line, editor.column, editor.selection_length
                    )
                ]
            else:
                self.status_bar.messages = [
                    "Ln {}, Col {}".format(editor.line, editor.column)
                ]
        else:
            self.status_bar.messages = []

    # Trait property getter/setters ------------------------------------------

    @cached_property
    def _get_active_editor(self):
        if self.editor_area is not None:
            return self.editor_area.active_editor
        return None
