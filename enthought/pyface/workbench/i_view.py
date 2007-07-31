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
from i_workbench_part import IWorkbenchPart, MWorkbenchPart


class IView(IWorkbenchPart):
    """ The interface for workbench views. """

    # Is the view busy? (i.e., should the busy cursor (often an hourglass) be
    # displayed?).
    busy = Bool(False)

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
