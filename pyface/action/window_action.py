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
""" Abstract base class for all window actions. """


# Enthought library imports.
from pyface.window import Window
from traits.api import Instance

# Local imports.
from pyface.action.action import Action


class WindowAction(Action):
    """ Abstract base class for all window actions. """

    #### 'WindowAction' interface #############################################

    #: The window that the action is associated with.
    window = Instance(Window)
