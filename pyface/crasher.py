"""
The script below segfaults for me around 10% of the time with:

- Ubuntu 22.04
- Python 3.10 (Ubuntu package)
- PySide 6.3.2 (installed via pip)

To reproduce:

- Save this script under the name 'crasher.py'
- Create and activate a Python 3.10 venv with e.g.

    python -m venv --clear crasher
    source crasher/bin/activate

- Install pyface and PySide6 < 6.4 from PyPI:

    python -m pip install pyface "PySide6<6.4"

- Run this script under unittest:

    python -m unittest crasher

"""

import unittest

from pyface.gui import GUI
from pyface.api import ApplicationWindow
from traits.api import HasTraits, Instance


class MyTasksApplication(HasTraits):
    window = Instance(ApplicationWindow)

    def run(self):
        gui = GUI()
        window = ApplicationWindow()
        window.open()
        self.window = window
        gui.invoke_later(self.exit)
        gui.start_event_loop()

    def exit(self):
        window = self.window
        self.window = None
        window.close()
        window.destroy()
        #window.closed = True



class TestTasksApplication(unittest.TestCase):
    def test_lifecycle(self):
        app = MyTasksApplication()
        app.run()

        # Run the event loop
        gui = GUI()
        gui.invoke_after(100, gui.stop_event_loop)
        gui.start_event_loop()
