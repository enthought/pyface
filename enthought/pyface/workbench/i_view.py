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


# Standard library imports.
import logging

# Enthought library imports.
from enthought.pyface.api import ImageResource
from enthought.traits.api import Bool, Enum, Float, Instance, List, Str
from enthought.traits.api import implements

# Local imports.
from i_perspective_item import IPerspectiveItem
from i_workbench_part import IWorkbenchPart, MWorkbenchPart
from perspective_item import PerspectiveItem


# Logging.
logger = logging.getLogger(__name__)


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
    # 'IWorkbenchPart' interface.
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """

        id = '%s.%s' % (type(self).__module__, type(self).__name__)
        logger.warn('view %s has no Id - using <%s>' % (self, id))

        # If no Id is specified then use the name.
        return id

    def _name_default(self):
        """ Trait initializer. """

        name = camel_case_to_words(type(self).__name__)
        logger.warn('view %s has no name - using <%s>' % (self, name))

        return name

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

# fixme: This is duplicated in 'plugin.py' where should it go?!?
def camel_case_to_words(s):
    """ Turn a string from CamelCase into words separated by spaces.

    e.g. 'CamelCase' -> 'Camel Case'

    """
    
    def add_space_between_words(s, c):
        # We detect a word boundary if the character we are looking at is
        # upper case, but the character preceding it is lower case.
        if len(s) > 0 and s[-1].islower() and c.isupper():
            return s + ' ' + c

        return s + c

    return reduce(add_space_between_words, s, '')
    
#### EOF ######################################################################
