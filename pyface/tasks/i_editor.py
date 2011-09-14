# Enthought library imports.
from traits.api import Any, Bool, Event, HasTraits, Interface, \
    Instance, Property, Unicode, Vetoable, VetoableEvent, cached_property


class IEditor(Interface):
    """ The base interface for all panes (central and dock) in a Task.
    """

    # The editor's user-visible name.
    name = Unicode

    # The tooltip to show for the editor's tab, if any.
    tooltip = Unicode

    # The toolkit-specific control that represents the editor.
    control = Any

    # The object that the editor is editing.
    obj = Any

    # Has the editor's object been modified but not saved?
    dirty = Bool

    # The editor area to which the editor belongs.
    editor_area = Instance(
        'pyface.tasks.i_editor_area_pane.IEditorAreaPane')

    # Is the editor active in the editor area?
    is_active = Bool

    # Does the editor currently have the focus?
    has_focus = Bool

    # Fired when the editor has been requested to close.
    closing = VetoableEvent

    # Fired when the editor has been closed.
    closed = Event

    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################

    def close(self):
        """ Close the editor.
        """

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            editor.
        """

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the editor.
        """


class MEditor(HasTraits):
    """ Mixin containing common code for toolkit-specific implementations.
    """

    #### 'IEditor' interface ##################################################

    name = Unicode
    tooltip = Unicode
    control = Any
    obj = Any
    dirty = Bool(False)

    editor_area = Instance(
        'pyface.tasks.i_editor_area_pane.IEditorAreaPane')
    is_active = Property(Bool, depends_on='editor_area.active_editor')
    has_focus = Bool(False)

    closing = VetoableEvent
    closed = Event

    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################

    def close(self):
        """ Close the editor.
        """
        if self.control is not None:
            self.closing = event = Vetoable()
            if not event.veto:
                self.editor_area.remove_editor(self)
                self.closed = True

    ###########################################################################
    # Private interface.
    ###########################################################################

    @cached_property
    def _get_is_active(self):
        if self.editor_area is not None:
            return self.editor_area.active_editor == self
        return False
