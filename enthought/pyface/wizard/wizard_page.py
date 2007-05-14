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
""" A page in a wizard. """


# Major package imports.
import wx

# Enthought library imports.
from enthought.pyface.api import HeadingText
from enthought.traits.api import Bool, HasPrivateTraits, Str


class WizardPage(HasPrivateTraits):
    """ A page in a wizard. """

    #### 'WizardPage' interface ###############################################

    # The unique Id of the page within the wizard.
    id = Str
    
    # Is the page complete (i.e. should the 'Next' button be enabled)?
    complete = Bool(False)

    # The page heading.
    heading = Str
    
    ###########################################################################
    # 'WizardPage' interface.
    ###########################################################################

    def create_page(self, parent):
        """ Creates the wizard page. """

        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # The 'pretty' heading ;^)
        if len(self.heading) > 0:
            title = HeadingText(panel, text=self.heading)
            sizer.Add(title.control, 0, wx.EXPAND | wx.BOTTOM, 5)

        # The page content.
        content = self._create_page_content(panel)
        sizer.Add(content, 1, wx.EXPAND)
        
        return panel

    def dispose_page(self):
        """ Disposes the wizard page.

        Subclasses are expected to override this method if they need to
        dispose of the contents of a page.
        """

        pass


    ###########################################################################
    # Protected 'WizardPage' interface.
    ###########################################################################

    def _create_page_content(self, parent):
        """ Creates the actual page content. """

        # Dummy implementation - override! 
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        panel.SetBackgroundColour('yellow')
        
        return panel

#### EOF ######################################################################
