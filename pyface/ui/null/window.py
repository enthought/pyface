# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from traits.api import Event, Property, provides, Str
from traits.api import Tuple


from pyface.i_window import IWindow, MWindow
from pyface.key_pressed_event import KeyPressedEvent
from .widget import Widget


@provides(IWindow)
class Window(MWindow, Widget):
    """ The toolkit specific implementation of a Window.  See the IWindow
    interface for the API documentation.
    """

    # 'IWindow' interface -------------------------------------------------#

    position = Property(Tuple)

    size = Property(Tuple)

    title = Str()

    # Events -----

    activated = Event()

    closed = Event()

    closing = Event()

    deactivated = Event()

    key_pressed = Event(KeyPressedEvent)

    opened = Event()

    opening = Event()

    # Private interface ----------------------------------------------------

    # Shadow trait for position.
    _position = Tuple((-1, -1))

    # Shadow trait for size.
    _size = Tuple((-1, -1))

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def show(self, visible):
        pass

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_position(self):
        """ Property getter for position. """

        return self._position

    def _set_position(self, position):
        """ Property setter for position. """

        old = self._position
        self._position = position

        self.trait_property_changed("position", old, position)

    def _get_size(self):
        """ Property getter for size. """

        return self._size

    def _set_size(self, size):
        """ Property setter for size. """

        old = self._size
        self._size = size

        self.trait_property_changed("size", old, size)
