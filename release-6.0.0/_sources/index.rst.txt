====================================
Welcome to the Pyface Documentation!
====================================

Pyface contains a toolkit-independent GUI abstraction layers, used to support
the "visualization" features of the Traits package. Thus, you can write code
in the abstraction of the PyFace API and the selected toolkit and backend take
care of the details of displaying them.

Pyface
======

Pyface enables programmers to interact with generic GUI objects, such as an
"MDI Application Window", rather than with raw GUI widgets. (Pyface is named by
analogy to JFace in Java.) Traits uses Pyface to implement views and editors
for displaying and editing Traits-based objects.

Toolkit Backends
================

Traits and Pyface define APIs that are independent of any GUI toolkit. However,
in order to actually produce user interfaces with them, you must install a
supported Python-based GUI toolkit and the appropriate toolkit-specific backend
project. Conversely, if you wish to use Traits without a UI, a "null" backend
is automatically used in the absence of a real backend.

Currently, the supported GUI toolkits are

* wxPython (>= 2.8, including experimental support for WxPython 3.0)
* PySide
* PyQt (Qt4 only, but Qt5 support is in development)

While all toolkits funtion with Pyface, integration with wxPython is currently
more complete.  Future development, however, will be more focused on
supporting Qt.

The default toolkit if none is supplied is ``qt4``. This changed from ``wx`` in
Pyface 5.0.

NOTE: Although the code in this library is BSD licensed, when the PyQt backend
is used the more restrictive terms of PyQt's GPL or proprietary licensing will
likely apply to your code.

Toolkit Backend Selection
-------------------------

Selecting the backend to use is possible via the singleton object **ETSConfig**
(importable from `traits.etsconfig.api`), which has a string attribute, toolkit,
that signifies the GUI toolkit.

The supported values of **ETSConfig.toolkit** are:

* 'qt4': `PyQt <http://riverbankcomputing.co.uk/pyqt/>`_, which provides Python
  bindings for the `Qt <http://trolltech.com/products/qt>`_ framework version 4.
* 'wx': `wxPython <http://www.wxpython.org>`_, which provides Python bindings
  for the `wxWidgets <http://wxwidgets.org>`_ toolkit.
* 'null': A do-nothing toolkit, for situations where neither of the other
  toolkits is installed, but Traits is needed for non-UI purposes.

The default behavior of Pyface is to search for available toolkit-specific
packages in the order listed, and uses the first one it finds. The programmer or
the user can override this behavior in any of several ways, in the following
order of precedence:

#. The program can explicitly set **ETSConfig.toolkit**. It must do this before
   importing from any other Enthought Tool Suite component, including
   traits.  For example, at the beginning of a program::

       from traits.etsconfig.api import ETSConfig
       ETSConfig.toolkit = 'wx'

#. The user can define a value for the ETS_TOOLKIT environment variable.

Contents
========

.. toctree::
   :maxdepth: 2

   Overview <overview>
   Toolkits <toolkits>
   API Documentation <api/pyface>
   Change Log <changelog>
