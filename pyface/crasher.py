"""
The script below segfaults for me some proportion (>10%) of the time with:

- Ubuntu 22.04
- Python 3.10 (Ubuntu package)
- PySide 6.3.2 (installed via pip)

To reproduce:

- Create and activate a Python 3.10 venv with e.g.

    python -m venv --clear crasher
    source crasher/bin/activate

- Install PySide6 < 6.4 from PyPI

    python -m pip install "PySide6 < 6.4"

- Clone Pyface, check out the debug-segfault-1211 branch and install

    python -m pip install -e .

- Run this file under unittest:

    python -m unittest pyface.crasher
"""

import unittest

from PySide6 import QtWidgets

from pyface.qt import QtCore, QtGui


class _FutureCall(QtCore.QObject):
    """ This is a helper class that is similar to the wx FutureCall class. """

    # Keep a list of references so that they don't get garbage collected.
    _calls = []

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
        self._calls.append(self)

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
        self._calls.remove(self)



class MyWindow:
    def open(self):
        control = QtWidgets.QMainWindow()
        control.setEnabled(True)
        control.setVisible(True)
        self.control = control


class MyApplication:

    def run(self):
        self.app = qt_app = QtWidgets.QApplication()

        window = MyWindow()
        window.open()
        self.window = window

        _FutureCall(100, qt_app.quit)
        qt_app.exec()


class TestApplication(unittest.TestCase):
    def test_lifecycle(self):
        app = MyApplication()
        app.run()

        print("leaving")
