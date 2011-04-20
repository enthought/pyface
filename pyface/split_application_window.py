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
""" A window that is split in two either horizontally or vertically. """


# Local imports.
from application_window import ApplicationWindow
from split_widget import SplitWidget


class SplitApplicationWindow(ApplicationWindow, SplitWidget):
    """ A window that is split in two either horizontally or vertically. """

    ###########################################################################
    # Protected 'ApplicationWindow' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        return self._create_splitter(parent)

#### EOF ######################################################################
