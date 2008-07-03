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
""" A wizard controller that has a static list of pages. """


# Enthought library imports.
from enthought.traits.api import List, Property

# Local imports.
from wizard_controller import WizardController
from wizard_page import WizardPage


class SimpleWizardController(WizardController):
    """ A wizard controller that has a static list of pages. """

    #### 'SimpleWizardController' interface ###################################

    # The pages in the wizard.
    pages = Property(List(WizardPage))

    #### Private interface ####################################################

    # Shadow trait for the 'pages' property.
    _pages = List(WizardPage)
    
    ###########################################################################
    # 'WizardController' interface.
    ###########################################################################

    def get_first_page(self):
        """ Returns the first page. """

        return self._pages[0]

    def get_next_page(self, page):
        """ Returns the next page. """

        index = self._pages.index(page) + 1

        if index < len(self._pages):
            return self._pages[index]

        return None

    def get_previous_page(self, page):
        """ Returns the previous page. """

        index = self._pages.index(page) - 1

        if index >= 0:
            return self._pages[index]

        return None

    def is_first_page(self, page):
        """ Is the page the first page? """

        return page is self._pages[0]

    def is_last_page(self, page):
        """ Is the page the last page? """

        return page is self._pages[-1]

    def dispose_pages(self):
        """ Dispose the wizard pages. """

        for page in self._pages:
            page.dispose_page()

        return
    
    ###########################################################################
    # 'SimpleWizardController' interface.
    ###########################################################################

    def _get_pages(self):
        """ Returns the pages in the wizard. """

        return self._pages[:]

    def _set_pages(self, pages):
        """ Sets the pages in the wizard. """

        self._pages = pages

        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _update(self):
        """ Checks the completion status of the controller. """
        
        # The entire wizard is complete when ALL pages are complete.
        for page in self._pages:
            if not page.complete:
                self.complete = False
                break
            
        else:
            self.complete = True

        return
    
    #### Trait event handlers #################################################

    #### Static ####

    def _current_page_changed(self, old, new):
        """ Called when the current page is changed. """

        if old is not None:
            old.on_trait_change(self._on_page_complete, 'complete',remove=True)

        if new is not None:
            new.on_trait_change(self._on_page_complete, 'complete')

        self._update()
        
        return

    #### Dynamic ####
    
    def _on_page_complete(self, obj, trait_name, old, new):
        """ Called when the current page is complete. """

        self._update()
        
        return
    
#### EOF ######################################################################
