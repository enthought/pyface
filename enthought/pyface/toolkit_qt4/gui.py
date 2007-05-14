#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtCore, QtGui


class GUI_qt4(object):
    """ The GUI monkey patch for Qt4. """

    ###########################################################################
    # 'GUI' toolkit interface.
    ###########################################################################

    def _tk_gui_enter_event_loop(self):
        """ Enter the GUI event loop. """

        QtGui.QApplication.instance().exec_()

    def _tk_gui_exit_event_loop(self):
        """ Exit the GUI event loop. """

        QtGui.QApplication.quit()

    def _tk_gui_busy_cursor(self, show):
        """ Show or remove a busy cursor. """

        if show:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        else:
            QtGui.QApplication.restoreOverrideCursor()

    def _tk_gui_future_call(cls, millisecs, callable, *args, **kw):
        """ Call a callable after a specific delay in the main GUI thread.

        Returns an object with which the return value of the callable can be
        obtained.
        """

        return _FutureCall(millisecs, callable, *args, **kw)

    _tk_gui_future_call = classmethod(_tk_gui_future_call)

    def _tk_gui_call_after(cls, callable, *args, **kw):
        """ Call a callable in the main GUI thread. """

        _FutureCall(0, callable, *args, **kw)

    _tk_gui_call_after = classmethod(_tk_gui_call_after)


# This is a helper class that is similar to the wx FutureCall class.
# ZZZ: We need to implement the wx API for querying the progress and value of
# the result of a call so that it is fully compatible with the wx port (which
# itself can't change because of backwards compatibility).
class _FutureCall(QtCore.QObject):
    # Keep a list of references so that they don't get garbage collected if the
    # application isn't interested in the result or progress of a call.
    _calls = []

    # Manage access to the list of instances.
    _calls_mutex = QtCore.QMutex()

    def __init__(self, ms, callable, *args, **kw):
        QtCore.QObject.__init__(self)

        # Save the arguments.
        self._callable = callable
        self._args = args
        self._kw = kw

        # Save the instance in case the application isn't interested.
        self._calls_mutex.lock()
        self._calls.append(self)
        self._calls_mutex.unlock()

        # Connect to the dispatcher.
        self.connect(self, QtCore.SIGNAL('dispatch'), _dispatcher.dispatch)

        # Start the timer.
        QtCore.QTimer.singleShot(ms, self._fire)

    def _fire(self):
        # Remove the instance from the global list.
        self._calls_mutex.lock()
        del self._calls[self._calls.index(self)]
        self._calls_mutex.unlock()

        # Pass the arguments to the dispatcher so that the callable executes in
        # the right thread.
        self.emit(QtCore.SIGNAL('dispatch'), self._callable, self._args, self._kw)


# This singleton class simply invokes a callable.  The single instance must be
# created in the GUI thread, ie. this module must be first imported in the GUI
# thread.  The class must be derived from QObject to ensure that the right
# thread is used.
class _Dispatcher(QtCore.QObject):

    # Invoke a callable.
    def dispatch(self, callable, args, kw):
        callable(*args, **kw)

# Create the single instance.
_dispatcher = _Dispatcher()
