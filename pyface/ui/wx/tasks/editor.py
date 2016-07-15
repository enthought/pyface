# Enthought library imports.
from pyface.tasks.i_editor import IEditor, MEditor
from traits.api import Bool, Property, provides

# System library imports.
import wx


@provides(IEditor)
class Editor(MEditor):
    """ The toolkit-specific implementation of a Editor.

    See the IEditor interface for API documentation.
    """


    #### 'IEditor' interface ##################################################

    has_focus = Property(Bool)

    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        self.control = wx.Window(parent, name="Editor")

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        if self.control is not None:
            self.control.Destroy()
            self.control = None

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_has_focus(self):
        if self.control is not None:
            return self.control.FindFocus() == self.control
        return False
