# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import weakref

from pyface.qt import QtCore, QtGui


from traits.api import (
    Enum,
    Event,
    Property,
    Tuple,
    Str,
    VetoableEvent,
    provides,
)


from pyface.i_window import IWindow, MWindow
from pyface.key_pressed_event import KeyPressedEvent
from .gui import GUI
from .widget import Widget


@provides(IWindow)
class Window(MWindow, Widget):
    """ The toolkit specific implementation of a Window.  See the IWindow
    interface for the API documentation.
    """

    # 'IWindow' interface -----------------------------------------------------

    position = Property(Tuple)

    size = Property(Tuple)

    size_state = Enum("normal", "maximized")

    title = Str()

    # Window Events ----------------------------------------------------------

    #: The window has been opened.
    opened = Event()

    #: The window is about to open.
    opening = VetoableEvent()

    #: The window has been activated.
    activated = Event()

    #: The window has been closed.
    closed = Event()

    #: The window is about to be closed.
    closing = VetoableEvent()

    #: The window has been deactivated.
    deactivated = Event()

    # Private interface ------------------------------------------------------

    #: Shadow trait for position.
    _position = Tuple((-1, -1))

    #: Shadow trait for size.
    _size = Tuple((-1, -1))

    # -------------------------------------------------------------------------
    # 'IWindow' interface.
    # -------------------------------------------------------------------------

    def activate(self):
        self.control.activateWindow()
        self.control.raise_()
        # explicitly fire activated trait as signal doesn't create Qt event
        self.activated = self

    # -------------------------------------------------------------------------
    # Protected 'IWindow' interface.
    # -------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create a default QMainWindow. """
        control = QtGui.QMainWindow(parent)

        if self.size != (-1, -1):
            control.resize(*self.size)
        if self.position != (-1, -1):
            control.move(*self.position)
        if self.size_state != "normal":
            self._size_state_changed(self.size_state)
        control.setWindowTitle(self.title)
        control.setEnabled(self.enabled)

        # XXX starting with visible true is not recommended
        control.setVisible(self.visible)

        return control

    # -------------------------------------------------------------------------
    # 'IWidget' interface.
    # -------------------------------------------------------------------------

    def destroy(self):

        if self.control is not None:
            # Avoid problems with recursive calls.
            # Widget.destroy() sets self.control to None,
            # so we need a reference to control
            control = self.control

            # Widget.destroy() sets self.control to None and deletes it later,
            # so we call it before control.close()
            # This is not strictly necessary (closing the window in fact
            # hides it), but the close may trigger an application shutdown,
            # which can take a long time and may also attempt to recursively
            # destroy the window again.
            super().destroy()
            control.close()
            control.hide()

    # -------------------------------------------------------------------------
    # Private interface.
    # -------------------------------------------------------------------------

    def _get_position(self):
        """ Property getter for position. """

        return self._position

    def _set_position(self, position):
        """ Property setter for position. """

        if self.control is not None:
            self.control.move(*position)

        old = self._position
        self._position = position

        self.trait_property_changed("position", old, position)

    def _get_size(self):
        """ Property getter for size. """

        return self._size

    def _set_size(self, size):
        """ Property setter for size. """

        if self.control is not None:
            self.control.resize(*size)

        old = self._size
        self._size = size

        self.trait_property_changed("size", old, size)

    def _size_state_changed(self, state):
        control = self.control
        if control is None:
            return  # Nothing to do here

        if state == "maximized":
            control.setWindowState(
                control.windowState() | QtCore.Qt.WindowState.WindowMaximized
            )
        elif state == "normal":
            control.setWindowState(
                control.windowState() & ~QtCore.Qt.WindowState.WindowMaximized
            )

    def _title_changed(self, title):
        """ Static trait change handler. """

        if self.control is not None:
            self.control.setWindowTitle(title)

    def __event_filter_default(self):
        return WindowEventFilter(self)


class WindowEventFilter(QtCore.QObject):
    """ An internal class that watches for certain events on behalf of the
    Window instance.
    """

    def __init__(self, window):
        """ Initialise the event filter. """
        QtCore.QObject.__init__(self)
        # use a weakref to fix finalization issues with circular references
        # we don't want to be the last thing holding a reference to the window
        self._window = weakref.ref(window)

    def eventFilter(self, obj, e):
        """ Adds any event listeners required by the window. """

        window = self._window()

        # Sanity check.
        if window is None or obj is not window.control:
            return False

        typ = e.type()

        if typ == QtCore.QEvent.Type.Close:
            # Do not destroy the window during its event handler.
            GUI.invoke_later(window.close)

            if window.control is not None:
                e.ignore()

            return True

        if typ == QtCore.QEvent.Type.WindowActivate:
            window.activated = window

        elif typ == QtCore.QEvent.Type.WindowDeactivate:
            window.deactivated = window

        elif typ in {QtCore.QEvent.Type.Show, QtCore.QEvent.Type.Hide}:
            window.visible = window.control.isVisible()

        elif typ == QtCore.QEvent.Type.Resize:
            # Get the new size and set the shadow trait without performing
            # notification.
            size = e.size()
            window._size = (size.width(), size.height())

        elif typ == QtCore.QEvent.Type.Move:
            # Get the real position and set the trait without performing
            # notification. Don't use event.pos(), as this excludes the window
            # frame geometry.
            pos = window.control.pos()
            window._position = (pos.x(), pos.y())

        elif typ == QtCore.QEvent.Type.KeyPress:
            # Pyface doesn't seem to be Str aware.  Only keep the key code
            # if it corresponds to a single Latin1 character.
            kstr = e.text()
            try:
                kcode = ord(str(kstr))
            except:
                kcode = 0

            mods = e.modifiers()
            window.key_pressed = KeyPressedEvent(
                alt_down=(
                    (mods & QtCore.Qt.KeyboardModifier.AltModifier) == QtCore.Qt.KeyboardModifier.AltModifier
                ),
                control_down=(
                    (mods & QtCore.Qt.KeyboardModifier.ControlModifier)
                    == QtCore.Qt.KeyboardModifier.ControlModifier
                ),
                shift_down=(
                    (mods & QtCore.Qt.KeyboardModifier.ShiftModifier) == QtCore.Qt.KeyboardModifier.ShiftModifier
                ),
                key_code=kcode,
                event=e,
            )

        elif typ == QtCore.QEvent.Type.WindowStateChange:
            # set the size_state of the window.
            state = obj.windowState()
            if state & QtCore.Qt.WindowState.WindowMaximized:
                window.size_state = "maximized"
            else:
                window.size_state = "normal"

        return False
