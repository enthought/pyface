#-------------------------------------------------------------------------------
#
#  Copyright (c) 2006, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: David C. Morrill
#  Date:   06/17/2006
#
#-------------------------------------------------------------------------------

""" Defines the IDockUIProvider interface which objects which support being
    dragged and dropped into a DockWindow must implement.
"""

#-------------------------------------------------------------------------------
#  'IDockUIProvider' class:
#-------------------------------------------------------------------------------

class IDockUIProvider ( object ):

    #---------------------------------------------------------------------------
    #  Returns a Traits UI which a DockWindow can imbed:
    #---------------------------------------------------------------------------

    def get_dockable_ui ( self, parent ):
        """ Returns a Traits UI which a DockWindow can imbed.
        """
        return self.edit_traits( parent     = parent,
                                 kind       = 'subpanel',
                                 scrollable = True )

