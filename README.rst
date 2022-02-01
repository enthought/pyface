==========================================
Pyface: Traits-capable Windowing Framework
==========================================

The Pyface project contains a toolkit-independent GUI abstraction layer,
which is used to support the "visualization" features of the Traits package.
Thus, you can write code in terms of the Traits API (views, items, editors,
etc.), and let Pyface and your selected toolkit and back-end take care of
the details of displaying them.

The following GUI backends are supported:

- PySide2 (stable) and PySide6 (experimental)
- PyQt5 (stable) and PyQt6 (in development)
- wxPython 4 (experimental)

Installation
------------

GUI backends are marked as optional dependencies of Pyface. Some features
or infrastructures may also require additional dependencies.

To install with PySide2 dependencies::

    $ pip install pyface[pyside2]

To install with PySide6 dependencies (experimental)::

    $ pip install pyface[pyside6]

To install with PyQt5 dependencies::

    $ pip install pyface[pyqt5]

To install with wxPython4 dependencies (experimental)::

    $ pip install pyface[wx]

``pillow`` is an optional dependency for the PILImage class::

    $ pip install pyface[pillow]

To install with additional test dependencies::

    $ pip install pyface[test]

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
are licensed with other licenses. See the license files for further
information.
