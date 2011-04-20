""" The editor manager interface. """


# Enthought library imports.
from traits.api import Instance, Interface


class IEditorManager(Interface):
    """ The editor manager interface. """

    # The workbench window that the editor manager manages editors for ;^)
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    def add_editor(self, editor, kind):
        """ Registers an existing editor. """

    def create_editor(self, window, obj, kind):
        """ Create an editor for an object.

        'kind' optionally contains any data required by the specific editor
        manager implementation to decide what type of editor to create.

        Returns None if no editor can be created for the resource.
        """

    def get_editor(self, window, obj, kind):
        """ Get the editor that is currently editing an object.

        'kind' optionally contains any data required by the specific editor
        manager implementation to decide what type of editor to create.

        Returns None if no such editor exists.
        """

    def get_editor_kind(self, editor):
        """ Return the 'kind' associated with 'editor'. """

    def get_editor_memento(self, editor):
        """ Return the state of an editor suitable for pickling etc.
        """

    def set_editor_memento(self, memento):
        """ Restore an editor from a memento and return it. """

#### EOF ######################################################################
