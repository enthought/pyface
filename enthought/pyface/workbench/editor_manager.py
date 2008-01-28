""" The default editor manager. """


# Enthought library imports.
from enthought.traits.api import HasTraits, Instance, implements

# Local imports.
from i_editor_manager import IEditorManager
from traits_ui_editor import TraitsUIEditor


class EditorManager(HasTraits):
    """ The default editor manager. """

    implements(IEditorManager)

    #### 'IEditorManager' interface ###########################################

    # The workbench window that the editor manager manages editors for ;^)
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')
    
    ###########################################################################
    # 'IEditorManager' interface.
    ###########################################################################
    
    def create_editor(self, window, obj, kind):
        """ Create an editor for an object. """

        return TraitsUIEditor(window=window, obj=obj)

    def get_editor(self, window, obj, kind):
        """ Get the editor that is currently editing an object. """

        for editor in window.editors:
            if self._is_editing(editor, obj, kind):
                break

        else:
            editor = None

        return editor

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
