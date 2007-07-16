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
""" The interface of a workbench view. """


# Enthought library imports.
from enthought.traits.api import Any, Bool, Enum, Float, Instance, Interface
from enthought.traits.api import List, Str, Unicode


class IView(Interface):
    """ The interface of a workbench view. """

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

    # The view's name (displayed to the user).
    name = Unicode

    # The current selection within the view.
    selection = List

    # The workbench window that the view is in.
    #
    # The framework sets this when the view is added to a window.
    window = Instance('WorkbenchWindow')

    # Whether the view is visible or not.
    visible = Bool(False)

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

    #### Methods ##############################################################
    
    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        Returns the toolkit-specific control.

        """

    def destroy_control(self):
        """ Destroys the toolkit-specific control that represents the view.

        Returns None.
        
        """

    def set_focus(self):
        """ Sets the focus to the appropriate control in the view.

        By default we set the focus to be the view's top-level control. If
        you need to give focus to some child control then override.

        Returns None.
        
        """


class MView(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IView interface.

    Implements: _id_default()
    """

    ###########################################################################
    # 'View' interface.
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """

        # If no Id is specified then use the name.
        return self.name
    
#### EOF ######################################################################
