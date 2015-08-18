""" The default editor manager. """

# Standard library imports.
import weakref

# Enthought library imports.
from traits.api import HasTraits, Instance, provides

# Local imports.
from .i_editor_manager import IEditorManager
from .traits_ui_editor import TraitsUIEditor


@provides(IEditorManager)
class EditorManager(HasTraits):
    """ The default editor manager. """
    #### 'IEditorManager' interface ###########################################

    # The workbench window that the editor manager manages editors for ;^)
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(EditorManager, self).__init__(**traits)

        # A mapping from editor to editor kind (the factory that created them).
        self._editor_to_kind_map = weakref.WeakKeyDictionary()

        return

    ###########################################################################
    # 'IEditorManager' interface.
    ###########################################################################

    def add_editor(self, editor, kind):
        """ Registers an existing editor. """

        self._editor_to_kind_map[editor] = kind

    def create_editor(self, window, obj, kind):
        """ Create an editor for an object. """

        editor = TraitsUIEditor(window=window, obj=obj)

        self.add_editor(editor, kind)

        return editor

    def get_editor(self, window, obj, kind):
        """ Get the editor that is currently editing an object. """

        for editor in window.editors:
            if self._is_editing(editor, obj, kind):
                break
        else:
            editor = None

        return editor

    def get_editor_kind(self, editor):
        """ Return the 'kind' associated with 'editor'. """

        return self._editor_to_kind_map[editor]

    def get_editor_memento(self, editor):
        """ Return the state of an editor suitable for pickling etc.

        By default we don't save the state of editors.
        """

        return None

    def set_editor_memento(self, memento):
        """ Restore the state of an editor from a memento.

        By default we don't try to restore the state of editors.
        """

        return None

    ###########################################################################
    # 'Protected' 'EditorManager'  interface.
    ###########################################################################

    def _is_editing(self, editor, obj, kind):
        """ Return True if the editor is editing the object. """

        return editor.obj == obj

#### EOF ######################################################################
