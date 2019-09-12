#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

#
# Author: Riverbank Computing Limited
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------


# Standard library imports.
import logging

# Major package imports.
from pyface.qt import QtCore, QtGui

# Enthought library imports.
from traits.api import Bool, HasTraits, Property, Unicode, provides
from pyface.util.guisupport import start_event_loop_qt4

# Local imports.
from pyface.i_gui import IGUI, MGUI


# Logging.
logger = logging.getLogger(__name__)


@provides(IGUI)
class GUI(MGUI, HasTraits):
    """ The toolkit specific implementation of a GUI.  See the IGUI interface
    for the API documentation.
    """


    #### 'GUI' interface ######################################################

    #: A reference to the toolkit application singleton.
    app = Property

    #: Is the GUI busy (i.e. should the busy cursor, often an hourglass, be
    #: displayed)?
    busy = Bool(False)

    #: Has the GUI's event loop been started?
    started = Bool(False)

    #: Whether the GUI quits on last window close.
    quit_on_last_window_close = Property(Bool)

    #: A directory on the local file system that we can read and write to at
    #: will.  This is used to persist layout information etc.  Note that
    #: individual toolkits will have their own directory.
    state_location = Unicode

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, splash_screen=None):
        # Display the (optional) splash screen.
        self._splash_screen = splash_screen

        if self._splash_screen is not None:
            self._splash_screen.open()

    ###########################################################################
    # 'GUI' class interface.
    ###########################################################################

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
        # process events posted via postEvent()
        QtCore.QCoreApplication.sendPostedEvents()

        if allow_user_events:
            events = QtCore.QEventLoop.AllEvents
        else:
            events = QtCore.QEventLoop.ExcludeUserInputEvents

        # process events from the window system/OS
        QtCore.QCoreApplication.processEvents(events)

    @staticmethod
    def set_busy(busy=True):
        if busy:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        else:
            QtGui.QApplication.restoreOverrideCursor()

    ###########################################################################
    # 'GUI' interface.
    ###########################################################################

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

    def top_level_windows(self):
        return self.app.topLevelWidgets()

    def close_all(self, force=False):
        if force:
            for window in self.top_level_windows():
                window.deleteLater()
        else:
            self.app.closeAllWindows()

    ###########################################################################
    # Trait handlers.
    ###########################################################################

    def _state_location_default(self):
        """ The default state location handler. """

        return self._default_state_location()

    def _busy_changed(self, new):
        """ The busy trait change handler. """

        if new:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        else:
            QtGui.QApplication.restoreOverrideCursor()

    # Property handlers -----------------------------------------------------

    def _get_app(self):
        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QtGui.QApplication()
        return app

    def _get_quit_on_last_window_close(self):
        return self.app.quitOnLastWindowClosed()

    def _set_quit_on_last_window_close(self, value):
        return self.app.setQuitOnLastWindowClosed(value)


class _FutureCall(QtCore.QObject):
    """ This is a helper class that is similar to the wx FutureCall class. """

    # Keep a list of references so that they don't get garbage collected.
    _calls = []

    # Manage access to the list of instances.
    _calls_mutex = QtCore.QMutex()

    # A new Qt event type for _FutureCalls
    _pyface_event = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

    def __init__(self, ms, callable, *args, **kw):
        super(_FutureCall, self).__init__()

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

        # Move to the main GUI thread.
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
            if self._ms == 0:
                # Invoke the callable now
                try:
                    self._callable(*self._args, **self._kw)
                finally:
                    # We cannot remove from self._calls here. QObjects don't like being
                    # garbage collected during event handlers (there are tracebacks,
                    # plus maybe a memory leak, I think).
                    QtCore.QTimer.singleShot(0, self._finished)
            else:
                # Invoke the callable (puts it at the end of the event queue)
                QtCore.QTimer.singleShot(self._ms, self._dispatch)
            return True

        return super(_FutureCall, self).event(event)

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
