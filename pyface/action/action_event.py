# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The event passed to an action's 'perform' method. """


import time


from traits.api import Float, HasTraits


class ActionEvent(HasTraits):
    """ The event passed to an action's 'perform' method. """

    # 'ActionEvent' interface ---------------------------------------------#

    #: When the action was performed (time.time()).
    when = Float()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, **traits):
        """ Creates a new action event.

        Note: Every keyword argument becomes a public attribute of the event.
        """
        # Base-class constructor.
        super().__init__(**traits)

        # When the action was performed.
        self.when = time.time()
