# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The workbench interface. """


from traits.api import Event, Instance, Interface, List, Str
from traits.api import VetoableEvent


from .user_perspective_manager import UserPerspectiveManager
from .window_event import WindowEvent, VetoableWindowEvent
from .workbench_window import WorkbenchWindow


class IWorkbench(Interface):
    """ The workbench interface. """

    # 'IWorkbench' interface -----------------------------------------------

    # The active workbench window (the last one to get focus).
    active_window = Instance(WorkbenchWindow)

    # The optional application scripting manager.
    script_manager = Instance("apptools.appscripting.api.IScriptManager")

    # A directory on the local file system that we can read and write to at
    # will. This is used to persist window layout information, etc.
    state_location = Str()

    # The optional undo manager.
    undo_manager = Instance("pyface.undo.api.IUndoManager")

    # The user defined perspectives manager.
    user_perspective_manager = Instance(UserPerspectiveManager)

    # All of the workbench windows created by the workbench.
    windows = List(WorkbenchWindow)

    # Workbench lifecycle events ----

    # Fired when the workbench is about to exit.
    #
    # This can be caused by either:-
    #
    # a) The 'exit' method being called.
    # b) The last open window being closed.
    exiting = VetoableEvent()

    # Fired when the workbench has exited.
    #
    # This is fired after the last open window has been closed.
    exited = Event()

    # Window lifecycle events ----

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

    # ------------------------------------------------------------------------
    # 'IWorkbench' interface.
    # ------------------------------------------------------------------------

    def create_window(self, **kw):
        """ Factory method that creates a new workbench window. """

    def edit(self, obj, kind=None, use_existing=True):
        """ Edit an object in the active workbench window. """

    def exit(self):
        """ Exit the workbench.

        This closes all open workbench windows.

        This method is not called when the user clicks the close icon. Nor when
        they do an Alt+F4 in Windows. It is only called when the application
        menu File->Exit item is selected.

        """

    def get_editor(self, obj, kind=None):
        """ Return the editor that is editing an object.

        Returns None if no such editor exists.

        """

    def get_editor_by_id(self, id):
        """ Return the editor with the specified Id.

        Returns None if no such editor exists.

        """
