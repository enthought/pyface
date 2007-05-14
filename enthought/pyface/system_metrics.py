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
""" System metrics (screen width and height etc). """


# Enthought library imports.
from enthought.traits.api import HasTraits, Int, Property

# Private Enthought library imports.
from enthought.pyface.toolkit import patch_toolkit


class SystemMetrics(HasTraits):
    """ System metrics (screen width and height etc). """

    __tko__ = 'SystemMetrics'

    # fixme: add in all the other metrics as we find the need for them.

    #### 'SystemMetrics' interface ############################################
    
    # The width of the screen in pixels.    
    screen_width = Property(Int)

    # The height of the screen in pixels.
    screen_height = Property(Int)
    
    # Background color of a standard dialog window as a tuple of RGB values 
    # between 0.0 and 1.0.
    dialog_background_color = Property
    
    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *args, **traits):
        """ Initialise the instance. """

        super(SystemMetrics, self).__init__(*args, **traits)

        patch_toolkit(self)

        return

    ###########################################################################
    # 'SystemMetrics' interface.
    ###########################################################################

    #### Properties ###########################################################
    
    def _get_screen_width(self):
        """ Returns the width of the screen in pixels. """

        return self._tk_systemmetrics_get_screen_width()
    
    def _get_screen_height(self):
        """ Returns the height of the screen in pixels. """

        return self._tk_systemmetrics_get_screen_height()

    def _get_dialog_background_color(self):
        """ Returns the background color of a standard dialog window as an RGB
        tuple.  RGB values range between 0.0-1.0 
        """

        return self._tk_systemmetrics_get_dialog_background_color()

    ###########################################################################
    # 'SystemMetrics' toolkit interface.
    ###########################################################################

    def _tk_systemmetrics_get_screen_width(self):
        """ Returns the width of the screen in pixels.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_systemmetrics_get_screen_height(self):
        """ Returns the height of the screen in pixels.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_systemmetrics_get_dialog_background_color(self):
        """ Returns the background color of a standard dialog window as an RGB
        tuple.  RGB values range between 0.0-1.0 

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
