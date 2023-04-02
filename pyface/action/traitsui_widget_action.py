# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Constant, HasTraits, Instance

from .action import Action


class TraitsUIWidgetAction(Action):
    """ A widget action containing a TraitsUI.

    If a object is supplied, then the UI is generated from the object's view,
    otherwise the ui is generated on using the Action object.

    Notes
    -----
    This is currently only supported by the Qt backend.
    """

    # TraitsUIWidgetAction traits -------------------------------------------

    #: The underlying traits model to be displayed, or None.
    model = Instance(HasTraits)

    # Action traits ---------------------------------------------------------

    #: This is a widget action.
    style = Constant("widget")

    # ------------------------------------------------------------------------
    # Action interface
    # ------------------------------------------------------------------------

    def create_control(self, parent):
        """ Called when creating a "widget" style action.

        This constructs an TraitsUI subpanel-based control.  It does no binding
        to the `perform` method.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control, usually a toolbar.

        Returns
        -------
        control : toolkit control
            A toolkit control or None.
        """
        ui = self.edit_traits(kind="subpanel", parent=parent)
        control = ui.control
        control._ui = ui
        return control

    # ------------------------------------------------------------------------
    # HasTraits interface
    # ------------------------------------------------------------------------

    def trait_context(self):
        """ Use the model object for the Traits UI context, if appropriate.
        """
        if self.model is not None:
            context = {"object": self.model, "action": self}
            return context
        return super().trait_context()
