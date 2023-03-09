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

    python -m unittest crasher
"""

import unittest

from pyface.gui import GUI
from pyface.qt import QtGui
from traits.api import HasTraits, Instance

from .window import Window


class MyApplicationWindow(Window):
    def _create(self):
        super()._create()
        contents = QtGui.QWidget(self.control)
        self.control.setCentralWidget(contents)

    def _create_control(self, parent):
        return super()._create_control(parent)


class MyTasksApplication(HasTraits):
    window = Instance(MyApplicationWindow)

    def run(self):
        gui = GUI()
        window = MyApplicationWindow()
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
        gui = GUI()
        gui.invoke_after(100, gui.stop_event_loop)
        gui.start_event_loop()
