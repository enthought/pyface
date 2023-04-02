# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface for all pyface wizards. """


from traits.api import Bool, HasTraits, Instance, List, Str
from pyface.i_dialog import IDialog


from .i_wizard_controller import IWizardController
from .i_wizard_page import IWizardPage


class IWizard(IDialog):
    """ The interface for all pyface wizards. """

    # 'IWizard' interface -------------------------------------------------#

    # The pages in the wizard.
    pages = List(IWizardPage)

    # The wizard controller provides the pages displayed in the wizard, and
    # determines when the wizard is complete etc.
    controller = Instance(IWizardController)

    # Should the 'Cancel' button be displayed?
    show_cancel = Bool(True)

    # 'IWindow' interface -------------------------------------------------#

    # The dialog title.
    title = Str("Wizard")

    # ------------------------------------------------------------------------
    # 'IWizard' interface.
    # ------------------------------------------------------------------------

    def next(self):
        """ Advance to the next page in the wizard. """

    def previous(self):
        """ Return to the previous page in the wizard. """


class MWizard(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IWizard interface.

    Implements: next(), previous()
    Reimplements: _create_contents()

    """

    # ------------------------------------------------------------------------
    # 'IWizard' interface.
    # ------------------------------------------------------------------------

    def next(self):
        """ Advance to the next page in the wizard. """

        page = self.controller.get_next_page(self.controller.current_page)
        self._show_page(page)

    def previous(self):
        """ Return to the previous page in the wizard. """

        page = self.controller.get_previous_page(self.controller.current_page)
        self._show_page(page)

        return

    # ------------------------------------------------------------------------
    # Protected 'IWindow' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        """ Creates the window contents. """

        # This creates the dialog and button areas.
        super()._create_contents(parent)

        # Wire up the controller.
        self._initialize_controller(self.controller)

        # Show the first page.
        self._show_page(self.controller.get_first_page())

        return

    # ------------------------------------------------------------------------
    # Protected MWizard interface.
    # ------------------------------------------------------------------------

    def _show_page(self, page):
        """ Show the specified page. """

        # Set the current page in the controller.
        #
        # fixme: Shouldn't this interface be reversed?  Maybe calling
        # 'next_page' on the controller should cause it to set its own current
        # page?
        self.controller.current_page = page

    def _update(self, event):
        """ Enables/disables buttons depending on the state of the wizard. """

        pass

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _initialize_controller(self, controller):
        """ Initializes the wizard controller. """

        controller.observe(self._update, "complete")

        controller.observe(self._on_current_page_changed, "current_page")

        return

    # Trait event handlers -------------------------------------------------

    def _on_current_page_changed(self, event):
        """ Called when the current page is changed. """

        if event.old is not None:
            event.old.observe(self._update, "complete", remove=True)

        if event.new is not None:
            event.new.observe(self._update, "complete")

        self._update(event=None)

    def _on_closed_changed(self):
        """ Called when the wizard is closed. """

        self.controller.dispose_pages()

        return
