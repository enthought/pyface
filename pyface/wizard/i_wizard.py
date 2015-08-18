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
""" The interface for all pyface wizards. """


# Enthought library imports.
from traits.api import Bool, Instance, List, Unicode
from pyface.i_dialog import IDialog

# Local imports.
from .i_wizard_controller import IWizardController
from .i_wizard_page import IWizardPage


class IWizard(IDialog):
    """ The interface for all pyface wizards. """

    #### 'IWizard' interface ##################################################

    # The pages in the wizard.
    pages = List(IWizardPage)

    # The wizard controller provides the pages displayed in the wizard, and
    # determines when the wizard is complete etc.
    controller = Instance(IWizardController)

    # Should the 'Cancel' button be displayed?
    show_cancel = Bool(True)

    #### 'IWindow' interface ##################################################

    # The dialog title.
    title = Unicode('Wizard')

    ###########################################################################
    # 'IWizard' interface.
    ###########################################################################

    def next(self):
        """ Advance to the next page in the wizard. """

    def previous(self):
        """ Return to the previous page in the wizard. """


class MWizard(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IWizard interface.

    Implements: next(), previous()
    Reimplements: _create_contents()

    """

    ###########################################################################
    # 'IWizard' interface.
    ###########################################################################

    def next(self):
        """ Advance to the next page in the wizard. """

        page = self.controller.get_next_page(self.controller.current_page)
        self._show_page(page)

        return

    def previous(self):
        """ Return to the previous page in the wizard. """

        page = self.controller.get_previous_page(self.controller.current_page)
        self._show_page(page)

        return

    ###########################################################################
    # Protected 'IWindow' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        # This creates the dialog and button areas.
        super(MWizard, self)._create_contents(parent)

        # Wire up the controller.
        self._initialize_controller(self.controller)

        # Show the first page.
        self._show_page(self.controller.get_first_page())

        return

    ###########################################################################
    # Protected MWizard interface.
    ###########################################################################

    def _show_page(self, page):
        """ Show the specified page. """

        # Set the current page in the controller.
        #
        # fixme: Shouldn't this interface be reversed?  Maybe calling
        # 'next_page' on the controller should cause it to set its own current
        # page?
        self.controller.current_page = page

    def _update(self):
        """ Enables/disables buttons depending on the state of the wizard. """

        pass

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _initialize_controller(self, controller):
        """ Initializes the wizard controller. """

        controller.on_trait_change(self._update, 'complete')

        controller.on_trait_change(
            self._on_current_page_changed, 'current_page'
        )

        return

    #### Trait event handlers #################################################

    def _on_current_page_changed(self, obj, trait_name, old, new):
        """ Called when the current page is changed. """

        if old is not None:
            old.on_trait_change(self._update, 'complete', remove=True)

        if new is not None:
            new.on_trait_change(self._update, 'complete')

        self._update()

        return

    def _on_closed_changed(self):
        """ Called when the wizard is closed. """

        self.controller.dispose_pages()

        return

#### EOF ######################################################################
