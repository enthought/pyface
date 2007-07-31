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
""" The interface for workbench views. """


# Enthought library imports.
from enthought.traits.api import Bool, Enum, Float, List, Str

# Local imports.
from i_perspective_item import IPerspectiveItem
from i_workbench_part import IWorkbenchPart, MWorkbenchPart


class IView(IWorkbenchPart, IPerspectiveItem):
    """ The interface for workbench views. """

    # Is the view busy? (i.e., should the busy cursor (often an hourglass) be
    # displayed?).
    busy = Bool(False)

    # Whether the view is visible or not.
    visible = Bool(False)


class MView(MWorkbenchPart):
    """ Mixin containing common code for toolkit-specific implementations. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __str__(self):
        """ Return an informal string representation of the object. """

        return 'View(%s)' % self.id

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """

        # If no Id is specified then use the name.
        return self.name
    
#### EOF ######################################################################
