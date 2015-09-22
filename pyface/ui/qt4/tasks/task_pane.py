# Enthought library imports.
from pyface.tasks.i_task_pane import ITaskPane, MTaskPane
from traits.api import provides

# System library imports.
from pyface.qt import QtGui

# Local imports.
from .util import set_focus


@provides(ITaskPane)
class TaskPane(MTaskPane):
    """ The toolkit-specific implementation of a TaskPane.

    See the ITaskPane interface for API documentation.
    """


    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        self.control = QtGui.QWidget(parent)

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        if self.control is not None:
            self.control.hide()
            self.control.setParent(None)
            self.control = None

    def set_focus(self):
        """ Gives focus to the control that represents the pane.
        """
        if self.control is not None:
            set_focus(self.control)
