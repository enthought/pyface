""" The default implementation of the editor interface. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Any, Bool, HasTraits, Instance, List, Property
from enthought.traits.api import Str, implements

# Private Enthought library imports.
from enthought.pyface.toolkit import patch_toolkit

# Local imports.
from i_editor import IEditor


# Logging.
logger = logging.getLogger(__name__)


class Editor(HasTraits):
    """ The default implementation of the editor interface. """

    __tko__ = 'Editor'

    implements(IEditor)

    #### 'IEditor' interface ##################################################

    # The toolkit-specific control that represents the editor.
    #
    # The framework sets this to the value returned by 'create_control'.
    control = Any

    # Does the editor currently have the focus?
    has_focus = Bool(False)

    # Is the resource that the editor is editing 'dirty' i.e., has it been
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
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *args, **traits):
        """ Initialise the instance. """

        super(Editor, self).__init__(*args, **traits)

        patch_toolkit(self)

        return

    ###########################################################################
    # 'Editor' interface.
    ###########################################################################
    
    def close(self):
        """ Close the editor. """

        if self.control is not None:
            logger.debug('closing editor [%s]', self)
            self.window.close_editor(self)

        else:
            logger.error('editor [%s] is not open', self)

        return

    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the editor. """

        return self._tk_editor_create(parent)

    def destroy_control(self):
        """ Destroy the toolkit-specific control that represents the editor.

        """

        if self.control is not None:
            logger.debug('destroying control for editor [%s]', self)
            self._tk_editor_destroy()

        else:
            logger.debug('no control to destroy for editor [%s]', self)

        return

    def set_focus(self):
        """ Sets the focus to the appropriate control in the editor.

        By default we set the focus to be the editor's top-level control.
        Override this method if you need to give focus to some other child
        control.

        """

        if self.control is not None:
            self._tk_editor_set_focus()

        return

    ###########################################################################
    # 'Editor' toolkit interface.
    ###########################################################################

    def _tk_editor_create(self, parent):
        """ Create a default control.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_editor_destroy(self):
        """ Destroy the control.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_editor_set_focus(self):
        """ Set the focus to the control.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
