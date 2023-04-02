# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Bool, Enum, HasTraits, Tuple


from pyface.tasks.i_task_pane import ITaskPane


class IDockPane(ITaskPane):
    """ A pane that is useful but unessential for a task.

    Dock panes are arranged around the central pane in dock areas, and can, in
    general, be moved, resized, and hidden by the user.
    """

    #: If enabled, the pane will have a button to close it, and a visibility
    #: toggle button will be added to the View menu. Otherwise, the pane's
    #: visibility will only be adjustable programmatically, though the
    #: 'visible' attribute.
    closable = Bool(True)

    #: The dock area in which the pane is currently present.
    dock_area = Enum("left", "right", "top", "bottom")

    #: Whether the pane can be detached from the main window.
    floatable = Bool(True)

    #: Whether the pane is currently detached from the main window.
    floating = Bool(False)

    #: Whether the pane can be moved from one dock area to another.
    movable = Bool(True)

    #: The size of the dock pane. Note that this value is read-only.
    size = Tuple()

    #: Whether the pane is currently visible.
    visible = Bool(False)

    # ------------------------------------------------------------------------
    # 'IDockPane' interface.
    # ------------------------------------------------------------------------

    def create_contents(self, parent):
        """ Create and return the toolkit-specific contents of the dock pane.
        """

    def hide(self):
        """ Convenience method to hide the dock pane.
        """

    def show(self):
        """ Convenience method to show the dock pane.
        """


class MDockPane(HasTraits):
    """ Mixin containing common code for toolkit-specific implementations.
    """

    # 'IDockPane' interface ------------------------------------------------

    closable = Bool(True)
    dock_area = Enum("left", "right", "top", "bottom")
    floatable = Bool(True)
    floating = Bool(False)
    movable = Bool(True)
    size = Tuple()
    visible = Bool(False)
    caption_visible = Bool(True)
    dock_layer = Bool(0)

    # ------------------------------------------------------------------------
    # 'IDockPane' interface.
    # ------------------------------------------------------------------------

    def hide(self):
        """ Convenience method to hide the dock pane.
        """
        self.visible = False

    def show(self):
        """ Convenience method to show the dock pane.
        """
        self.visible = True
