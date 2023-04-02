# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Any, Bool, HasTraits, Interface, Instance, Str


from pyface.tasks.task import Task


class ITaskPane(Interface):
    """ The base interface for all panes (central and dock) in a Task.
    """

    #: The pane's identifier, unique within a Task.
    id = Str()

    #: The pane's user-visible name.
    name = Str()

    #: The toolkit-specific control that represents the pane.
    control = Any()

    #: Does the pane currently have focus?
    has_focus = Bool()

    #: The task with which the pane is associated. Set by the framework.
    task = Instance(Task)

    # ------------------------------------------------------------------------
    # 'ITaskPane' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """

    def set_focus(self):
        """ Gives focus to the control that represents the pane.
        """


class MTaskPane(HasTraits):
    """ Mixin containing common code for toolkit-specific implementations.
    """

    # 'ITaskPane' interface ------------------------------------------------

    id = Str()
    name = Str()
    control = Any()
    has_focus = Bool(False)
    task = Instance(Task)
