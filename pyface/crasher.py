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


class MyWindow:

    def __init__(self):
        self.control = None

    def open(self):
        if self.control is None:
            control = QtGui.QMainWindow()
            control.setEnabled(True)
            control.setVisible(True)
            self.control = control

    def close(self):
        if self.control is not None:
            control = self.control
            self.control = None

            control.deleteLater()
            control.close()
            control.hide()


class MyApplication:

    def __init__(self):
        self.window = None

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


class TestApplication(unittest.TestCase):
    def test_lifecycle(self):
        app = MyApplication()
        app.run()

        # Run the event loop
        gui = GUI()
        gui.invoke_after(100, gui.stop_event_loop)
        gui.start_event_loop()
