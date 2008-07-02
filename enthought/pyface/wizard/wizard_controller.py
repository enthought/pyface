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
""" Abstract base class for all wizard controllers. """


# Enthought library imports.
from enthought.traits.api import Bool, HasTraits, Instance

# Local imports.
from wizard_page import WizardPage


class WizardController(HasTraits):
    """ Abstract base class for all wizard controllers. """

    #### 'WizardController' interface #########################################

    # The current page.
    current_page = Instance(WizardPage)

    # Is the wizard complete (i.e. should the 'Finish' button be enabled)?
    complete = Bool(False)

    ###########################################################################
    # 'WizardModel' interface.
    ###########################################################################

    def get_first_page(self):
        """ Returns the first page in the model. """

        raise NotImplementedError

    def get_next_page(self, page):
        """ Returns the next page. """

        raise NotImplementedError

    def get_previous_page(self, page):
        """ Returns the previous page. """

        raise NotImplementedError

    def is_first_page(self, page):
        """ Is the page the first page? """

        raise NotImplementedError

    def is_last_page(self, page):
        """ Is the page the last page? """

        raise NotImplementedError

    def dispose_pages(self):
        """ Dispose all the pages. """

        raise NotImplementedError
    
#### EOF ######################################################################
