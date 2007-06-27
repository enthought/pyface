""" A simple example of using the workbench window. """


# Enthought library imports.
from enthought.pyface.action.api import Action, MenuManager
from enthought.pyface.workbench.api import WorkbenchWindow, Perspective
from enthought.pyface.workbench.api import PerspectiveItem
from enthought.pyface.workbench.action.api import MenuBarManager
from enthought.pyface.workbench.action.api import ToolBarManager
from enthought.pyface.workbench.action.api import ViewMenuManager

# Local imports.
from black_view import BlackView
from blue_view import BlueView
from green_view import GreenView
from red_view import RedView
from yellow_view import YellowView


# Until TraitsUI supports PyQt we provide an alternative editor manager that
# creates bespoke editors if PyQt is the selected toolkit.
from enthought.etsconfig.api import ETSConfig
from enthought.pyface.workbench.api import Editor, EditorManager


class _TkEditorManager(EditorManager):
    """ An editor manager to allow the example to work with Qt4. """
    
    class _PyQt4PersonEditor(Editor):
        """ A Qt4 editor for 'Person' objects. """

        #######################################################################
        # 'IEditor' interface.
        #######################################################################

        #### Initializers #####################################################
        
        def _name_default(self):
            """ Trait initializer. """
            
            return str(self.obj)

        #### Initializers #####################################################

        def create_control(self, parent):
            """ Create the toolkit-specific control that represents the editor.

            """

            from PyQt4 import QtGui

            lay = QtGui.QGridLayout()

            lay.addWidget(QtGui.QLabel("Age"), 0, 0)
            lay.addWidget(QtGui.QLineEdit(str(self.obj.age)), 0, 1)

            lay.addWidget(QtGui.QLabel("Name"), 1, 0)
            lay.addWidget(QtGui.QLineEdit(self.obj.name), 1, 1)

            lay.setRowStretch(2, 1)

            ui = QtGui.QWidget(parent)
            ui.setLayout(lay)

            return ui

    #######################################################################
    # 'IEditorManager' interface.
    #######################################################################

    def create_editor(self, window, obj, kind):
        """ Create an editor for an object. """
        
        if ETSConfig.toolkit == 'qt4':
            editor = self._PyQt4PersonEditor(window=window, obj=obj)

        else:
            editor = EditorManager.create_editor(self, window, obj, kind)

        return editor


class ExampleWorkbenchWindow(WorkbenchWindow):
    """ A simple example of using the workbench window. """

    #### 'WorkbenchWindow' interface ##########################################

    # The available perspectives.
    perspectives = [
        Perspective(
            name     = 'Foo',
            contents = [
                PerspectiveItem(id='Black', position='bottom')
            ]
        ),
        
        Perspective(
            name     = 'Bar',
            contents = [
                PerspectiveItem(id='Black', position='top'),
                PerspectiveItem(id='Blue', position='bottom'),
                PerspectiveItem(id='Green', position='left'),
                PerspectiveItem(id='Red', position='right')
            ]
        )
    ]

    ###########################################################################
    # 'ApplicationWindow' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _editor_manager_default(self):
        """ Trait initializer.

        Here we return the replacement editor manager (until TraitsUI supports
        PyQt).

        """
        
        return _TkEditorManager()
    
    def _menu_bar_manager_default(self):
        """ Trait initializer. """

        # Actions.
        exit_action = Action(name='E&xit', on_perform=self.workbench.exit)

        # Menus.
        file_menu = MenuManager(exit_action, name='&File', id='FileMenu')
        view_menu = ViewMenuManager(name='&View', id='ViewMenu', window=self)
        
        return MenuBarManager(file_menu, view_menu, window=self)

    def _tool_bar_manager_default(self):
        """ Trait initializer. """

        exit_action = Action(name='E&xit', on_perform=self.workbench.exit)

        tool_bar_manager = ToolBarManager(
            exit_action,
            show_tool_names = False
        )

        return tool_bar_manager
    
    ###########################################################################
    # 'WorkbenchWindow' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _views_default(self):
        """ Trait initializer. """

        # Using an initializer makes sure that every window instance gets its
        # own view instances (which is necessary since each view has a
        # reference to its toolkit-specific control etc.).
        return [BlackView(), BlueView(), GreenView(), RedView(), YellowView()]

#### EOF ######################################################################
