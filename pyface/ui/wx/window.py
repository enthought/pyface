# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Enthought pyface package component
"""


import wx


from traits.api import Event, Property, Tuple, Str, VetoableEvent, provides


from pyface.i_window import IWindow, MWindow
from pyface.key_pressed_event import KeyPressedEvent
from .system_metrics import SystemMetrics
from .widget import Widget


@provides(IWindow)
class Window(MWindow, Widget):
    """ The toolkit specific implementation of a Window.  See the IWindow
    interface for the API documentation.
    """

    # 'IWindow' interface -----------------------------------------------------

    position = Property(Tuple)

    size = Property(Tuple)

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

    #: A key was pressed while the window had focus.
    # FIXME v3: This smells of a hack. What's so special about key presses?
    # FIXME v3: Str
    key_pressed = Event(KeyPressedEvent)

    size = Property(Tuple)

    # Private interface ------------------------------------------------------

    # Shadow trait for position.
    _position = Tuple((-1, -1))

    # Shadow trait for size.
    _size = Tuple((-1, -1))

    # -------------------------------------------------------------------------
    # 'IWindow' interface.
    # -------------------------------------------------------------------------

    def activate(self):
        self.control.Iconize(False)
        self.control.Raise()

    def show(self, visible):
        self.control.Show(visible)

    # -------------------------------------------------------------------------
    # Protected 'IWindow' interface.
    # -------------------------------------------------------------------------

    def _add_event_listeners(self):
        super()._add_event_listeners()
        self.control.Bind(wx.EVT_ACTIVATE, self._wx_on_activate)
        self.control.Bind(wx.EVT_SHOW, self._wx_on_show)
        self.control.Bind(wx.EVT_CLOSE, self._wx_on_close)
        self.control.Bind(wx.EVT_SIZE, self._wx_on_control_size)
        self.control.Bind(wx.EVT_MOVE, self._wx_on_control_move)
        self.control.Bind(wx.EVT_CHAR, self._wx_on_char)

    # -------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # -------------------------------------------------------------------------

    def _create_control(self, parent):
        # create a basic window control

        style = (
            wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_WINDOW_MENU | wx.CLIP_CHILDREN
        )
        control = wx.Frame(
            parent,
            -1,
            self.title,
            style=style,
            size=self.size,
            pos=self.position,
        )
        control.SetBackgroundColour(SystemMetrics().dialog_background_color)
        control.Enable(self.enabled)

        # XXX starting with self.visible true is generally a bad idea
        control.Show(self.visible)

        return control

    # -------------------------------------------------------------------------
    # Private interface.
    # -------------------------------------------------------------------------

    def _get_position(self):
        """ Property getter for position. """

        return self._position

    def _set_position(self, position):
        """ Property setter for position. """

        if self.control is not None:
            self.control.SetPosition(position)

        old = self._position
        self._position = position

        self.trait_property_changed("position", old, position)

    def _get_size(self):
        """ Property getter for size. """

        return self._size

    def _set_size(self, size):
        """ Property setter for size. """

        if self.control is not None:
            self.control.SetSize(size)

        old = self._size
        self._size = size

        self.trait_property_changed("size", old, size)

    def _title_changed(self, title):
        """ Static trait change handler. """

        if self.control is not None:
            self.control.SetTitle(title)

    # wx event handlers ------------------------------------------------------

    def _wx_on_activate(self, event):
        """ Called when the frame is being activated or deactivated. """

        if event.GetActive():
            self.activated = self
        else:
            self.deactivated = self

        event.Skip()

    def _wx_on_show(self, event):
        """ Called when the frame is being activated or deactivated. """

        self.visible = event.IsShown()

        event.Skip()

    def _wx_on_close(self, event):
        """ Called when the frame is being closed. """

        self.close()

    def _wx_on_control_move(self, event):
        """ Called when the window is resized. """

        # Get the real position and set the trait without performing
        # notification.

        # WXBUG - From the API documentation you would think that you could
        # call event.GetPosition directly, but that would be wrong.  The pixel
        # reported by that call is the pixel just below the window menu and
        # just right of the Windows-drawn border.

        try:
            self._position = (
                event.GetEventObject().GetPosition().Get()
            )  # Sizer.GetPosition().Get()
        except:
            pass
        event.Skip()

    def _wx_on_control_size(self, event):
        """ Called when the window is resized. """

        # Get the new size and set the shadow trait without performing
        # notification.
        wxsize = event.GetSize()

        self._size = (wxsize.GetWidth(), wxsize.GetHeight())

        event.Skip()

    def _wx_on_char(self, event):
        """ Called when a key is pressed when the tree has focus. """

        self.key_pressed = KeyPressedEvent(
            alt_down=event.altDown,
            control_down=event.controlDown,
            shift_down=event.shiftDown,
            key_code=event.KeyCode,
            event=event,
        )

        event.Skip()
