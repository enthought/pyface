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
from enthought.pyface.api import ImageResource
from enthought.traits.api import Bool, Enum, Float, Instance, List, Str
from enthought.traits.api import implements

# Local imports.
from i_perspective_item import IPerspectiveItem
from i_workbench_part import IWorkbenchPart, MWorkbenchPart
from perspective_item import PerspectiveItem


class IView(IWorkbenchPart, IPerspectiveItem):
    """ The interface for workbench views. """

    # Is the view busy? (i.e., should the busy cursor (often an hourglass) be
    # displayed?).
    busy = Bool(False)

    # The category that the view belongs to (this can used to group views when
    # they are displayed to the user).
    category = Str('General')

    # An image used to represent the view to the user (shown in the view tab
    # and in the view chooser etc).
    image = Instance(ImageResource)
    
    # Whether the view is visible or not.
    visible = Bool(False)

    ###########################################################################
    # 'IView' interface.
    ###########################################################################

    def activate(self):
        """ Activate the view.

        """
        
    def hide(self):
        """ Hide the view.

        """

    def show(self):
        """ Show the view.

        """


class MView(MWorkbenchPart, PerspectiveItem):
    """ Mixin containing common code for toolkit-specific implementations. """

    implements(IView)

    #### 'IView' interface ####################################################
    
    # Is the view busy? (i.e., should the busy cursor (often an hourglass) be
    # displayed?).
    busy = Bool(False)

    # The category that the view belongs to (this can be used to group views
    # when they are displayed to the user).
    category = Str('General')

    # An image used to represent the view to the user (shown in the view tab
    # and in the view chooser etc).
    image = Instance(ImageResource)

    # Whether the view is visible or not.
    visible = Bool(False)
    
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

    ###########################################################################
    # 'IView' interface.
    ###########################################################################

    def activate(self):
        """ Activate the view.

        """

        self.window.activate_view(self)

        return
    
    def hide(self):
        """ Hide the view. """

        self.window.hide_view(self)

        return

    def show(self):
        """ Show the view. """

        self.window.show_view(self)

        return
    
#### EOF ######################################################################
