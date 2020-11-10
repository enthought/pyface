==========================================
Pyface: Traits-capable Windowing Framework
==========================================

.. image:: https://travis-ci.org/enthought/pyface.svg?branch=master
    :target: https://travis-ci.org/enthought/pyface

.. image:: https://ci.appveyor.com/api/projects/status/68nfb049cdq9wqd1/branch/master?svg=true
    :target: https://ci.appveyor.com/project/EnthoughtOSS/pyface/branch/master

.. image:: https://codecov.io/github/enthought/pyface/coverage.svg?branch=master
    :target: https://codecov.io/github/enthought/pyface?branch=master


The Pyface project contains a toolkit-independent GUI abstraction layer,
which is used to support the "visualization" features of the Traits package.
Thus, you can write code in terms of the Traits API (views, items, editors,
etc.), and let Pyface and your selected toolkit and back-end take care of
the details of displaying them.

The following GUI backends are supported:

- PyQt 4 and 5
- PySide2
- wxPython 4 (experimental)

Installation
------------

GUI backends are marked as optional dependencies of Pyface. Some features
or infrastructures may also require additional dependencies.

To install with PySide2 dependencies::

    $ pip install pyface[pyside2]

To install with PyQt5 dependencies::

    $ pip install pyface[pyqt5]

To install with wxPython4 dependencies (experimental)::

    $ pip install pyface[wx]

To install with additional test dependencies::

    $ pip install pyface[test]

Documentation
-------------

* `Online Documentation <http://docs.enthought.com/pyface/>`_.

* `API Documentation <http://docs.enthought.com/pyface/api/pyface.html>`_.

Prerequisites
-------------

Pyface depends on:

* a GUI toolkit: one of PySide, PyQt or WxPython

* `Traits <https://github.com/enthought/traits>`_

* Pygments for syntax highlighting in the Qt code editor widget.

* some widgets may have additional optional dependencies.

.. end_of_long_description

Running the Test Suite
----------------------

To run the test suite, you will need to install Git and
`EDM <http://docs.enthought.com/edm/>`__ as well as have a Python environment
which has install `Click <http://click.pocoo.org/>`__ available. You can then
follow the instructions in ``etstool.py``.  In particular::

    > python etstool.py test-all

will run tests in all supported environments automatically.
