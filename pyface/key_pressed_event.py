# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The event that is generated when a key is pressed. """


from traits.api import Bool, HasTraits, Int, Any


class KeyPressedEvent(HasTraits):
    """ The event that is generated when a key is pressed. """

    # 'KeyPressedEvent' interface -----------------------------------------#

    #: Is the alt key down?
    alt_down = Bool()

    #: Is the control key down?
    control_down = Bool()

    #: Is the shift key down?
    shift_down = Bool()

    #: The keycode.
    key_code = Int()

    #: The original toolkit specific event.
    event = Any()
