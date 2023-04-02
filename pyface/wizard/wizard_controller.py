# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A wizard controller that has a static list of pages. """


from traits.api import (
    Bool, HasTraits, Instance, List, Property, provides, observe
)


from .i_wizard_controller import IWizardController
from .i_wizard_page import IWizardPage


@provides(IWizardController)
class WizardController(HasTraits):
    """ A wizard controller that has a static list of pages. """

    # 'IWizardController' interface ----------------------------------------

    # The pages under the control of this controller.
    pages = Property(List(IWizardPage))

    # The current page.
    current_page = Instance(IWizardPage)

    # Set if the wizard is complete.
    complete = Bool(False)

    # Protected 'IWizardController' interface -----------------------------#

    # Shadow trait for the 'pages' property.
    _pages = List(IWizardPage)

    # ------------------------------------------------------------------------
    # 'IWizardController' interface.
    # ------------------------------------------------------------------------

    def get_first_page(self):
        """ Returns the first page. """

        if self._pages:
            return self._pages[0]

        return None

    def get_next_page(self, page):
        """ Returns the next page. """

        if page.last_page:
            pass

        elif page.next_id:
            for p in self._pages:
                if p.id == page.next_id:
                    return p

        else:
            index = self._pages.index(page) + 1

            if index < len(self._pages):
                return self._pages[index]

        return None

    def get_previous_page(self, page):
        """ Returns the previous page. """

        for p in self._pages:
            next = self.get_next_page(p)

            if next is page:
                return p

        return None

    def is_first_page(self, page):
        """ Is the page the first page? """

        return page is self._pages[0]

    def is_last_page(self, page):
        """ Is the page the last page? """

        if page.last_page:
            return True

        if page.next_id:
            return False

        return page is self._pages[-1]

    def dispose_pages(self):
        """ Dispose the wizard pages. """

        for page in self._pages:
            page.dispose_page()

        return

    # ------------------------------------------------------------------------
    # 'WizardController' interface.
    # ------------------------------------------------------------------------

    def _get_pages(self):
        """ Returns the pages in the wizard. """

        return self._pages[:]

    def _set_pages(self, pages):
        """ Sets the pages in the wizard. """

        self._pages = pages

        # Make sure the current page is valid.
        # If the current page is None (i.e., the current page has
        # not been set yet), do not set it here. The current page will
        # get set when the wizard calls _show_page.
        if (
            self.current_page is not None
            and self.current_page not in self._pages
        ):
            self.current_page = self._pages[0]
        else:
            self._update()

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _update(self):
        """ Checks the completion status of the controller. """

        # The entire wizard is complete when the last page is complete.
        if self.current_page is None:
            self.complete = False
        elif self.is_last_page(self.current_page):
            self.complete = self.current_page.complete
        else:
            self.complete = False

        return

    # Trait event handlers -------------------------------------------------

    # Static ----

    @observe("current_page")
    def _reset_observers_on_current_page_and_update(self, event):
        """ Called when the current page is changed. """
        old, new = event.old, event.new
        if old is not None:
            old.observe(
                self._on_page_complete, "complete", remove=True
            )

        if new is not None:
            new.observe(self._on_page_complete, "complete")

        self._update()

        return

    # Dynamic ----

    def _on_page_complete(self, event):
        """ Called when the current page is complete. """

        self._update()

        return
