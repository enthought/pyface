==========================================
Pyface: Traits-capable Windowing Framework
==========================================

The Pyface project contains a toolkit-independent GUI abstraction layer,
which is used to support the "visualization" features of the Enthought Tool
Suite libraries.  Pyface contains Traits-aware wrappers of standard GUI
elements such as Windows, Dialogs and Fields, together with the "Tasks"
application framework which provides a rich GUI experience with dock panes,
tabbed editors, and so forth.  This permits you to write cross-platform
interactive GUI code without needing to use the underlying GUI backend.

The following GUI backends are supported:

- PySide2 (stable) and PySide6 (experimental)
- PyQt5 (stable) and PyQt6 (in development)
- wxPython 4 (experimental)

Example
-------

The following code creates a window with a simple Python shell:

..  code-block:: python

    from pyface.api import ApplicationWindow, GUI, IPythonShell

    class MainWindow(ApplicationWindow):
        """ The main application window. """

        #: The PythonShell that forms the contents of the window
        shell = Instance(IPythonShell, allow_none=False)

        def _create_contents(self, parent):
            """ Create the editor. """
            self.shell.create(parent)
            return self.shell.control

        def destroy(self):
            self.shell.destroy()
            super().destroy()

        def _shell_default(self):
            from pyface.api import PythonShell
            return PythonShell()

    # Application entry point.
    if __name__ == "__main__":
        # Create the GUI.
        gui = GUI()

        # Create and open the main window.
        window = MainWindow(title="Python Shell", size=(640, 480))
        window.open()

        # Start the GUI event loop!
        gui.start_event_loop()

..  image:: https://raw.github.com/enthought/pyface/main/shell_window.png
    :alt: A Pyface GUI window containing a Python shell.

Installation
------------

Pyface is a pure Python package.  In most cases Pyface will be installable
using a simple ``pip install`` command.

To install with a backend, choose one of the following, as appropriate:

..  code-block:: console

    $ pip install pyface[pyside2]

    $ pip install pyface[pyside6]

    $ pip install pyface[pyqt5]

    $ pip install pyface[wx]

Some optional functionality uses ``pillow`` and ``numpy`` and these can be
installed using optional dependencies:

..  code-block:: console

    $ pip install pyface[pillow]

    $ pip install pyface[numpy]

For running tests a few more packages are required:

..  code-block:: console

    $ pip install pyface[test]

Documentation
-------------

* `Online Documentation <http://docs.enthought.com/pyface/>`_.

* `API Documentation <http://docs.enthought.com/pyface/api/pyface.html>`_.

.. end_of_long_description

Developing Pyface
-----------------

The `etstool.py` script provides utilities to assist developers wanting to work
on Pyface.  To use it, you will need to have the source checked out via Git,
Enthought's `EDM <http://docs.enthought.com/edm/>`__ distribution manager, and
a minimal environment containing at least the
`Click <http://click.pocoo.org/>`__ library.

You can then follow the instructions in ``etstool.py``.  In particular:

- use `etstool.py install` to create environments for particular toolkits and
  runtimes
- use `etstool.py shell` to activate those environments
- use `etstool.py test` to run the tests in those environments
- use `etstool.py flake8` to perform style checks
- use `etstool.py docs` to build the documentation
- use `etstool.py test-all` to run the tests across all supported runtimes and toolkits

License
-------

Pyface source code is licensed with a BSD-style license.  Some default images
are licensed with other licenses. See the license files for further
information.
