# Enthought library imports.
from enthought.traits.api import Any, DelegatesTo, HasTraits, Instance, \
     Interface, implements

class ITaskWindowLayout(Interface):
    """ The TaskWindow layout interface.

    TaskWindow delegates to an ITaskWindowLayout object for toolkit-specific
    layout functionality.
    """

    # The root control of the TaskWindow to which the layout belongs.
    control = Any

    # The TaskWindow to which the layout belongs.
    window = Instance('enthought.pyface.tasks.task_window.TaskWindow')

    ###########################################################################
    # 'ITaskWindowLayout' interface.
    ###########################################################################

    def create_contents(self, parent):
        """ Create and return the TaskWindow's contents. (See IWindow.)
        """

    def hide_task(self, state):
        """ Assuming the specified TaskState is active, hide its controls.
        """

    def show_task(self, state):
        """ Assumming no task is currently active, show the controls of the
            specified TaskState.
        """

    #### Methods for saving and restoring the layout ##########################

    def get_layout(self):
        """ Returns a TaskLayout for the current state of the window.
        """

    def set_layout(self, layout):
        """ Applies a TaskLayout (which should be suitable for the active task)
            to the window.
        """

    
class MTaskWindowLayout(HasTraits):
    """ Mixin containing common coe for toolkit-specific implementations.
    """
    
    implements(ITaskWindowLayout)

    #### 'ITaskWindowLayout' interface ########################################

    control = DelegatesTo('window')

    window = Instance('enthought.pyface.tasks.task_window.TaskWindow')

    def create_contents(self, parent):
        raise NotImplementedError

    def hide_task(self, state):
        raise NotImplementedError

    def show_task(self, state):
        raise NotImplementedError

    def get_layout(self):
        raise NotImplementedError

    def set_layout(self, layout):
        raise NotImplementedError
