# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A thin visual divider. """


import wx


class Divider(wx.StaticLine):
    """ A thin visual divider. """

    def __init__(self, parent, id, **kw):
        """ Creates a divider. """

        # Base-class constructor.
        wx.StaticLine.__init__(self, parent, id, style=wx.LI_HORIZONTAL, **kw)

        # Create the widget!
        self._create_widget()

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_widget(self):
        """ Creates the widget. """

        self.SetSize((1, 1))

        return
