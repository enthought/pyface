""" The workbench window layout interface. """


# Enthought library imports.
from enthought.traits.api import Event, Instance, Interface, Str

# Local imports.
from i_editor import IEditor


class IWorkbenchWindowLayout(Interface):
    """ The workbench window layout interface.

    Window layouts are responsible for creating and managing the internal
    structure of a workbench window (it knows how to add and remove views and
    editors etc).

    """

    # The Id of the editor area.
    editor_area_id = Str

    # The workbench window that this is the layout for.
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    #### Events ####

    # Fired when an editor is about to be opened (or restored).
    editor_opening = Event(IEditor)

    # Fired when an editor has been opened (or restored).
    editor_opened = Event(IEditor)

    # Fired when an editor is about to be closed.
    editor_closing = Event(IEditor)

    # Fired when an editor has been closed.
    editor_closed = Event(IEditor)

    def activate_editor(self, editor):
        """ Activate an editor.

        Returns the editor (just for convenience).

        """

    def activate_view(self, view):
        """ Activate a view.

        Returns the view (just for convenience).

        """

    def add_editor(self, editor, title):
        """ Add an editor.

        Returns the editor (just for convenience).

        """

    def add_view(self, view, position, relative_to=None, size=(-1, -1)):
        """ Add a view.

        Returns the view (just for convenience).

        """

    def close_editor(self, editor):
        """ Close an editor.

        Returns the editor (just for convenience).

        """

    def close_view(self, view):
        """ Close a view.

        Returns the view (just for convenience).

        """

    def close(self):
        """ Close the entire window layout.

        fixme: Should this be called 'destroy'?

        Returns None.

        """

    def create_initial_layout(self):
        """ Creates the initial window layout.

        Returns the layout.

        """

    def contains_view(self, view):
        """ Returns True if the view exists in the window layout.

        Note that this returns True even if the view is hidden.

        """
        
    def hide_editor_area(self):
        """ Hide the editor area.

        Returns None.

        """

    def hide_view(self, view):
        """ Hide a view.

        Returns the view (just for convenience).

        """

    def refresh(self):
        """ Refreshes the window layout to reflect any changes.

        Returns None.

        """

    def reset_editors(self):
        """ Activate the first editor in every group.

        Returns None.

        """

    def reset_views(self):
        """ Activate the first view in every region.

        Returns None.

        """

    def show_editor_area(self):
        """ Show the editor area.

        Returns None.

        """

    def show_view(self, view):
        """ Show a view.

        Returns None.

        """

    #### Methods for saving and restoring the layout ##########################

    def get_view_memento(self):
        """ Returns the state of the views. """

    def set_view_memento(self, memento):
        """ Restores the state of the views. """

    def get_editor_memento(self):
        """ Returns the state of the editors. """

    def set_editor_memento(self, memento):
        """ Restores the state of the editors. """

#### EOF ######################################################################
