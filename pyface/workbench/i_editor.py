# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface of a workbench editor. """

import uuid


from traits.api import (
    Any,
    Bool,
    Event,
    VetoableEvent,
    Vetoable,
    Instance,
)
from traits.api import provides


from .i_workbench_part import IWorkbenchPart, MWorkbenchPart


class IEditor(IWorkbenchPart):
    """ The interface of a workbench editor. """

    # The optional command stack.
    command_stack = Instance("pyface.undo.api.ICommandStack")

    # Is the object that the editor is editing 'dirty' i.e., has it been
    # modified but not saved?
    dirty = Bool(False)

    # The object that the editor is editing.
    #
    # The framework sets this when the editor is created.
    obj = Any()

    # Editor Lifecycle Events ---------------------------------------------#

    # Fired when the editor is closing.
    closing = VetoableEvent()

    # Fired when the editor is closed.
    closed = Event()

    # Methods -------------------------------------------------------------#

    def close(self):
        """ Close the editor.

        This method is not currently called by the framework itself as the user
        is normally in control of the editor lifecycle. Call this if you want
        to control the editor lifecycle programmatically.

        """


@provides(IEditor)
class MEditor(MWorkbenchPart):
    """ Mixin containing common code for toolkit-specific implementations. """

    # 'IEditor' interface -------------------------------------------------#

    # The optional command stack.
    command_stack = Instance("pyface.undo.api.ICommandStack")

    # Is the object that the editor is editing 'dirty' i.e., has it been
    # modified but not saved?
    dirty = Bool(False)

    # The object that the editor is editing.
    #
    # The framework sets this when the editor is created.
    obj = Any()

    # Editor Lifecycle Events ---------------------------------------------#

    # Fired when the editor is opening.
    opening = VetoableEvent()

    # Fired when the editor has been opened.
    open = Event()

    # Fired when the editor is closing.
    closing = Event(VetoableEvent)

    # Fired when the editor is closed.
    closed = Event()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __str__(self):
        """ Return an informal string representation of the object. """

        return "Editor(%s)" % self.id

    # ------------------------------------------------------------------------
    # 'IWorkbenchPart' interface.
    # ------------------------------------------------------------------------

    def _id_default(self):
        """ Trait initializer. """

        # If no Id is specified then use a random uuid
        # this gaurantees (barring *really* unusual cases) that there are no
        # collisions between the ids of editors.
        return uuid.uuid4().hex

    # ------------------------------------------------------------------------
    # 'IEditor' interface.
    # ------------------------------------------------------------------------

    def close(self):
        """ Close the editor. """

        if self.control is not None:
            self.closing = event = Vetoable()
            if not event.veto:
                self.window.close_editor(self)

                self.closed = True

        return

    # Initializers ---------------------------------------------------------

    def _command_stack_default(self):
        """ Trait initializer. """

        # We make sure the undo package is entirely optional.
        try:
            from pyface.undo.api import CommandStack
        except ImportError:
            return None

        return CommandStack(undo_manager=self.window.workbench.undo_manager)
