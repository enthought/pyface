# Enthought library imports.
from enthought.traits.api import Bool, Enum, Str, Tuple, implements

# Local imports.
from i_task_pane import ITaskPane, MTaskPane


class IDockPane(ITaskPane):
    """ A pane that is useful but unessential for a task.

    Dock panes are arranged around the central pane in dock areas, and can, in
    general, be moved, resized, and hidden by the user.
    """
    
    # If enabled, the pane will have a button to close it, and a visibility
    # toggle button will be added to the View menu. Otherwise, the pane's
    # visibility will only be adjustable programmatically, though the 'visible'
    # attribute.
    closable = Bool(True)

    # The dock area in which the pane is currently present.
    dock_area = Enum('left', 'right', 'top', 'bottom')

    # Whether the pane can be detached from the main window.
    floatable = Bool(True)

    # Whether the pane is currently detached from the main window.
    floating = Bool(False)

    # Whether the pane can be moved from one dock area to another.
    movable = Bool(True)

    # An optional initial size hint for the dock pane.
    size = Tuple(-1, -1)

    # Whether the pane is currently visible.
    visible = Bool(True)

    ###########################################################################
    # 'IDockPane' interface.
    ###########################################################################

    def create_contents(self):
        """ Create and return the toolkit-specific contents of the dock pane.
        """

    def hide(self):
        """ Convenience method to hide the dock pane.
        """

    def show(self):
        """ Convenience method to show the dock pane.
        """

        
class MDockPane(MTaskPane):
    """ Mixin containing common code for toolkit-specific implementations.
    """ 

    implements(IDockPane)

    #### 'IDockPane' interface ################################################

    closable = Bool(True)
    dock_area = Enum('left', 'right', 'top', 'bottom')
    floatable = Bool(True)
    floating = Bool(False)
    movable = Bool(True)
    size = Tuple(-1, -1)
    visible = Bool(True)

    ###########################################################################
    # 'IDockPane' interface.
    ###########################################################################

    def create_contents(self):
        """ Create and return the toolkit-specific contents of the dock pane.
        """
        raise NotImplementedError

    def hide(self):
        """ Convenience method to hide the dock pane.
        """
        self.visible = False

    def show(self):
        """ Convenience method to show the dock pane.
        """
        self.visible = True
