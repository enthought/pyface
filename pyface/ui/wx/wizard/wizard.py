# (C) Copyright 2005-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The base class for all pyface wizards. """


import wx


from traits.api import Bool, Instance, List, Property, provides, Str
from pyface.api import Dialog, LayeredPanel
from pyface.wizard.i_wizard import IWizard, MWizard
from pyface.wizard.i_wizard_controller import IWizardController
from pyface.wizard.i_wizard_page import IWizardPage


@provides(IWizard)
class Wizard(MWizard, Dialog):
    """ The base class for all pyface wizards.

    See the IWizard interface for the API documentation.

    """

    # 'IWizard' interface --------------------------------------------------

    pages = Property(List(IWizardPage))

    controller = Instance(IWizardController)

    show_cancel = Bool(True)

    # 'IWindow' interface --------------------------------------------------

    title = Str("Wizard")

    # private traits -------------------------------------------------------

    _layered_panel = Instance(LayeredPanel)

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_dialog_area(self, parent):
        """ Creates the main content of the dialog. """

        self._layered_panel = panel = LayeredPanel(parent=parent)
        panel.create()
        # fixme: Specific size?
        panel.control.SetSize((100, 200))

        return panel.control

    def _create_buttons(self, parent):
        """ Creates the buttons. """

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 'Back' button.
        self._back = back = wx.Button(parent, -1, "Back")
        parent.Bind(wx.EVT_BUTTON, self._on_back, back)
        sizer.Add(back, 0)

        # 'Next' button.
        self._next = next = wx.Button(parent, -1, "Next")
        parent.Bind(wx.EVT_BUTTON, self._on_next, next)
        sizer.Add(next, 0, wx.LEFT, 5)
        next.SetDefault()

        # 'Finish' button.
        self._finish = finish = wx.Button(parent, wx.ID_OK, "Finish")
        finish.Enable(self.controller.complete)
        parent.Bind(wx.EVT_BUTTON, self._wx_on_ok, finish)
        sizer.Add(finish, 0, wx.LEFT, 5)

        # 'Cancel' button.
        if self.show_cancel:
            self._cancel = cancel = wx.Button(parent, wx.ID_CANCEL, "Cancel")
            parent.Bind(wx.EVT_BUTTON, self._wx_on_cancel, cancel)
            sizer.Add(cancel, 0, wx.LEFT, 10)

        # 'Help' button.
        if len(self.help_id) > 0:
            help = wx.Button(parent, wx.ID_HELP, "Help")
            parent.Bind(wx.EVT_BUTTON, self._wx_on_help, help)
            sizer.Add(help, 0, wx.LEFT, 10)

        return sizer

    # ------------------------------------------------------------------------
    # Protected 'MWizard' interface.
    # ------------------------------------------------------------------------

    def _show_page(self, page):
        """ Show the specified page. """

        panel = self._layered_panel

        # If the page has not yet been shown then create it.
        if not panel.has_layer(page.id):
            panel.add_layer(page.id, page.create_page(panel.control))

        # Show the page.
        layer = panel.show_layer(page.id)
        layer.SetFocus()

        # Set the current page in the controller.
        #
        # fixme: Shouldn't this interface be reversed?  Maybe calling
        # 'next_page' on the controller should cause it to set its own current
        # page?
        self.controller.current_page = page

    def _update(self, event):
        """ Enables/disables buttons depending on the state of the wizard. """

        controller = self.controller
        current_page = controller.current_page

        is_first_page = controller.is_first_page(current_page)
        is_last_page = controller.is_last_page(current_page)

        # 'Next button'.
        if self._next is not None:
            self._next.Enable(current_page.complete and not is_last_page)

        # 'Back' button.
        if self._back is not None:
            self._back.Enable(not is_first_page)

        # 'Finish' button.
        if self._finish is not None:
            self._finish.Enable(controller.complete)

        # If this is the last page then the 'Finish' button is the default
        # button, otherwise the 'Next' button is the default button.
        if is_last_page:
            if self._finish is not None:
                self._finish.SetDefault()

        else:
            if self._next is not None:
                self._next.SetDefault()

    # Trait handlers -------------------------------------------------------

    def _controller_default(self):
        """ Provide a default controller. """

        from pyface.wizard.wizard_controller import WizardController

        return WizardController()

    def _get_pages(self):
        """ Returns the pages in the wizard. """

        return self.controller.pages

    def _set_pages(self, pages):
        """ Sets the pages in the wizard. """

        self.controller.pages = pages

    # wx event handlers ----------------------------------------------------

    def _on_next(self, event):
        """ Called when the 'Next' button is pressed. """

        self.next()

    def _on_back(self, event):
        """ Called when the 'Back' button is pressed. """

        self.previous()
