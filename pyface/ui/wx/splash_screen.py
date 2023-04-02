# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""


from logging import DEBUG


import wx
import wx.adv


from traits.api import Any, Bool, Int, provides
from traits.api import Tuple, Str


from pyface.i_splash_screen import ISplashScreen, MSplashScreen
from pyface.ui_traits import Image
from pyface.wx.util.font_helper import new_font_like
from .image_resource import ImageResource
from .window import Window


@provides(ISplashScreen)
class SplashScreen(MSplashScreen, Window):
    """ The toolkit specific implementation of a SplashScreen.  See the
    ISplashScreen interface for the API documentation.
    """

    # 'ISplashScreen' interface --------------------------------------------

    image = Image(ImageResource("splash"))

    log_level = Int(DEBUG)

    show_log_messages = Bool(True)

    text = Str()

    text_color = Any()

    text_font = Any()

    text_location = Tuple(5, 5)

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        # Get the splash screen image.
        image = self.image.create_image()

        splash_screen = wx.adv.SplashScreen(
            # The bitmap to display on the splash screen.
            image.ConvertToBitmap(),
            # Splash Style.
            wx.adv.SPLASH_NO_TIMEOUT | wx.adv.SPLASH_CENTRE_ON_SCREEN,
            # Timeout in milliseconds (we don't currently timeout!).
            0,
            # The parent of the splash screen.
            parent,
            # wx Id.
            -1,
            # Window style.
            style=wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR,
        )

        # By default we create a font slightly bigger and slightly more italic
        # than the normal system font ;^)  The font is used inside the event
        # handler for 'EVT_PAINT'.
        self._wx_default_text_font = new_font_like(
            wx.NORMAL_FONT,
            point_size=wx.NORMAL_FONT.GetPointSize() + 1,
            style=wx.ITALIC,
        )

        # This allows us to write status text on the splash screen.
        splash_screen.Bind(wx.EVT_PAINT, self._on_paint)

        return splash_screen

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _text_changed(self):
        """ Called when the splash screen text has been changed. """

        # Passing 'False' to 'Refresh' means "do not erase the background".
        if self.control is not None:
            self.control.Refresh(False)
            self.control.Update()
        wx.GetApp().Yield(True)

    def _on_paint(self, event):
        """ Called when the splash window is being repainted. """

        if self.control is not None:
            # Get the window that the splash image is drawn in.
            window = self.control  # .GetSplashWindow()

            dc = wx.PaintDC(window)

            if self.text_font is None:
                text_font = self._wx_default_text_font
            else:
                text_font = self.text_font

            dc.SetFont(text_font)

            if self.text_color is None:
                text_color = "black"
            else:
                text_color = self.text_color

            dc.SetTextForeground(text_color)

            x, y = self.text_location
            dc.DrawText(self.text, x, y)

        # Let the normal wx paint handling do its stuff.
        event.Skip()
