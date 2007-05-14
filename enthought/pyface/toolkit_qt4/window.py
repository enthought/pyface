#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtCore, QtGui

# Enthought library imports.
from enthought.pyface.api import KeyPressedEvent


class Window_qt4(object):
    """ The Window monkey patch for Qt4. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create_control(self, parent):
        """ Create and return the toolkit specific control that represents the
        window.
        """

        control = QtGui.QWidget(parent)
        control.setWindowTitle(self.title)

        if self.position != (-1, -1):
            control.move(*self.position)

        if self.size != (-1, -1):
            control.resize(*self.size)

    ###########################################################################
    # 'Window' toolkit interface.
    ###########################################################################

    def _tk_window_add_event_listeners(self, control):
        """ Adds any event listeners required by the window. """

        # Create an event filter for the control.  Note that the control
        # argument is ignored (because the original wx implementation also
        # ignores it).
        self._qt4_event_filter = _EventFilter(self)
    
    def _tk_window_create_contents(self, parent):
        """ Create and return the (optional) window contents. """

        panel = QtGui.QWidget(parent)
        panel.resize(500, 400)

        pal = panel.palette()
        pal.setColor(QtGui.QPalette.Window, QtCore.Qt.blue)
        panel.setPalette(pal)
        panel.setAutoFillBackground(True)

        if isinstance(parent, QtGui.QMainWindow):
            parent.setCentralWidget(panel)

        return panel
            
    def _tk_window_layout_contents(self, content):
        """ Layout the window contents. """

        self.sizer.addWidget(content)

    def _tk_window_layout_control(self):
        """ Layout the window control. """

        self.main_sizer.addWidget(self.control)

    def _tk_window_set_position(self, position):
        """ Set the window's position. """

        self.control.move(*position)

    def _tk_window_set_size(self, size):
        """ Set the window's size. """

        self.control.resize(*size)

    def _tk_window_set_title(self, title):
        """ Set the window's title. """

        self.control.setWindowTitle(title)

    def _tk_window_set_visible(self, visible):
        """ Show or hide the window. """

        self.control.setVisible(visible)

    def _qt4_on_activate(self, event):
        """ Called when the frame is being activated or deactivated. """

        # Trait notification.
        if self.control.windowState() & QtCore.Qt.WindowActive:
            self.activated = self
        else:
            self.deactivated = self

    def _qt4_on_close(self, event):
        """ Called when the frame is being closed. """

        self.close()

    def _qt4_on_control_move(self, event):
        """ Called when the window is resized. """

        # Get the real position and set the trait without performing
        # notification.
        pos = event.pos()
        self._position = (pos.x(), pos.y())

    def _qt4_on_control_size(self, event):
        """ Called when the window is resized. """

        # Get the new size and set the shadow trait without performing
        # notification.
        size = event.size()
        self._size = (size.width(), size.height())

    def _qt4_on_char(self, event):
        """ Called when a key is pressed when the tree has focus. """

        # Pyface doesn't seem to be Unicode aware.  Only keep the key code if
        # it corresponds to a single Latin1 character.
        kstr = event.text().toLatin1()

        if kstr.length() == 1:
            kcode = ord(kstr.at(0))
        else:
            kcode = 0

        mods = event.modifiers()

        self.key_pressed = KeyPressedEvent(
            alt_down     = ((mods & QtCore.Qt.AltModifier) == QtCore.Qt.AltModifier),
            control_down = ((mods & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier),
            shift_down   = ((mods & QtCore.Qt.ShiftModifier) == QtCore.Qt.ShiftModifier),
            key_code     = kcode,
            event        = event
        )


class _EventFilter(QtCore.QObject):
    """ An internal class that watches for certain events on behalf of the
        Window instance.
    """

    def __init__(self, window):
        """ Initialise the event filter. """

        QtCore.QObject.__init__(self)

        window.control.installEventFilter(self)
        self._window = window

    def eventFilter(self, obj, e):
        """ Adds any event listeners required by the window. """

        # Sanity check.
        if obj is not self._window.control:
            return False

        if e.type() == QtCore.QEvent.Close:
            self._window._qt4_on_close(e)
            e.ignore()
            return True

        if e.type() == QtCore.QEvent.WindowStateChange:
            self._window._qt4_on_activate(e)
        elif e.type() == QtCore.QEvent.Resize:
            self._window._qt4_on_control_size(e)
        elif e.type() == QtCore.QEvent.Move:
            self._window._qt4_on_control_move(e)
        elif e.type() == QtCore.QEvent.KeyPress:
            self._window._qt4_on_char(e)

        return False
