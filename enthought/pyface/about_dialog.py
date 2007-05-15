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
""" A simple 'About' dialog. """


# Standard library imports.
import sys

# Enthought library imports.
from enthought.traits.api import Instance, List, String

# Local imports.
from dialog import Dialog
from image_resource import ImageResource


class AboutDialog(Dialog):
    """ A simple 'About' dialog. """

    __tko__ = 'AboutDialog'

    #### 'AboutDialog' interface ##############################################

    # The image displayed in the dialog.
    image = Instance(ImageResource, ImageResource('about'))

    # Additional strings to be added to the dialog.
    additions = List(String)

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        # Get the version of Python we are running on.
        # ...remove the more detailed info (build date, platform, etc.)
        # ...this may be needed in the future though
        py_version = sys.version[0:sys.version.find("(")]

        return self._tk_aboutdialog_create_contents(parent, py_version)

    ###########################################################################
    # 'AboutDialog' toolkit interface.
    ###########################################################################

    def _tk_aboutdialog_create_contents(self, parent, py_version):
        """ Creates the dialog contents.
        
        This must be reimplemented.
        """

        raise NotImplementedError

### EOF #######################################################################
