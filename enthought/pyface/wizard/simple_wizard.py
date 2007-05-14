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
""" A simple wizard model that has a static list of pages. """


# Enthought library imports.
from enthought.traits.api import Delegate, Instance, List, Property

# Local imports.
from simple_wizard_controller import SimpleWizardController
from wizard import Wizard
from wizard_page import WizardPage


class SimpleWizard(Wizard):
    """ A wizard model that has a static list of pages. """

    #### 'Wizard' interface ###################################################

    # The wizard controller provides the pages displayed in the wizard, and
    # determines when the wizard is complete etc.
    controller = Instance(SimpleWizardController, ())

    #### 'SimpleWizard' interface #############################################

    # The pages in the wizard.
    #
    # fixme: I'm not sure why, but if I try to use a delegate we get a pwang!
    pages = Property(List(WizardPage)) # Delegate('controller', modify=True)

    ###########################################################################
    # 'SimpleWizard' interface.
    ###########################################################################

    def _get_pages(self):
        """ Returns the pages in the wizard. """

        return self.controller.pages

    def _set_pages(self, pages):
        """ Sets the pages in the wizard. """

        self.controller.pages = pages

        return

#### EOF ######################################################################
