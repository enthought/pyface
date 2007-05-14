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
""" The default implementation of the 'IView' interface. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Any, Bool, Enum, Float, HasTraits, Instance
from enthought.traits.api import List, Str, implements  

# Private Enthought library imports.
from enthought.pyface.toolkit import patch_toolkit

# Local imports.
from i_view import IView
from workbench_window import WorkbenchWindow


# Logging.
logger = logging.getLogger(__name__)


class View(HasTraits):
    """ The default implementation of the 'IView' interface. """

    __tko__ = 'View'

    implements(IView)
    
    #### 'View' interface #####################################################
    
    # Is the view busy? (i.e., should the busy cursor (often an hourglass) be
    # displayed?).
    busy = Bool(False)

    # The toolkit-specific control that represents the view.
    #
    # The framework sets this to the value returned by 'create_control'.
    control = Any

    # Does the view currently have the focus?
    has_focus = Bool(False)
    
    # The view's globally unique identifier.
    id = Str

    # The view's name.
    name = Str

    # The current selection within the view.
    selection = List

    # The workbench window that the view is in.
    #
    # The framework sets this when the view is added to a window.
    window = Instance(WorkbenchWindow)

    # Whether the view is visible or not.
    visible = Bool(True)

    # The following traits specify the *default* position of the view. This
    # information is only used if the view is added to a perspective that
    # it is not explicitly part of (i.e. it does not appear in the
    # perspective's 'contents'.
    #
    # This often happens because:-
    #
    # a) The application doesn't define any perspectives
    # b) The user can add/remove any view to/from any perspective
    #
    # fixme: These traits are idential to those in 'PerspectiveItem'. How can
    # we unify them?
    
    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    #
    # 'top'    puts the view above the 'relative_to' item.
    # 'bottom' puts the view below the 'relative_to' item.
    # 'left'   puts the view to the left of  the 'relative_to' item.
    # 'right'  puts the view to the right of the 'relative_to' item.
    # 'with'   puts the view in the same region as the 'relative_to' item.
    #
    # If the position is specified as 'with' you must specify a 'relative_to'
    # item other than the editor area (i.e., you cannot position a view 'with'
    # the editor area).
    position = Enum('left', 'top', 'bottom', 'right', 'with')

    # The Id of the view to position this view relative to. If this is not
    # specified (or if no view exists with this Id) then the view will be
    # placed relative to the editor area.
    relative_to = Str

    # The default width of the view (as a fraction of the window width).
    #
    # e.g. 0.5 == half the window width.
    #
    # Note that this is treated as a suggestion, and it may not be possible for
    # the workbench to allocate space requested.
    width = Float(-1)

    # The default height of the view (as a fraction of the window height).
    #
    # e.g. 0.5 == half the window height.
    #
    # Note that this is treated as a suggestion, and it may not be possible for
    # the workbench to allocate space requested.
    height = Float(-1)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *args, **traits):
        """ Initialise the instance. """

        super(View, self).__init__(*args, **traits)

        patch_toolkit(self)

        return
    
    ###########################################################################
    # 'View' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _id_default(self):
        """ Trait initializer. """

        # If no Id is specified then use the name.
        return self.name
    
    #### Methods ##############################################################
    
    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        View implementors should override this!

        """

        return self._tk_view_create(parent)

    def destroy_control(self):
        """ Destroys the toolkit-specific control that represents the view.

        """

        if self.control is not None:
            logger.debug('destroying control for view [%s]', self)
            self._tk_view_destroy()

        else:
            logger.debug('no control to destroy for view [%s]', self)

        return

    def set_focus(self):
        """ Sets the focus to the appropriate control in the view.

        By default we set the focus to be the view's top-level control. If
        you need to give focus to some child control then override.

        """

        if self.control is not None:
            self._tk_view_set_focus()

        return

    ###########################################################################
    # 'View' toolkit interface.
    ###########################################################################

    def _tk_view_create(self, parent):
        """ Create a default control.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_view_destroy(self):
        """ Destroy the control.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_view_set_focus(self):
        """ Set the focus to the control.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
