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
from enthought.traits.api import Delegate, Instance, List, Property

# Local imports.
from chained_wizard_controller import ChainedWizardController
from simple_wizard import SimpleWizard
from wizard import Wizard
from wizard_page import WizardPage


class ChainedWizard(SimpleWizard):
    """ A wizard model that can be chained with other wizards. """

    #### 'Wizard' interface ###################################################

    # The wizard controller provides the pages displayed in the wizard, and
    # determines when the wizard is complete etc.
    controller = Instance(ChainedWizardController, ())

    #### 'ChainedWizard' interface ############################################

    # The wizard following this wizard in the chain.
    next_wizard = Instance(Wizard)

    ###########################################################################
    # 'ChainedWizard' interface.
    ###########################################################################

    #### Trait event handlers. ################################################

    #### Static ####

    def _next_wizard_changed(self, old, new):
        """ Handle the next wizard being changed. """

        if new is not None:
            self.controller.next_controller = new.controller

        self._update()

        return

    def _controller_changed(self, old, new):
        """ handle the controller being changed. """

        if new is not None and self.next_wizard is not None:
            self.controller.next_controller = self.next_wizard.controller

        self._update()
        
        return
    
#### EOF ######################################################################
