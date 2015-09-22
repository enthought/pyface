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
""" The interface for all pyface wizard controllers. """


# Enthought library imports.
from traits.api import Bool, Interface, Instance, List

# Local imports.
from .i_wizard_page import IWizardPage


class IWizardController(Interface):
    """ The interface for all pyface wizard controllers. """

    #### 'IWizardController' interface ########################################

    # The pages under the control of this controller.
    pages = List(IWizardPage)

    # The current page.
    current_page = Instance(IWizardPage)

    # Set if the wizard complete.
    complete = Bool(False)

    ###########################################################################
    # 'IWizardController' interface.
    ###########################################################################

    def get_first_page(self):
        """ Returns the first page in the model. """

    def get_next_page(self, page):
        """ Returns the next page. """

    def get_previous_page(self, page):
        """ Returns the previous page. """

    def is_first_page(self, page):
        """ Is the page the first page? """

    def is_last_page(self, page):
        """ Is the page the last page? """

    def dispose_pages(self):
        """ Dispose all the pages. """

#### EOF ######################################################################
