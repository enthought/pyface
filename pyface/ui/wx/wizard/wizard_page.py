# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A page in a wizard. """


import wx


from traits.api import Bool, HasTraits, provides, Str, Tuple
from pyface.api import HeadingText
from pyface.wizard.i_wizard_page import IWizardPage, MWizardPage


@provides(IWizardPage)
class WizardPage(MWizardPage, HasTraits):
    """ The toolkit specific implementation of a WizardPage.

    See the IWizardPage interface for the API documentation.

    """

    # 'IWizardPage' interface ---------------------------------------------#

    id = Str()

    next_id = Str()

    last_page = Bool(False)

    complete = Bool(False)

    heading = Str()

    subheading = Str()

    size = Tuple()

    # ------------------------------------------------------------------------
    # 'IWizardPage' interface.
    # ------------------------------------------------------------------------

    def create_page(self, parent):
        """ Creates the wizard page. """

        # FIXME: implement support for the size trait.

        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # The 'pretty' heading ;^)
        if len(self.heading) > 0:
            title = HeadingText(panel, text=self.heading)
            sizer.Add(title.control, 0, wx.EXPAND | wx.BOTTOM, 5)

        if len(self.subheading) > 0:
            subtitle = wx.StaticText(panel, -1, self.subheading)
            sizer.Add(subtitle, 0, wx.EXPAND | wx.BOTTOM, 5)

        # The page content.
        content = self._create_page_content(panel)
        sizer.Add(content, 1, wx.EXPAND)

        return panel

    # ------------------------------------------------------------------------
    # Protected 'IWizardPage' interface.
    # ------------------------------------------------------------------------

    def _create_page_content(self, parent):
        """ Creates the actual page content. """

        # Dummy implementation - override!
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        panel.SetBackgroundColour("yellow")

        return panel
