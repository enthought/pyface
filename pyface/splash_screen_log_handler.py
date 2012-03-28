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
""" A log handler that emits records to a splash screen. """


# Standard library imports.
from logging import Handler


class SplashScreenLogHandler(Handler):
    """ A log handler that displays log messages on a splash screen. """

    def __init__(self, splash_screen):
        """ Creates a new handler for a splash screen. """

        # Base class constructor.
        Handler.__init__(self)

        # The splash screen that we will display log messages on.
        self._splash_screen = splash_screen

        return

    def emit(self, record):
        """ Emits the log record. """

        self._splash_screen.text = unicode(record.getMessage()) + u'...'

        return

#### EOF ######################################################################
