# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A panel sized by a sizer. """


import wx


class SizedPanel(wx.Panel):
    """ A panel sized by a sizer. """

    def __init__(self, parent, wxid, sizer, **kw):
        """ Creates a new sized panel. """

        # Base-class constructor.
        wx.Panel.__init__(self, parent, wxid, **kw)

        # Set up the panel's sizer.
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        # A quick reference to our sizer (at least quicker than using
        # 'self.GetSizer()' ;^).
        self.sizer = sizer

        return

    # ------------------------------------------------------------------------
    # 'SizedPanel' interface.
    # ------------------------------------------------------------------------

    def Fit(self):
        """ Resizes the panel to match the sizer's minimal size. """

        self.sizer.Fit(self)

    def Layout(self):
        """ Lays out the sizer without changing the panel geometry. """

        self.sizer.Layout()

        return
