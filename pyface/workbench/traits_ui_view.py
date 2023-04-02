# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A view whose content is provided by a traits UI. """


import logging


from traits.api import Any, Instance, Str


from .view import View


# Logging.
logger = logging.getLogger(__name__)


class TraitsUIView(View):
    """ A view whose content is provided by a traits UI. """

    # 'TraitsUIView' interface ---------------------------------------------

    # The object that we povide a traits UI of (this defaults to the view
    # iteself ie. 'self').
    obj = Any()

    # The traits UI that represents the view.
    #
    # The framework sets this to the value returned by 'create_ui'.
    ui = Instance("traitsui.ui.UI")

    # The name of the traits UI view used to create the UI (if not specified,
    # the default traits UI view is used).
    view = Str()

    # ------------------------------------------------------------------------
    # 'IWorkbenchPart' interface.
    # ------------------------------------------------------------------------

    # Trait initializers ---------------------------------------------------

    def _name_default(self):
        """ Trait initializer. """

        return str(self.obj)

    # Methods -------------------------------------------------------------#

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the editor.

        'parent' is the toolkit-specific control that is the editor's parent.

        Overridden to call 'create_ui' to get the traits UI.

        """

        self.ui = self.create_ui(parent)

        return self.ui.control

    def destroy_control(self):
        """ Destroys the toolkit-specific control that represents the editor.

        Overridden to call 'dispose' on the traits UI.

        """

        # Give the traits UI a chance to clean itself up.
        if self.ui is not None:
            logger.debug("disposing traits UI for view [%s]", self)
            self.ui.dispose()
            self.ui = None
            # Break reference to the control, so the view is created afresh
            # next time.
            self.control = None

        return

    # ------------------------------------------------------------------------
    # 'TraitsUIView' interface.
    # ------------------------------------------------------------------------

    # Trait initializers ---------------------------------------------------

    def _obj_default(self):
        """ Trait initializer. """

        return self

    # Methods -------------------------------------------------------------#

    def create_ui(self, parent):
        """ Creates the traits UI that represents the editor.

        By default it calls 'edit_traits' on the view's 'model'. If you
        want more control over the creation of the traits UI then override!

        """

        ui = self.obj.edit_traits(
            parent=parent, view=self.view, kind="subpanel"
        )

        return ui
