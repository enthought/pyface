#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtCore, QtGui


class SplashScreen_qt4(object):
    """ The SplashScreen monkey patch for Qt4. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create and return the toolkit specific control that represents the
        widget.
        """

        splash_screen = QtGui.QSplashScreen(self.image.create_image())
        self._qt4_show_message(splash_screen)

        return splash_screen

    ###########################################################################
    # 'SplashScreen' toolkit interface.
    ###########################################################################

    def _tk_splashscreen_update_text(self):
        """ Update the splash screen text. """

        self._qt4_show_message(self.control)

    def _qt4_show_message(self, control):
        """ Set the message text for a splash screen control. """

        if self.text_font is not None:
            control.setFont(self.text_font)

        if self.text_color is None:
            text_color = QtCore.Qt.black
        else:
            # Until we get the type of this trait finalised (ie. when TraitsUI
            # supports PyQt) convert it explcitly to a colour.
            text_color = QtGui.QColor(self.text_color)

        control.showMessage(self.text, QtCore.Qt.AlignLeft, text_color)
