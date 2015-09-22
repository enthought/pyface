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
""" The interface for a simple 'About' dialog. """

# Enthought library imports.
from traits.api import Instance, List, Unicode

# Local imports.
from pyface.i_dialog import IDialog
from pyface.image_resource import ImageResource


class IAboutDialog(IDialog):
    """ The interface for a simple 'About' dialog. """

    #### 'IAboutDialog' interface #############################################

    #: Additional strings to be added to the dialog.
    additions = List(Unicode)

    #: The image displayed in the dialog.
    image = Instance(ImageResource, ImageResource('about'))


class MAboutDialog(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IAboutDialog interface.
    """
