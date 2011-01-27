# Enthought library imports.
from enthought.traits.api import Any, Bool, HasTraits, Interface, Instance, \
     Str, Unicode, implements

# Local imports.
from task import Task


class ITaskPane(Interface):
    """ The base interface for all panes (central and dock) in a Task.
    """

    # The pane's identifier, unique within a Task.
    id = Str

    # The pane's user-visible name.
    name = Unicode
    
    # The toolkit-specific control that represents the pane.
    control = Any

    # Does the pane currently have focus?
    has_focus = Bool

    # The task with which the pane is associated. Set by the framework.
    task = Instance(Task)

    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """

    def set_focus(self):
        """ Gives focus to the control that represents the pane.
        """


class MTaskPane(HasTraits):
    """ Mixin containing common code for toolkit-specific implementations.
    """ 

    implements(ITaskPane)
    
    #### 'ITaskPane' interface ################################################

    id = Str
    name = Str
    control = Any
    has_focus = Bool
    task = Instance(Task)

    def create(self, parent):
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError

    def set_focus(self):
        raise NotImplementedError
