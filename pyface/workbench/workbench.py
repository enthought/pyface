# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A workbench. """


import pickle
import logging
import os


from traits.etsconfig.api import ETSConfig
from pyface.api import NO
from traits.api import Bool, Callable, Event, HasTraits, provides
from traits.api import Instance, List, Str, Vetoable
from traits.api import VetoableEvent


from .i_editor_manager import IEditorManager
from .i_workbench import IWorkbench
from .user_perspective_manager import UserPerspectiveManager
from .workbench_window import WorkbenchWindow
from .window_event import WindowEvent, VetoableWindowEvent


# Logging.
logger = logging.getLogger(__name__)


@provides(IWorkbench)
class Workbench(HasTraits):
    """ A workbench.

    There is exactly *one* workbench per application. The workbench can create
    any number of workbench windows.

    """

    # 'IWorkbench' interface -----------------------------------------------

    # The active workbench window (the last one to get focus).
    active_window = Instance(WorkbenchWindow)

    # The editor manager is used to create/restore editors.
    editor_manager = Instance(IEditorManager)

    # The optional application scripting manager.
    script_manager = Instance("apptools.appscripting.api.IScriptManager")

    # A directory on the local file system that we can read and write to at
    # will. This is used to persist window layout information, etc.
    state_location = Str()

    # The optional undo manager.
    undo_manager = Instance("pyface.undo.api.IUndoManager")

    # The user-defined perspectives manager.
    user_perspective_manager = Instance(UserPerspectiveManager)

    # All of the workbench windows created by the workbench.
    windows = List(WorkbenchWindow)

    # Workbench lifecycle events -------------------------------------------

    # Fired when the workbench is about to exit.
    #
    # This can be caused by either:-
    #
    # a) The 'exit' method being called.
    # b) The last open window being closed.
    #
    exiting = VetoableEvent()

    # Fired when the workbench has exited.
    exited = Event()

    # Window lifecycle events ---------------------------------------------#

    # Fired when a workbench window has been created.
    window_created = Event(WindowEvent)

    # Fired when a workbench window is opening.
    window_opening = Event(VetoableWindowEvent)

    # Fired when a workbench window has been opened.
    window_opened = Event(WindowEvent)

    # Fired when a workbench window is closing.
    window_closing = Event(VetoableWindowEvent)

    # Fired when a workbench window has been closed.
    window_closed = Event(WindowEvent)

    # 'Workbench' interface ------------------------------------------------

    # The factory that is used to create workbench windows. This is used in
    # the default implementation of 'create_window'. If you override that
    # method then you obviously don't need to set this trait!
    window_factory = Callable

    # Private interface ----------------------------------------------------

    # An 'explicit' exit is when the the 'exit' method is called.
    # An 'implicit' exit is when the user closes the last open window.
    _explicit_exit = Bool(False)

    # ------------------------------------------------------------------------
    # 'IWorkbench' interface.
    # ------------------------------------------------------------------------

    def create_window(self, **kw):
        """ Factory method that creates a new workbench window. """

        window = self.window_factory(workbench=self, **kw)

        # Add on any user-defined perspectives.
        window.perspectives.extend(self.user_perspective_manager.perspectives)

        # Restore the saved window memento (if there is one).
        self._restore_window_layout(window)

        # Listen for the window being activated/opened/closed etc. Activated in
        # this context means 'gets the focus'.
        #
        # NOTE: 'activated' is not fired on a window when the window first
        # opens and gets focus. It is only fired when the window comes from
        # lower in the stack to be the active window.
        window.observe(self._on_window_activated, "activated")
        window.observe(self._on_window_opening, "opening")
        window.observe(self._on_window_opened, "opened")
        window.observe(self._on_window_closing, "closing")
        window.observe(self._on_window_closed, "closed")

        # Event notification.
        self.window_created = WindowEvent(window=window)

        return window

    def exit(self):
        """ Exits the workbench.

        This closes all open workbench windows.

        This method is not called when the user clicks the close icon. Nor when
        they do an Alt+F4 in Windows. It is only called when the application
        menu File->Exit item is selected.

        Returns True if the exit succeeded, False if it was vetoed.

        """

        logger.debug("**** exiting the workbench ****")

        # Event notification.
        self.exiting = event = Vetoable()
        if not event.veto:
            # This flag is checked in '_on_window_closing' to see what kind of
            # exit is being performed.
            self._explicit_exit = True

            if len(self.windows) > 0:
                exited = self._close_all_windows()

            # The degenerate case where no workbench windows have ever been
            # created!
            else:
                # Trait notification.
                self.exited = self

                exited = True

            # Whether the exit succeeded or not, we are no longer in the
            # process of exiting!
            self._explicit_exit = False

        else:
            exited = False

        if not exited:
            logger.debug("**** exit of the workbench vetoed ****")

        return exited

    # Convenience methods on the active window -----------------------------

    def edit(self, obj, kind=None, use_existing=True):
        """ Edit an object in the active workbench window. """

        return self.active_window.edit(obj, kind, use_existing)

    def get_editor(self, obj, kind=None):
        """ Return the editor that is editing an object.

        Returns None if no such editor exists.

        """

        if self.active_window is None:
            return None

        return self.active_window.get_editor(obj, kind)

    def get_editor_by_id(self, id):
        """ Return the editor with the specified Id.

        Returns None if no such editor exists.

        """

        return self.active_window.get_editor_by_id(id)

    # Message dialogs ----

    def confirm(self, message, title=None, cancel=False, default=NO):
        """ Convenience method to show a confirmation dialog. """

        return self.active_window.confirm(message, title, cancel, default)

    def information(self, message, title="Information"):
        """ Convenience method to show an information message dialog. """

        return self.active_window.information(message, title)

    def warning(self, message, title="Warning"):
        """ Convenience method to show a warning message dialog. """

        return self.active_window.warning(message, title)

    def error(self, message, title="Error"):
        """ Convenience method to show an error message dialog. """

        return self.active_window.error(message, title)

    # ------------------------------------------------------------------------
    # 'Workbench' interface.
    # ------------------------------------------------------------------------

    # Initializers ---------------------------------------------------------

    def _state_location_default(self):
        """ Trait initializer. """

        # It would be preferable to base this on GUI.state_location.
        state_location = os.path.join(
            ETSConfig.application_home,
            "pyface",
            "workbench",
            ETSConfig.toolkit,
        )

        if not os.path.exists(state_location):
            os.makedirs(state_location)

        logger.debug("workbench state location is %s", state_location)

        return state_location

    def _undo_manager_default(self):
        """ Trait initializer. """

        # We make sure the undo package is entirely optional.
        try:
            from pyface.undo.api import UndoManager
        except ImportError:
            return None

        return UndoManager()

    def _user_perspective_manager_default(self):
        """ Trait initializer. """

        return UserPerspectiveManager(state_location=self.state_location)

    # ------------------------------------------------------------------------
    # Protected 'Workbench' interface.
    # ------------------------------------------------------------------------

    def _create_window(self, **kw):
        """ Factory method that creates a new workbench window. """

        raise NotImplementedError()

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _close_all_windows(self):
        """ Closes all open windows.

        Returns True if all windows were closed, False if the user changed
        their mind ;^)

        """

        # We take a copy of the windows list because as windows are closed
        # they are removed from it!
        windows = self.windows[:]
        windows.reverse()

        for window in windows:
            # We give the user chance to cancel the exit as each window is
            # closed.
            if not window.close():
                all_closed = False
                break

        else:
            all_closed = True

        return all_closed

    def _restore_window_layout(self, window):
        """ Restore the window layout. """

        filename = os.path.join(self.state_location, "window_memento")
        if os.path.exists(filename):
            try:
                # If the memento class itself has been modified then there
                # is a chance that the unpickle will fail. If so then we just
                # carry on as if there was no memento!
                f = open(filename, "rb")
                memento = pickle.load(f)
                f.close()

                # The memento doesn't actually get used until the window is
                # opened, so there is nothing to go wrong in this step!
                window.set_memento(memento)

            # If *anything* goes wrong then simply log the error and carry on
            # with no memento!
            except:
                logger.exception("restoring window layout from %s", filename)

    def _save_window_layout(self, window):
        """ Save the window layout. """

        # Save the window layout.
        f = open(os.path.join(self.state_location, "window_memento"), "wb")
        pickle.dump(window.get_memento(), f)
        f.close()

        return

    # Trait change handlers ------------------------------------------------

    def _on_window_activated(self, event):
        """ Dynamic trait change handler. """
        window = event.object
        logger.debug("window %s activated", window)

        self.active_window = window

    def _on_window_opening(self, event):
        """ Dynamic trait change handler. """
        window = event.object
        # Event notification.
        self.window_opening = window_event = VetoableWindowEvent(window=window)
        if window_event.veto:
            event.new.veto = True

    def _on_window_opened(self, event):
        """ Dynamic trait change handler. """
        window = event.object
        # We maintain a list of all open windows so that (amongst other things)
        # we can detect when the user is attempting to close the last one.
        self.windows.append(window)

        # This is necessary because the activated event is not fired when a
        # window is first opened and gets focus. It is only fired when the
        # window comes from lower in the stack to be the active window.
        self.active_window = window

        # Event notification.
        self.window_opened = WindowEvent(window=window)

    def _on_window_closing(self, event):
        """ Dynamic trait change handler. """
        window = event.object
        # Event notification.
        self.window_closing = window_event = VetoableWindowEvent(window=window)

        if window_event.veto:
            event.new.veto = True

        else:
            # Is this the last open window?
            if len(self.windows) == 1:
                # If this is an 'implicit exit' then make sure that we fire the
                # appropriate workbench lifecycle events.
                if not self._explicit_exit:
                    # Event notification.
                    self.exiting = window_event = Vetoable()
                    if window_event.veto:
                        event.new.veto = True

                if not event.new.veto:
                    # Save the window size, position and layout.
                    self._save_window_layout(window)

    def _on_window_closed(self, event):
        """ Dynamic trait change handler. """
        window = event.object
        self.windows.remove(window)

        # Event notification.
        self.window_closed = WindowEvent(window=window)

        # Was this the last window?
        if len(self.windows) == 0:
            # Event notification.
            self.exited = self

        return
