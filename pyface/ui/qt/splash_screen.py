# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


from logging import DEBUG

from traits.api import Any, Bool, Int, Tuple, Str, provides

from pyface.qt import QtCore, QtGui
from pyface.i_splash_screen import ISplashScreen, MSplashScreen
from pyface.ui_traits import Image
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
        splash_screen = QtGui.QSplashScreen(self.image.create_image())
        self._qt4_show_message(splash_screen)

        return splash_screen

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _text_changed(self):
        """ Called when the splash screen text has been changed. """

        if self.control is not None:
            self._qt4_show_message(self.control)

    def _qt4_show_message(self, control):
        """ Set the message text for a splash screen control. """

        if self.text_font is not None:
            control.setFont(self.text_font)

        if self.text_color is None:
            text_color = QtCore.Qt.GlobalColor.black
        else:
            # Until we get the type of this trait finalised (ie. when TraitsUI
            # supports PyQt) convert it explcitly to a colour.
            text_color = QtGui.QColor(self.text_color)

        control.showMessage(self.text, QtCore.Qt.AlignmentFlag.AlignLeft, text_color)
