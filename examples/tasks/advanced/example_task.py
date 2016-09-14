# Enthought library imports.
from pyface.tasks.api import Task, TaskLayout, PaneItem, IEditor, \
    IEditorAreaPane, EditorAreaPane
from pyface.tasks.action.api import DockPaneToggleGroup, SMenuBar, \
    SMenu, SToolBar, TaskAction
from pyface.api import ConfirmationDialog, FileDialog, \
    ImageResource, YES, OK, CANCEL
from traits.api import on_trait_change, Property, Instance

# Local imports.
from example_panes import PythonScriptBrowserPane
from python_editor import PythonEditor

class ExampleTask(Task):
    """ A simple task for editing Python code.
    """

    #### Task interface #######################################################

    id = 'example.example_task'
    name = 'Multi-Tab Editor'

    active_editor = Property(Instance(IEditor),
                             depends_on='editor_area.active_editor')

    editor_area = Instance(IEditorAreaPane)

    menu_bar = SMenuBar(SMenu(TaskAction(name='New', method='new',
                                         accelerator='Ctrl+N'),
                              TaskAction(name='Open...', method='open',
                                         accelerator='Ctrl+O'),
                              TaskAction(name='Save', method='save',
                                         accelerator='Ctrl+S'),
                              id='File', name='&File'),
                        SMenu(DockPaneToggleGroup(),
                              id='View', name='&View'))

    tool_bars = [ SToolBar(TaskAction(method='new',
                                      tooltip='New file',
                                      image=ImageResource('document_new')),
                           TaskAction(method='open',
                                      tooltip='Open a file',
                                      image=ImageResource('document_open')),
                           TaskAction(method='save',
                                      tooltip='Save the current file',
                                      image=ImageResource('document_save')),
                           image_size = (32, 32), show_tool_names=False), ]

    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def _default_layout_default(self):
        return TaskLayout(
            left=PaneItem('example.python_script_browser_pane'))

    def activated(self):
        """ Overriden to set the window's title.
        """
        return
        filename = self.active_editor.path if self.active_editor else ''
        self.window.title = filename if filename else 'Untitled'

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        self.editor_area = EditorAreaPane()
        return self.editor_area

    def create_dock_panes(self):
        """ Create the file browser and connect to its double click event.
        """
        browser = PythonScriptBrowserPane()
        handler = lambda: self._open_file(browser.selected_file)
        browser.on_trait_change(handler, 'activated')
        return [ browser ]

    ###########################################################################
    # 'ExampleTask' interface.
    ###########################################################################

    def new(self):
        """ Opens a new empty window
        """
        editor = PythonEditor()
        self.editor_area.add_editor(editor)
        self.editor_area.activate_editor(editor)
        self.activated()

    def open(self):
        """ Shows a dialog to open a file.
        """
        dialog = FileDialog(parent=self.window.control, wildcard='*.py')
        if dialog.open() == OK:
            self._open_file(dialog.path)

    def save(self):
        """ Attempts to save the current file, prompting for a path if
            necessary. Returns whether the file was saved.
        """
        editor = self.active_editor
        try:
            editor.save()
        except IOError:
            # If you are trying to save to a file that doesn't exist, open up a
            # FileDialog with a 'save as' action.
            dialog = FileDialog(parent=self.window.control,
                                action='save as', wildcard='*.py')
            if dialog.open() == OK:
                editor.save(dialog.path)
            else:
                return False
        return True

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _open_file(self, filename):
        """ Opens the file at the specified path in the editor.
        """
        editor = PythonEditor(path=filename)
        self.editor_area.add_editor(editor)
        self.editor_area.activate_editor(editor)
        self.activated()

    def _prompt_for_save(self):
        """ Prompts the user to save if necessary. Returns whether the dialog
            was cancelled.
        """
        dirty_editors = dict([(editor.name, editor)
                              for editor in self.editor_area.editors
                              if editor.dirty])
        if not dirty_editors.keys():
            return True
        message = 'You have unsaved files. Would you like to save them?'
        dialog = ConfirmationDialog(parent=self.window.control,
                                    message=message, cancel=True,
                                    default=CANCEL, title='Save Changes?')
        result = dialog.open()
        if result == CANCEL:
            return False
        elif result == YES:
            for name, editor in dirty_editors.items():
                editor.save(editor.path)
        return True

    #### Trait change handlers ################################################

    @on_trait_change('window:closing')
    def _prompt_on_close(self, event):
        """ Prompt the user to save when exiting.
        """
        close = self._prompt_for_save()
        event.veto = not close

    #### Trait property getter/setters ########################################

    def _get_active_editor(self):
        if self.editor_area is not None:
            return self.editor_area.active_editor
        return None
