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

from pyface.gui import GUI
from pyface.qt import QtGui
from traits.api import Any, HasTraits, Instance



class MyWindow(HasTraits):
    control = Any()

    parent = Any()

    def _create(self):
        self.control = self._create_control(self.parent)

    def _create_control(self, parent):
        control = QtGui.QMainWindow(parent)
        control.setEnabled(True)
        control.setVisible(True)
        return control

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
            if self.control is not None:
                self.control.deleteLater()
                if self.control is not None:
                    self.control = None
            # super().destroy()
            control.close()
            control.hide()

    def open(self):
        if self.control is None:
            self._create()

    def close(self, force=False):
        """Closes the window."""
        if self.control is not None:
            if force:
                self.destroy()


class MyTasksApplication(HasTraits):
    window = Instance(MyWindow)

    def run(self):
        gui = GUI()
        window = MyWindow()
        window.open()
        self.window = window
        gui.invoke_later(self.exit)
        gui.start_event_loop()

    def exit(self):
        window = self.window
        self.window = None
        window.close()
        window.destroy()
        # window.closed = True


class TestTasksApplication(unittest.TestCase):
    def test_lifecycle(self):
        app = MyTasksApplication()
        app.run()

        # Run the event loop
        # gui = GUI()
        # gui.invoke_after(100, gui.stop_event_loop)
        # gui.start_event_loop()
