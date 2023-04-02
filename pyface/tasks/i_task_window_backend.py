# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import (
    Any,
    DelegatesTo,
    HasTraits,
    Instance,
    Interface,
    provides,
)


class ITaskWindowBackend(Interface):
    """ The TaskWindow layout interface.

    TaskWindow delegates to an ITaskWindowBackend object for toolkit-specific
    layout functionality.
    """

    #: The root control of the TaskWindow to which the layout belongs.
    control = Any()

    #: The TaskWindow to which the layout belongs.
    window = Instance("pyface.tasks.task_window.TaskWindow")

    # ------------------------------------------------------------------------
    # 'ITaskWindowBackend' interface.
    # ------------------------------------------------------------------------

    def create_contents(self, parent):
        """ Create and return the TaskWindow's contents. (See IWindow.)
        """

    def destroy(self):
        """ Destroy the backend.

        Note that TaskWindow will destroy the widget created in create_contents,
        but this method may be used to perform additional cleanup.
        """

    def hide_task(self, state):
        """ Assuming the specified TaskState is active, hide its controls.
        """

    def show_task(self, state):
        """ Assuming no task is currently active, show the controls of the
            specified TaskState.
        """

    # Methods for saving and restoring the layout -------------------------#

    def get_layout(self):
        """ Returns a TaskLayout for the current state of the window.
        """

    def set_layout(self, layout):
        """ Applies a TaskLayout (which should be suitable for the active task)
            to the window.
        """


@provides(ITaskWindowBackend)
class MTaskWindowBackend(HasTraits):
    """ Mixin containing common coe for toolkit-specific implementations.
    """

    # 'ITaskWindowBackend' interface ---------------------------------------

    control = DelegatesTo("window")
    window = Instance("pyface.tasks.task_window.TaskWindow")

    # ------------------------------------------------------------------------
    # 'ITaskWindowBackend' interface.
    # ------------------------------------------------------------------------

    def create_contents(self, parent):
        raise NotImplementedError()

    def destroy(self):
        pass

    def hide_task(self, state):
        raise NotImplementedError()

    def show_task(self, state):
        raise NotImplementedError()

    def get_layout(self):
        raise NotImplementedError()

    def set_layout(self, layout):
        raise NotImplementedError()
