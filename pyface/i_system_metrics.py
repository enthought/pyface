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
""" The interface to system metrics (screen width and height etc). """


# Enthought library imports.
from traits.api import Int, Interface, Tuple


class ISystemMetrics(Interface):
    """ The interface to system metrics (screen width and height etc). """

    #### 'ISystemMetrics' interface ###########################################

    #: The width of the screen in pixels.
    screen_width = Int

    #: The height of the screen in pixels.
    screen_height = Int

    #: Background color of a standard dialog window as a tuple of RGB values
    #: between 0.0 and 1.0.
    # FIXME v3: Why isn't this a traits colour?
    dialog_background_color = Tuple


class MSystemMetrics(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the ISystemMetrics interface.
    """
