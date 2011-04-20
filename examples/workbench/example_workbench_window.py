""" A simple example of using the workbench window. """


# Enthought library imports.
from pyface.action.api import Action, MenuManager
from pyface.workbench.api import EditorManager, WorkbenchWindow
from pyface.workbench.api import Perspective, PerspectiveItem
from pyface.workbench.action.api import MenuBarManager
from pyface.workbench.action.api import ToolBarManager
from pyface.workbench.action.api import ViewMenuManager
from traits.api import Callable, List, Instance

# Local imports.
from black_view import BlackView
from blue_view import BlueView
from green_view import GreenView
from red_view import RedView
from yellow_view import YellowView
from person import Person


class ExampleEditorManager(EditorManager):
    """ An editor manager that supports the editor memento protocol. """

    #######################################################################
    # 'IEditorManager' interface.
    #######################################################################

    def get_editor_memento(self, editor):
        """ Return the state of the editor contents. """

        # Return the data attributes as a tuple.
        return (editor.obj.name, editor.obj.age)

    def set_editor_memento(self, memento):
        """ Restore an editor from a memento and return it. """

        # Create a new data object.
        name, age = memento
        person = Person(name=name, age=age)

        # Create an editor for the data.
        return self.create_editor(self.window, person, None)


class ExampleWorkbenchWindow(WorkbenchWindow):
    """ A simple example of using the workbench window. """

    #### 'WorkbenchWindow' interface ##########################################

    # The available perspectives.
    perspectives = [
        Perspective(
            name     = 'Foo',
            contents = [
                PerspectiveItem(id='Black', position='bottom', height=0.1),
                PerspectiveItem(id='Debug', position='left', width=0.25)
            ]
        ),

        Perspective(
            name     = 'Bar',
            contents = [
                PerspectiveItem(id='Black', position='top'),
                PerspectiveItem(id='Blue', position='bottom'),
                PerspectiveItem(id='Green', position='left'),
                PerspectiveItem(id='Red', position='right'),
                PerspectiveItem(id='Debug', position='left')
            ]
        )
    ]

    #### 'ExampleWorkbenchWindow' interface ###################################

    # The view factories.
    #
    # fixme: This should be part of the standadr 'WorkbenchWindow'!
    view_factories = List(Callable)

    #### Private interface ####################################################

    # The Exit action.
    _exit_action = Instance(Action)

    # The New Person action.
    _new_person_action = Instance(Action)

    ###########################################################################
    # 'ApplicationWindow' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _editor_manager_default(self):
        """ Trait initializer.

        Here we return the replacement editor manager.
        """

        return ExampleEditorManager()

    def _menu_bar_manager_default(self):
        """ Trait initializer. """

        file_menu = MenuManager(
            self._new_person_action, self._exit_action,
            name='&File', id='FileMenu'
        )
        view_menu = ViewMenuManager(name='&View', id='ViewMenu', window=self)

        return MenuBarManager(file_menu, view_menu, window=self)

    def _tool_bar_managers_default(self):
        """ Trait initializer. """

        # Add multiple (albeit identical!) tool bars just to show that it is
        # allowed!
        tool_bar_managers = [
            ToolBarManager(
                self._exit_action, show_tool_names = False, name=str(i)
            )

            for i in range(5)
        ]

        return tool_bar_managers

    ###########################################################################
    # 'WorkbenchWindow' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _view_factories_default(self):
        """ Trait initializer. """

        from pyface.workbench.debug.api import DebugView

        return [DebugView, BlackView, BlueView, GreenView, RedView, YellowView]

    def _views_default(self):
        """ Trait initializer. """

        # Using an initializer makes sure that every window instance gets its
        # own view instances (which is necessary since each view has a
        # reference to its toolkit-specific control etc.).
        return [factory(window=self) for factory in self.view_factories]

    ###########################################################################
    # Private interface.
    ###########################################################################

    def __exit_action_default(self):
        """ Trait initializer. """

        return Action(name='E&xit', on_perform=self.workbench.exit)

    def __new_person_action_default(self):
        """ Trait initializer. """

        return Action(name='New Person', on_perform=self._new_person)

    def _new_person(self):
        """ Create a new person. """

        from person import Person

        self.workbench.edit(Person(name='New', age=100))

        return

#### EOF ######################################################################
