"""Incremental demo for wx support of tasks.

Create and delete task panes
"""
# Enthought library imports.
from pyface.api import GUI, ConfirmationDialog, FileDialog, \
    ImageResource, YES, OK, CANCEL
from pyface.tasks.api import Task, TaskWindow, TaskLayout, PaneItem, IEditor, \
    IEditorAreaPane, EditorAreaPane, Editor, DockPane
from pyface.tasks.action.api import DockPaneToggleGroup, SMenuBar, \
    SMenu, SToolBar, TaskAction
from traits.api import on_trait_change, Property, Instance

class ExamplePane(DockPane):
    """ A simple file browser pane.
    """

    #### TaskPane interface ###################################################

    id = 'steps.example_pane'
    name = 'Example Pane'

class ExampleTask(Task):
    """ A simple task for opening a blank editor.
    """

    #### Task interface #######################################################

    id = 'example.example_task'
    name = 'Multi-Tab Editor'

    active_editor = Property(Instance(IEditor),
                             depends_on='editor_area.active_editor')

    editor_area = Instance(IEditorAreaPane)

    menu_bar = SMenuBar(SMenu(TaskAction(name='New', method='new',
                                         accelerator='Ctrl+N'),
                              id='File', name='&File'),
                        SMenu(DockPaneToggleGroup(),
                              id='View', name='&View'))

    tool_bars = [ SToolBar(TaskAction(method='new',
                                      tooltip='New file',
                                      image=ImageResource('document_new')),
                           image_size = (32, 32)), ]

    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def _default_layout_default(self):
        return TaskLayout(
            top=PaneItem('steps.example_pane'))

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        self.editor_area = EditorAreaPane()
        return self.editor_area

    def create_dock_panes(self):
        """ Create the file browser and connect to its double click event.
        """
        pane = ExamplePane()
        return [ pane ]

    ###########################################################################
    # 'ExampleTask' interface.
    ###########################################################################

    def new(self):
        """ Opens a new empty window
        """
        editor = Editor()
        self.editor_area.add_editor(editor)
        self.editor_area.activate_editor(editor)
        self.activated()

    #### Trait property getter/setters ########################################

    def _get_active_editor(self):
        if self.editor_area is not None:
            return self.editor_area.active_editor
        return None

def main(argv):
    """ A simple example of using Tasks.
    """
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create a Task and add it to a TaskWindow.
    task = ExampleTask()
    window = TaskWindow(size=(800, 600))
    window.add_task(task)

    # Show the window.
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()


if __name__ == '__main__':
    import sys
    main(sys.argv)
