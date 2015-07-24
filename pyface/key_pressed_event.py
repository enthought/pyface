""" The event that is generated when a key is pressed. """


# Enthought library imports.
from traits.api import Bool, HasTraits, Int, Any


class KeyPressedEvent(HasTraits):
    """ The event that is generated when a key is pressed. """

    #### 'KeyPressedEvent' interface ##########################################

    #: Is the alt key down?
    alt_down = Bool

    #: Is the control key down?
    control_down = Bool

    #: Is the shift key down?
    shift_down = Bool

    #: The keycode.
    key_code = Int

    #: The original toolkit specific event.
    event = Any

#### EOF ######################################################################
