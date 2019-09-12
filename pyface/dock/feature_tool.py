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
#  Date:   07/04/2006
#
#-------------------------------------------------------------------------------

""" Implements the FeatureTool feature that allows a dragged object
    implementing the IFeatureTool interface to be dropped onto any compatible
    object.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from pyface.image_resource import ImageResource
from .dock_window_feature import DockWindowFeature

#-------------------------------------------------------------------------------
#  'FeatureTool' class:
#-------------------------------------------------------------------------------

class FeatureTool ( DockWindowFeature ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    image = ImageResource( 'feature_tool' )

    #---------------------------------------------------------------------------
    #  Returns whether a specified object can be dropped on the feature image:
    #---------------------------------------------------------------------------

    def can_drop ( self, object ):
        """ Returns whether a specified object can be dropped on the feature
            image.
        """
        return True

