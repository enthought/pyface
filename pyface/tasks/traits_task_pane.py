# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import HasTraits, Instance


from .task_pane import TaskPane


class TraitsTaskPane(TaskPane):
    """ A TaskPane that displays a Traits UI View.
    """

    # TraitsTaskPane interface ---------------------------------------------

    #: The model object to view. If not specified, the pane is used instead.
    model = Instance(HasTraits)

    #: The UI object associated with the Traits view, if it has been
    #: constructed.
    ui = Instance("traitsui.ui.UI")

    # ------------------------------------------------------------------------
    # 'HasTraits' interface.
    # ------------------------------------------------------------------------

    def trait_context(self):
        """ Use the model object for the Traits UI context, if appropriate.
        """
        if self.model:
            return {"object": self.model, "pane": self}
        return super().trait_context()

    # ------------------------------------------------------------------------
    # 'ITaskPane' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        self.ui = self.edit_traits(kind="subpanel", parent=parent)
        self.control = self.ui.control

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        if self.ui is not None:
            self.ui.dispose()
            self.ui = None
        self.control = self.ui = None
