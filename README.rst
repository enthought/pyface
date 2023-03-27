==========================================
Pyface: Traits-capable Windowing Framework
==========================================

The Pyface project contains a toolkit-independent GUI abstraction layer,
which wraps an underlying GUI toolkit with classes that integrate with the
`Traits <docs.enthought.com/traits>`_ framework so that changes in the
underlying GUI widgets are reflected by in changes in the wrapped traits.

The following GUI backends are supported:

- PySide2 (stable) and PySide6 (experimental)
- PyQt5 (stable) and PyQt6 (in development)
- wxPython 4 (experimental)

Installation
------------

GUI backends are marked as optional dependencies of Pyface. Some features
or infrastructures may also require additional dependencies.

To install with PySide2 dependencies::

    $ pip install "pyface[pyside2]"

To install with PySide6 dependencies (experimental)::

    $ pip install "pyface[pyside6]"

To install with PyQt5 dependencies::

    $ pip install "pyface[pyqt5]"

To install with wxPython4 dependencies (experimental)::

    $ pip install "pyface[wx]"

In addition, to run examples you will want add the ``examples`` dependencies::

    $ pip install "pyface[examples]"

To install with additional ``test`` dependencies::

    $ pip install "pyface[test]"

To install with additional ``doc`` dependencies::

    $ pip install "pyface[doc]"

There are additional optional dependencies on ``numpy`` and ``pillow`` for
certain image types.

Example
-------

The following code creates a window with a simple Python shell widget::

    from pyface.api import ApplicationWindow, GUIApplication, PythonShell
    from traits.api import Instance

    class PythonShellWindow(ApplicationWindow):

        title = "Python Shell"

        shell = Instance(PythonShell)

        def _create_contents(self, parent):
            self.shell = PythonShell(parent)
            self.shell.create()
            return self.shell.control

        def destroy(self):
            if self.shell is not None:
                self.shell.destroy()
            super().destroy()

    def create_app_window(application, **kwargs):
        return PythonShellWindow()

    app = GUIApplication(
        name="PythonShell",
        window_factory=create_app_window
    )

    app.run()

More complete examples with menus, toolbars and so forth can be found in the
examples.

Documentation
-------------

* `Online Documentation <http://docs.enthought.com/pyface/>`_.

* `API Documentation <http://docs.enthought.com/pyface/api/pyface.html>`_.

Prerequisites
-------------

Pyface depends on:

* `Traits <https://github.com/enthought/traits>`_

* a GUI toolkit as described above

* Pygments for syntax highlighting in the Qt code editor widget.

* some widgets may have additional optional dependencies such as NumPy or
  Pillow.

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
and icons are licensed with other licenses. See the image_LICENSE.txt file for
further information.
