==========================================
pyface: traits-capable windowing framework
==========================================

.. image:: https://travis-ci.org/enthought/pyface.svg?branch=master
    :target: https://travis-ci.org/enthought/pyface

.. image:: https://ci.appveyor.com/api/projects/status/68nfb049cdq9wqd1/branch/master?svg=true
    :target: https://ci.appveyor.com/project/EnthoughtOSS/pyface/branch/master

.. image:: https://codecov.io/github/enthought/pyface/coverage.svg?branch=master
    :target: https://codecov.io/github/enthought/pyface?branch=master


The pyface project contains a toolkit-independent GUI abstraction layer,
which is used to support the "visualization" features of the Traits package.
Thus, you can write code in terms of the Traits API (views, items, editors,
etc.), and let pyface and your selected toolkit and back-end take care of
the details of displaying them.

The following GUI backends are supported:

- wxPython
- PyQt
- PySide

**Warning:** The default toolkit if none is supplied is ``qt4``.
   This changed from ``wx`` in Pyface 5.0..

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
