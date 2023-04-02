# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A panel used as a spacer.

It is in a separate class so that you can set the background color in a
single place to give visual feedback on sizer layouts (in particular,
FlexGridSizer layouts).

"""


import wx


class Spacer(wx.Panel):
    """ A panel used as a spacer. """

    def __init__(self, parent, id, **kw):
        """ Creates a spacer. """

        # Base-class constructor.
        wx.Panel.__init__(self, parent, id, **kw)

        # Create the widget!
        self._create_widget()

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_widget(self):
        """ Create the widget! """

        # self.SetBackgroundColour("brown")

        return
