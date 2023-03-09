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


from pyface.tasks.dock_pane import DockPane


class TraitsDockPane(DockPane):
    """ A DockPane that displays a Traits UI View.
    """

    # TraitsDockPane interface ---------------------------------------------

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

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        # Destroy the Traits-generated control inside the dock control.
        if self.ui is not None:
            self.ui.dispose()
            self.ui = None

        # Destroy the dock control.
        super().destroy()

    # ------------------------------------------------------------------------
    # 'IDockPane' interface.
    # ------------------------------------------------------------------------

    def create_contents(self, parent):
        """ Create and return the toolkit-specific contents of the dock pane.
        """
        self.ui = self.edit_traits(kind="subpanel", parent=parent)
        return self.ui.control
