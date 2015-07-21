==========================================
pyface: traits-capable windowing framework
==========================================

The pyface project contains a toolkit-independent GUI abstraction layer,
which is used to support the "visualization" features of the Traits package.
Thus, you can write code in terms of the Traits API (views, items, editors,
etc.), and let pyface and your selected toolkit and back-end take care of
the details of displaying them.

The following GUI backends are supported:

- wxPython
- PyQt
- PySide

Documentation
-------------

* `Online Documentation <http://docs.enthought.com/pyface/>`_.

* `API Documentation <http://docs.enthought.com/pyface/api/pyface.html>`_.

Prerequisites
-------------

Pyface depends on:

* a GUI toolkit: one of PySide, PyQt or WxPython

* `Traits <https://github.com/enthought/traits>`_

* some widgets may have additional optional dependencies.  For example, the
  IPython shell widgets require IPython to be installed.
