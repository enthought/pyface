""" The editor interface. """


# Enthought library imports.
from enthought.traits.api import Any, Bool, Instance, Interface, List, Str


class IEditor(Interface):
    """ The editor interface. """

    # The optional command stack.
    command_stack = Instance('enthought.undo.api.ICommandStack')

    # The toolkit-specific control that represents the editor.
    #
    # The framework sets this to the value returned by 'create_control'.
    control = Any

    # Does the editor currently have the focus?
    has_focus = Bool(False)

    # Is the object that the editor is editing 'dirty' i.e., has it been
    # modified but not saved?
    dirty = Bool(False)

    # The editor's globally unique identifier.
    id = Str

    # The editor's name (displayed to the user).
    name = Str

    # The object that the editor is editing.
    #
    # The framework sets this when the editor is created.
    obj = Any

    # The current selection within the editor.
    selection = List

    # The workbench window that the editor is in.
    #
    # The framework sets this when the editor is created.
    window = Instance('IWorkbenchWindow')

    #### Methods ##############################################################
    
    def close(self):
        """ Close the editor.

        This method is not currently called by the framework itself as the user
        is normally in control of the editor lifecycle. Call this if you want
        to control the editor lifecycle programmatically.

        """

    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the editor.

        The parameter *parent* is the toolkit-specific control that is the 
        editor's parent.

        Returns the toolkit-specific control.
        
        """

    def destroy_control(self):
        """ Destroy the toolkit-specific control that represents the editor.

        Returns None.
        
        """

    def set_focus(self):
        """ Set the focus to the appropriate control in the editor.

        Returns None.

        """

#### EOF ######################################################################
