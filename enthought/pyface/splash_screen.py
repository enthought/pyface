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
""" A splash screen. """


# Standard library imports.
from logging import DEBUG

# Enthought library imports.
from enthought.logger import logger
from enthought.traits.api import Any, Bool, Font, Instance, Int, Str, Tuple

# Local imports.
from image_resource import ImageResource
from splash_screen_log_handler import SplashScreenLogHandler
from window import Window


class SplashScreen(Window):
    """ A splash screen. """

    __tko__ = 'SplashScreen'

    #### 'SplashScreen' interface #############################################
    
    # The image to display on the splash screen.
    image = Instance(ImageResource, ImageResource('splash'))

    # If log messages are to be displayed then this is the logging level. See
    # the Python documentation for the 'logging' module for more details.
    log_level = Int(DEBUG)

    # Should the splash screen display log messages in the splash text?
    show_log_messages = Bool(True)

    # Optional text to display on top of the splash image.
    text = Str

    # The text color.
    # ZZZ: When TraitsUI supports PyQt then change this to 'Color', (unless
    # that needs to toolkit to be selected too soon, in which case it may need
    # to stay as Any - or Str?)
    #text_color = WxColor('black')
    text_color = Any

    # The text font.
    # ZZZ: When TraitsUI supports PyQt then change this back to 'Font(None)'
    # with the actual default being toolkit specific.
    #text_font = Font(None)
    text_font = Any

    # The x, y location where the text will be drawn.
    text_location  = Tuple(5, 5)
    
    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def open(self):
        """ Creates the toolkit-specific control for the widget. """

        super(SplashScreen, self).open()

        if self.show_log_messages:
            self._log_handler = SplashScreenLogHandler(self)
            self._log_handler.setLevel(self.log_level)
            
            logger.addHandler(self._log_handler)

        return

    def close(self):
        """ Close the window. """

        if self.show_log_messages:
            logger.removeHandler(self._log_handler)

        super(SplashScreen, self).close()
        
        return

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        # The toolkit is expected to create the whole thing when it creates the
        # control.
        return None
        
    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait event handlers #################################################

    def _text_changed(self):
        """ Called when the splash screen text has been changed. """

        if self.control is not None:
            self._tk_splashscreen_update_text()

        return

    ###########################################################################
    # 'SplashScreen' toolkit interface.
    ###########################################################################

    def _tk_splashscreen_update_text(self):
        """ Update the splash screen text.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
