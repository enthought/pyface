# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


import logging
import threading


from pyface.qt import QtCore, QtGui


from traits.api import Bool, HasTraits, observe, provides, Str
from pyface.util.guisupport import start_event_loop_qt4


from pyface.i_gui import IGUI, MGUI


# Logging.
logger = logging.getLogger(__name__)


@provides(IGUI)
class GUI(MGUI, HasTraits):
    """ The toolkit specific implementation of a GUI.  See the IGUI interface
    for the API documentation.
    """

    # 'GUI' interface -----------------------------------------------------#

    busy = Bool(False)

    started = Bool(False)

    state_location = Str()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, splash_screen=None):
        # Display the (optional) splash screen.
        self._splash_screen = splash_screen

        if self._splash_screen is not None:
            self._splash_screen.open()

    # ------------------------------------------------------------------------
    # 'GUI' class interface.
    # ------------------------------------------------------------------------

    @classmethod
    def invoke_after(cls, millisecs, callable, *args, **kw):
        _FutureCall(millisecs, callable, *args, **kw)

    @classmethod
    def invoke_later(cls, callable, *args, **kw):
        _FutureCall(0, callable, *args, **kw)

    @classmethod
    def set_trait_after(cls, millisecs, obj, trait_name, new):
        _FutureCall(millisecs, setattr, obj, trait_name, new)

    @classmethod
    def set_trait_later(cls, obj, trait_name, new):
        _FutureCall(0, setattr, obj, trait_name, new)

    @staticmethod
    def process_events(allow_user_events=True):
        if allow_user_events:
            events = QtCore.QEventLoop.ProcessEventsFlag.AllEvents
        else:
            events = QtCore.QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents

        QtCore.QCoreApplication.processEvents(events)

    @staticmethod
    def set_busy(busy=True):
        if busy:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        else:
            QtGui.QApplication.restoreOverrideCursor()

    # ------------------------------------------------------------------------
    # 'GUI' interface.
    # ------------------------------------------------------------------------

    def start_event_loop(self):
        if self._splash_screen is not None:
            self._splash_screen.close()

        # Make sure that we only set the 'started' trait after the main loop
        # has really started.
        self.set_trait_later(self, "started", True)

        logger.debug("---------- starting GUI event loop ----------")
        start_event_loop_qt4()

        self.started = False

    def stop_event_loop(self):
        logger.debug("---------- stopping GUI event loop ----------")
        QtGui.QApplication.quit()

    # ------------------------------------------------------------------------
    # Trait handlers.
    # ------------------------------------------------------------------------

    def _state_location_default(self):
        """ The default state location handler. """

        return self._default_state_location()

    @observe("busy")
    def _update_busy_state(self, event):
        """ The busy trait change handler. """
        new = event.new
        if new:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        else:
            QtGui.QApplication.restoreOverrideCursor()


class _FutureCall(QtCore.QObject):
    """ This is a helper class that is similar to the wx FutureCall class. """

    # Keep a list of references so that they don't get garbage collected.
    _calls = []

    # Manage access to the list of instances.
    _calls_mutex = QtCore.QMutex()

    # A new Qt event type for _FutureCalls
    _pyface_event = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

    def __init__(self, ms, callable, *args, **kw):
        super().__init__()

        # Save the arguments.
        self._ms = ms
        self._callable = callable
        self._args = args
        self._kw = kw

        # Save the instance.
        self._calls_mutex.lock()
        try:
            self._calls.append(self)
        finally:
            self._calls_mutex.unlock()

        # Move to the main GUI thread if necessary.
        # Note that calling QApplication.thread() seems to cause an
        # atexit-time segfault on Linux under some versions of PySide6.
        # xref: https://bugreports.qt.io/browse/PYSIDE-2254
        # xref: https://github.com/enthought/pyface/issues/1211
        if threading.current_thread() != threading.main_thread():
            self.moveToThread(QtGui.QApplication.instance().thread())

        # Post an event to be dispatched on the main GUI thread. Note that
        # we do not call QTimer.singleShot here, which would be simpler, because
        # that only works on QThreads. We want regular Python threads to work.
        event = QtCore.QEvent(self._pyface_event)
        QtGui.QApplication.postEvent(self, event)

    def event(self, event):
        """ QObject event handler.
        """
        if event.type() == self._pyface_event:
            # Invoke the callable (puts it at the end of the event queue)
            QtCore.QTimer.singleShot(self._ms, self._dispatch)
            return True

        return super().event(event)

    def _dispatch(self):
        """ Invoke the callable.
        """
        try:
            self._callable(*self._args, **self._kw)
        finally:
            self._finished()

    def _finished(self):
        """ Remove the call from the list, so it can be garbage collected.
        """
        self._calls_mutex.lock()
        try:
            self._calls.remove(self)
        finally:
            self._calls_mutex.unlock()
