"""Incremental demo for wx support of tasks.

Multiple tasks

Note that naively subclassing SecondTask from ExampleTask, it initially used
the same menu_bar and tool_bars traits from ExampleTask.  This caused the
incorrect tying of the controls to SecondTask because the class attributes
were shared between both classes.
"""
# Enthought library imports.
from pyface.api import GUI, ConfirmationDialog, FileDialog, \
    ImageResource, YES, OK, CANCEL
from pyface.tasks.api import Task, TaskWindow, TaskLayout, PaneItem, IEditor, \
    IEditorAreaPane, EditorAreaPane, Editor, DockPane, HSplitter, VSplitter
from pyface.tasks.action.api import DockPaneToggleGroup, SMenuBar, \
    SMenu, SToolBar, TaskAction, TaskToggleGroup
from traits.api import on_trait_change, Property, Instance

class Pane1(DockPane):
    #### TaskPane interface ###################################################

    id = 'steps.pane1'
    name = 'Pane 1'

class Pane2(DockPane):
    #### TaskPane interface ###################################################

    id = 'steps.pane2'
    name = 'Pane 2'

class Pane3(DockPane):
    #### TaskPane interface ###################################################

    id = 'steps.pane3'
    name = 'Pane 3'

class Pane4(DockPane):
    #### TaskPane interface ###################################################

    id = 'steps.pane4'
    name = 'Pane 4'

class Pane5(DockPane):
    #### TaskPane interface ###################################################

    id = 'steps.pane5'
    name = 'Pane 5'

class Pane6(DockPane):
    #### TaskPane interface ###################################################

    id = 'steps.pane6'
    name = 'Pane 6'

class Pane7(DockPane):
    #### TaskPane interface ###################################################

    id = 'steps.pane7'
    name = 'Pane 7'

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
                              TaskToggleGroup(),
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
            top=HSplitter(
                PaneItem('steps.pane1'),
                PaneItem('steps.pane2'),
                PaneItem('steps.pane3'),
                ))

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        self.editor_area = EditorAreaPane()
        return self.editor_area

    def create_dock_panes(self):
        """ Create the file browser and connect to its double click event.
        """
        return [ Pane1(), Pane2(), Pane3() ]

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

class SecondTask(ExampleTask):
    """ A simple task for opening a blank editor.
    """

    #### Task interface #######################################################

    id = 'example.second_task'
    name = 'Second Multi-Tab Editor'

    menu_bar = SMenuBar(SMenu(TaskAction(name='New', method='new',
                                         accelerator='Ctrl+N'),
                              id='File', name='&File'),
                        SMenu(DockPaneToggleGroup(),
                              TaskToggleGroup(),
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
            left=VSplitter(
                PaneItem('steps.pane1'),
                PaneItem('steps.pane2'),
                PaneItem('steps.pane3'),
                ))
            
def main(argv):
    """ A simple example of using Tasks.
    """
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create a Task and add it to a TaskWindow.
    task1 = ExampleTask()
    task2 = SecondTask()
    window = TaskWindow(size=(800, 600))
    window.add_task(task1)
    window.add_task(task2)

    # Show the window.
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()


if __name__ == '__main__':
    import sys
    main(sys.argv)
