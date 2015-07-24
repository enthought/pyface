""" The event passed to an action's 'perform' method. """


# Standard library imports.
import time

# Enthought library imports.
from traits.api import Float, HasTraits, Int


class ActionEvent(HasTraits):
    """ The event passed to an action's 'perform' method. """

    #### 'ActionEvent' interface ##############################################

    #: When the action was performed (time.time()).
    when = Float

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Creates a new action event.

        Note: Every keyword argument becoames a public attribute of the event.
        """
        # Base-class constructor.
        super(ActionEvent, self).__init__(**traits)

        # When the action was performed.
        self.when = time.time()
