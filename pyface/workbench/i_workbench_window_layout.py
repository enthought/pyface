#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" The workbench window layout interface. """


# Enthought library imports.
from traits.api import Event, HasTraits, Instance, Interface, Str
from traits.api import provides

# Local imports.
from .i_editor import IEditor
from .i_view import IView


class IWorkbenchWindowLayout(Interface):
    """ The workbench window layout interface.

    Window layouts are responsible for creating and managing the internal
    structure of a workbench window (it knows how to add and remove views and
    editors etc).

    """

    # The Id of the editor area.
    # FIXME v3: This is toolkit specific.
    editor_area_id = Str

    # The workbench window that this is the layout for.
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    #### Events ####

    # Fired when an editor is about to be opened (or restored).
    editor_opening = Event(IEditor)

    # Fired when an editor has been opened (or restored).
    editor_opened = Event(IEditor)

    # Fired when an editor is about to be closed.
    editor_closing = Event(IEditor)

    # Fired when an editor has been closed.
    editor_closed = Event(IEditor)

    # Fired when a view is about to be opened (or restored).
    view_opening = Event(IView)

    # Fired when a view has been opened (or restored).
    view_opened = Event(IView)

    # Fired when a view is about to be closed (*not* hidden!).
    view_closing = Event(IView)

    # Fired when a view has been closed (*not* hidden!).
    view_closed = Event(IView)

    # FIXME v3: The "just for convenience" returns are a really bad idea.
    #
    # Why? They allow the call to be used on the LHS of an expression...
    # Because they have nothing to do with what the call is supposed to be
    # doing, they are unlikely to be used (because they are so unexpected and
    # inconsistently implemented), and only serve to replace two shorter lines
    # of code with one long one, arguably making code more difficult to read.
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

    def add_view(self, view, position=None, relative_to=None, size=(-1, -1)):
        """ Add a view.

        Returns the view (just for convenience).

        """

    def close_editor(self, editor):
        """ Close an editor.

        Returns the editor (just for convenience).

        """

    def close_view(self, view):
        """ Close a view.

        FIXME v3: Currently views are never 'closed' in the same sense as an
        editor is closed. When we close an editor, we destroy its control.
        When we close a view, we merely hide its control. I'm not sure if this
        is a good idea or not. It came about after discussion with Dave P. and
        he mentioned that some views might find it hard to persist enough state
        that they can be re-created exactly as they were when they are shown
        again.

        Returns the view (just for convenience).

        """

    def close(self):
        """ Close the entire window layout.

        FIXME v3: Should this be called 'destroy'?

        """

    def create_initial_layout(self, parent):
        """ Create the initial window layout.

        Returns the layout.

        """

    def contains_view(self, view):
        """ Return True if the view exists in the window layout.

        Note that this returns True even if the view is hidden.

        """

    def hide_editor_area(self):
        """ Hide the editor area.

        """

    def hide_view(self, view):
        """ Hide a view.

        Returns the view (just for convenience).

        """

    def refresh(self):
        """ Refresh the window layout to reflect any changes.

        """

    def reset_editors(self):
        """ Activate the first editor in every group.

        """

    def reset_views(self):
        """ Activate the first view in every region.

        """

    def show_editor_area(self):
        """ Show the editor area.

        """

    def show_view(self, view):
        """ Show a view.

        """

    #### Methods for saving and restoring the layout ##########################

    def get_view_memento(self):
        """ Returns the state of the views.

        """

    def set_view_memento(self, memento):
        """ Restores the state of the views.

        """

    def get_editor_memento(self):
        """ Returns the state of the editors.

        """

    def set_editor_memento(self, memento):
        """ Restores the state of the editors.

        """

    def get_toolkit_memento(self):
        """ Return any toolkit-specific data that should be part of the memento.
        """

    def set_toolkit_memento(self, memento):
        """ Restores any toolkit-specific data.
        """


@provides(IWorkbenchWindowLayout)
class MWorkbenchWindowLayout(HasTraits):
    """ Mixin containing common code for toolkit-specific implementations. """
    #### 'IWorkbenchWindowLayout' interface ###################################

    # The Id of the editor area.
    # FIXME v3: This is toolkit specific.
    editor_area_id = Str

    # The workbench window that this is the layout for.
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    #### Events ####

    # Fired when an editor is about to be opened (or restored).
    editor_opening = Event(IEditor)

    # Fired when an editor has been opened (or restored).
    editor_opened = Event(IEditor)

    # Fired when an editor is about to be closed.
    editor_closing = Event(IEditor)

    # Fired when an editor has been closed.
    editor_closed = Event(IEditor)

    # Fired when a view is about to be opened (or restored).
    view_opening = Event(IView)

    # Fired when a view has been opened (or restored).
    view_opened = Event(IView)

    # Fired when a view is about to be closed (*not* hidden!).
    view_closing = Event(IView)

    # Fired when a view has been closed (*not* hidden!).
    view_closed = Event(IView)

    ###########################################################################
    # 'IWorkbenchWindowLayout' interface.
    ###########################################################################

    def activate_editor(self, editor):
        """ Activate an editor. """

        raise NotImplementedError

    def activate_view(self, view):
        """ Activate a view. """

        raise NotImplementedError

    def add_editor(self, editor, title):
        """ Add an editor. """

        raise NotImplementedError

    def add_view(self, view, position=None, relative_to=None, size=(-1, -1)):
        """ Add a view. """

        raise NotImplementedError

    def close_editor(self, editor):
        """ Close an editor. """

        raise NotImplementedError

    def close_view(self, view):
        """ Close a view. """

        raise NotImplementedError

    def close(self):
        """ Close the entire window layout. """

        raise NotImplementedError

    def create_initial_layout(self, parent):
        """ Create the initial window layout. """

        raise NotImplementedError

    def contains_view(self, view):
        """ Return True if the view exists in the window layout. """

        raise NotImplementedError

    def hide_editor_area(self):
        """ Hide the editor area. """

        raise NotImplementedError

    def hide_view(self, view):
        """ Hide a view. """

        raise NotImplementedError

    def refresh(self):
        """ Refresh the window layout to reflect any changes. """

        raise NotImplementedError

    def reset_editors(self):
        """ Activate the first editor in every group. """

        raise NotImplementedError

    def reset_views(self):
        """ Activate the first view in every region. """

        raise NotImplementedError

    def show_editor_area(self):
        """ Show the editor area. """

        raise NotImplementedError

    def show_view(self, view):
        """ Show a view. """

        raise NotImplementedError

    #### Methods for saving and restoring the layout ##########################

    def get_view_memento(self):
        """ Returns the state of the views. """

        raise NotImplementedError

    def set_view_memento(self, memento):
        """ Restores the state of the views. """

        raise NotImplementedError

    def get_editor_memento(self):
        """ Returns the state of the editors. """

        raise NotImplementedError

    def set_editor_memento(self, memento):
        """ Restores the state of the editors. """

        raise NotImplementedError

    def get_toolkit_memento(self):
        """ Return any toolkit-specific data that should be part of the memento.
        """
        return None

    def set_toolkit_memento(self, memento):
        """ Restores any toolkit-specific data.
        """
        return

    ###########################################################################
    # Protected 'MWorkbenchWindowLayout' interface.
    ###########################################################################

    def _get_editor_references(self):
        """ Returns a reference to every editor. """

        editor_manager = self.window.editor_manager

        editor_references = {}
        for editor in self.window.editors:
            # Create the editor reference.
            #
            # If the editor manager returns 'None' instead of a resource
            # reference then this editor will not appear the next time the
            # workbench starts up. This is useful for things like text files
            # that have an editor but have NEVER been saved.
            editor_reference = editor_manager.get_editor_memento(editor)
            if editor_reference is not None:
                editor_references[editor.id] = editor_reference

        return editor_references

#### EOF ######################################################################
