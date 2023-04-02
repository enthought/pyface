# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A wizard controller that can be chained with others. """


from traits.api import Instance, observe


from .i_wizard_controller import IWizardController
from .wizard_controller import WizardController


class ChainedWizardController(WizardController):
    """ A wizard controller that can be chained with others. """

    # 'ChainedWizardController' interface ---------------------------------#

    # The next chained wizard controller.
    next_controller = Instance(IWizardController)

    # ------------------------------------------------------------------------
    # 'IWizardController' interface.
    # ------------------------------------------------------------------------

    def get_next_page(self, page):
        """ Returns the next page. """

        next_page = None

        if page in self._pages:
            if page is not self._pages[-1]:
                index = self._pages.index(page)
                next_page = self._pages[index + 1]

            else:
                if self.next_controller is not None:
                    next_page = self.next_controller.get_first_page()

        else:
            if self.next_controller is not None:
                next_page = self.next_controller.get_next_page(page)

        return next_page

    def get_previous_page(self, page):
        """ Returns the previous page. """

        if page in self._pages:
            index = self._pages.index(page)
            previous_page = self._pages[index - 1]

        else:
            if self.next_controller is not None:
                if self.next_controller.is_first_page(page):
                    previous_page = self._pages[-1]

                else:
                    previous_page = self.next_controller.get_previous_page(
                        page
                    )

            else:
                previous_page = None

        return previous_page

    def is_first_page(self, page):
        """ Is the page the first page? """

        return page is self._pages[0]

    def is_last_page(self, page):
        """ Is the page the last page? """

        if page in self._pages:
            # If page is not this controller's last page, then it cannot be
            # *the* last page.
            if page is not self._pages[-1]:
                is_last = False

            # Otherwise, it is *the* last page if this controller has no next
            # controller or the next controller has no pages.
            else:
                if self.next_controller is None:
                    is_last = True

                else:
                    is_last = self.next_controller.is_last_page(page)

        else:
            if self.next_controller is not None:
                is_last = self.next_controller.is_last_page(page)

            elif len(self._pages) > 0:
                is_last = False

            else:
                is_last = True

        return is_last

    def dispose_pages(self):
        """ Dispose the wizard's pages. """

        for page in self._pages:
            page.dispose_page()

        if self.next_controller is not None:
            self.next_controller.dispose_pages()

        return

    # ------------------------------------------------------------------------
    # 'ChainedWizardController' interface.
    # ------------------------------------------------------------------------

    def _get_pages(self):
        """ Returns the pages in the wizard. """

        pages = self._pages[:]

        if self.next_controller is not None:
            pages.extend(self.next_controller.pages)

        return pages

    def _set_pages(self, pages):
        """ Sets the pages in the wizard. """

        self._pages = pages

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _update(self):
        """ Checks the completion status of the controller. """

        # The entire wizard is complete when ALL pages are complete.
        for page in self._pages:
            if not page.complete:
                self.complete = False
                break

        else:
            if self.next_controller is not None:
                # fixme: This is a abstraction leak point, since _update is not
                # part of the wizard_controller interface!
                self.next_controller._update()
                self.complete = self.next_controller.complete

            else:
                self.complete = True

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

        if self.next_controller is not None:
            self.next_controller.current_page = new

        self._update()

    @observe("next_controller")
    def _reset_observers_on_next_controller_and_update(self, event):
        """ Called when the next controller is changed. """
        old, new = event.old, event.new
        if old is not None:
            old.observe(
                self._on_controller_complete, "complete", remove=True
            )

        if new is not None:
            new.observe(self._on_controller_complete, "complete")

        self._update()

        return

    # Dynamic ----

    def _on_controller_complete(self, event):
        """ Called when the next controller's complete state changes. """

        self._update()

    def _on_page_complete(self, event):
        """ Called when the current page is complete. """

        self._update()

        return
