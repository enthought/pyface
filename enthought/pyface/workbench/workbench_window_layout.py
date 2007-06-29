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
""" The default workbench window layout. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.pyface.api import error
from enthought.traits.api import Delegate, Event, HasTraits, Instance
from enthought.traits.api import implements

# Local imports.
from enthought.pyface.toolkit import patch_toolkit
from editor import Editor
from i_workbench_window_layout import IWorkbenchWindowLayout


# Logging.
logger = logging.getLogger(__name__)


class WorkbenchWindowLayout(HasTraits):
    """ The default workbench window layout.

    The window layout is responsible for creating and managing the internal
    structure of a workbench window (it knows how to add and remove views and
    editors etc).
    """

    __tko__ = 'WorkbenchWindowLayout'

    implements(IWorkbenchWindowLayout)

    #### 'WindowLayout' interface #############################################

    # The Id of the editor area.
    editor_area_id = Delegate('window')

    # The workbench window that this is the layout for.
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    #### Events ####

    # Fired when an editor is about to be opened (or restored).
    editor_opening = Event(Editor)

    # Fired when an editor has been opened (or restored).
    editor_opened = Event(Editor)

    # Fired when an editor is about to be closed.
    editor_closing = Event(Editor)

    # Fired when an editor has been closed.
    editor_closed = Event(Editor)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *args, **traits):
        """ Initialise the instance. """

        HasTraits.__init__(self, *args, **traits)

        patch_toolkit(self)

        return
    
    ###########################################################################
    # 'WorkbenchWindowLayout' interface.
    ###########################################################################

    def activate_editor(self, editor):
        """ Activates an editor. """

        self._tk_workbenchwindowlayout_activate_editor(editor)

        # This sets the focus to the editor control itself.
        editor.set_focus()

        return

    def activate_view(self, view):
        """ Activates a view. """

        self._tk_workbenchwindowlayout_activate_view(view)

        # This sets the focus to the view control itself.
        view.set_focus()

        return

    def add_editor(self, editor, title):
        """ Adds an editor. """

        try:
            self._tk_workbenchwindowlayout_add_editor(editor, title)

        except Exception:
            logger.exception('error creating editor control [%s]', editor.id)

        return

    def add_view(self, view, position, relative_to=None, size=(-1, -1)):
        """ Adds a view. """

        try:
            self._tk_workbenchwindowlayout_add_view(
                view, position, relative_to, size
            )
            view.visible = True

        except Exception:
            logger.exception('error creating view control [%s]', view.id)

            # Even though we caught the exception, it sometimes happens that
            # the view's control has been created as a child of the application
            # window (or maybe even the dock control.)  We should destroy the
            # control to avoid bad UI effects.
            view.destroy_control()

            # Additionally, display an error message to the user.
            error(
                self.window.control, 'Unable to add view [%s]' % view.id,
                'Workbench Plugin Error'
            )

        return

    def close_editor(self, editor):
        """ Closes an editor. """

        self._tk_workbenchwindowlayout_close_editor(editor)

        return

    def close_view(self, view):
        """ Closes a view.

        fixme: Currently views are never 'closed' in the same sense as an
        editor is closed. When we close an editor, we destroy its control.
        When we close a view, we merely hide its control. I'm not sure if this
        is a good idea or not. It came about after discussion with Dave P. and
        he mentioned that some views might find it hard to persist enough state
        that they can be re-created exactly as they were when they are shown
        again.

        """

        self.hide_view(view)

        return

    def close(self):
        """ Closes the entire window layout.

        In this case, the dock windows are explicitly closed. Other cleanup
        operations go here, but at the moment Linux (and other non-Windows
        platforms?) are less forgiving when things like event handlers aren't
        unregistered.
        """

        self._tk_workbenchwindowlayout_close()

        return

    def create_initial_layout(self):
        """ Create and return the initial window layout. """

        return self._tk_workbenchwindowlayout_create()

    def contains_view(self, view):
        """ Returns True if the view exists in the window layout.

        Note that this returns True even if the view is hidden.

        """

        return self._tk_workbenchwindowlayout_contains_view(view)

    def hide_editor_area(self):
        """ Hides the editor area. """

        self._tk_workbenchwindowlayout_set_editor_area_visible(False)

        return

    def hide_view(self, view):
        """ Hides a view. """

        self._tk_workbenchwindowlayout_set_view_visible(view, False)

        view.visible = False

        return

    def refresh(self):
        """ Refreshes the window layout to reflect any changes. """

        self._tk_workbenchwindowlayout_refresh()

        return

    def reset_editors(self):
        """ Activates the first editor in every region. """

        self._tk_workbenchwindowlayout_reset_editors()

        return

    def reset_views(self):
        """ Activates the first view in every region. """

        self._tk_workbenchwindowlayout_reset_views()

        return

    def show_editor_area(self):
        """ Shows the editor area. """

        self._tk_workbenchwindowlayout_set_editor_area_visible(True)

        return

    def show_view(self, view):
        """ Shows a view. """

        self._tk_workbenchwindowlayout_set_view_visible(view, True)

        view.visible = True

        return

    #### Methods for saving and restoring the layout ##########################

    def get_view_memento(self):
        """ Returns the state of the views. """

        return self._tk_workbenchwindowlayout_get_view_memento()

    def set_view_memento(self, memento):
        """ Restores the state of the views. """

        self._tk_workbenchwindowlayout_set_view_memento(memento)

        return

    def get_editor_memento(self):
        """ Returns the state of the editors. """

        return self._tk_workbenchwindowlayout_get_editor_memento()

    def set_editor_memento(self, memento):
        """ Restores the state of the editors. """

        self._tk_workbenchwindowlayout_set_editor_memento(memento)

        return

    ###########################################################################
    # 'WorkbenchWindowLayout' toolkit interface.
    ###########################################################################

    def _tk_workbenchwindowlayout_activate_editor(self, editor):
        """ Activates an editor.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_activate_view(self, view):
        """ Activates a view.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_add_editor(self, editor, title):
        """ Adds an editor.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_add_view(self, view, position, relative_to=None, size=(-1, -1)):
        """ Adds a view.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_close_editor(self, editor):
        """ Closes an editor.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_close(self):
        """ Closes the entire window layout.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_create(self):
        """ Create and return the initial window layout.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_contains_view(self, view):
        """ Returns True if the view exists in the window layout.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_refresh(self):
        """ Refreshes the window layout to reflect any changes.

        This default implementation does nothing.
        """

        pass

    def _tk_workbenchwindowlayout_reset_editors(self):
        """ Activates the first editor in every region.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_reset_views(self):
        """ Activates the first view in every region.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_set_editor_area_visible(self, visible):
        """ Sets the editor area visibility.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_set_view_visible(self, view, visible):
        """ Sets a view's visibility.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_get_view_memento(self):
        """ Returns the state of the views.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_set_view_memento(self, memento):
        """ Restores the state of the views.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_get_editor_memento(self):
        """ Returns the state of the editors.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_workbenchwindowlayout_set_editor_memento(self, memento):
        """ Restores the state of the editors.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
