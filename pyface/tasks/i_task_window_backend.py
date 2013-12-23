# Enthought library imports.
from traits.api import Any, DelegatesTo, HasTraits, Instance, Interface, \
    provides


class ITaskWindowBackend(Interface):
    """ The TaskWindow layout interface.

    TaskWindow delegates to an ITaskWindowBackend object for toolkit-specific
    layout functionality.
    """

    # The root control of the TaskWindow to which the layout belongs.
    control = Any

    # The TaskWindow to which the layout belongs.
    window = Instance('pyface.tasks.task_window.TaskWindow')

    ###########################################################################
    # 'ITaskWindowBackend' interface.
    ###########################################################################

    def create_contents(self, parent):
        """ Create and return the TaskWindow's contents. (See IWindow.)
        """

    def destroy(self):
        """ Destroy the backend.

        Note that TaskWindow will destroy the widget created in create_contents,
        but this method may be used to perform additional cleanup.
        """

    def begin_batch_window_updates(self):
        """ Hint that a large number of window updates are pending
        
        Hook for toolkits that can provide a method to prevent window redrawing
        while layout updates of the controls is taking place.  If used, must
        be followed with a call to end_batch_window_updates.
        """

    def end_batch_window_updates(self):
        """ Restore normal window redrawing after begin_batch_window_updates
        """

    def hide_task(self, state):
        """ Assuming the specified TaskState is active, hide its controls.
        """

    def show_task(self, state):
        """ Assuming no task is currently active, show the controls of the
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


@provides(ITaskWindowBackend)
class MTaskWindowBackend(HasTraits):
    """ Mixin containing common coe for toolkit-specific implementations.
    """


    #### 'ITaskWindowBackend' interface #######################################

    control = DelegatesTo('window')
    window = Instance('pyface.tasks.task_window.TaskWindow')

    ###########################################################################
    # 'ITaskWindowBackend' interface.
    ###########################################################################

    def create_contents(self, parent):
        raise NotImplementedError

    def destroy(self):
        pass

    def begin_batch_window_updates(self):
        pass

    def end_batch_window_updates(self):
        pass

    def hide_task(self, state):
        raise NotImplementedError

    def show_task(self, state):
        raise NotImplementedError

    def get_layout(self):
        raise NotImplementedError

    def set_layout(self, layout):
        raise NotImplementedError
