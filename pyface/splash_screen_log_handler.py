# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A log handler that emits records to a splash screen. """


from logging import Handler


class SplashScreenLogHandler(Handler):
    """ A log handler that displays log messages on a splash screen. """

    def __init__(self, splash_screen):
        """ Creates a new handler for a splash screen.

        Parameters
        ----------
        splash_screen : ISplashScreen
            The splash screen being used to display the log messages
        """
        # Base class constructor.
        super().__init__()

        # The splash screen that we will display log messages on.
        self._splash_screen = splash_screen

    def emit(self, record):
        """ Emits the log record's message to the splash screen.

        Parameters
        ----------
        record : logging record
            The log record to be displayed.
        """
        self._splash_screen.text = str(record.getMessage()) + "..."
