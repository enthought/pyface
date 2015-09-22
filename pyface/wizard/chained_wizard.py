#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" A wizard model that can be chained with other wizards. """


# Enthought library imports.
from traits.api import Instance

# Local imports.
from .i_wizard import IWizard
from .wizard import Wizard


class ChainedWizard(Wizard):
    """ A wizard model that can be chained with other wizards. """

    #### 'ChainedWizard' interface ############################################

    # The wizard following this wizard in the chain.
    next_wizard = Instance(IWizard)

    ###########################################################################
    # 'ChainedWizard' interface.
    ###########################################################################

    #### Trait handlers. ######################################################

    def _controller_default(self):
        """ Provide a default controller. """

        from chained_wizard_controller import ChainedWizardController

        return ChainedWizardController()

    #### Trait event handlers. ################################################

    #### Static ####

    def _next_wizard_changed(self, old, new):
        """ Handle the next wizard being changed. """

        if new is not None:
            self.controller.next_controller = new.controller

        if self.control is not None:
            # FIXME: Do we need to call _create_buttons? Buttons would have
            # added when the main dialog area was created (for the first
            # wizard), and calling update should update the state of these
            # buttons. Do we need to check if buttons are already present in
            # the dialog area? What is use case for calling _create_buttons?
            # self._create_buttons(self.control)
            self._update()

        return

    def _controller_changed(self, old, new):
        """ handle the controller being changed. """

        if new is not None and self.next_wizard is not None:
            self.controller.next_controller = self.next_wizard.controller

        if self.control is not None:
            self._update()

        return

#### EOF ######################################################################
