====================================
Welcome to the Pyface Documentation!
====================================

Pyface contains toolkit-independent GUI abstraction layers, used to support
the TraitsUI package. Thus, you can write code in the abstraction of the
Pyface API and the selected toolkit and backend take care of the details of
displaying them.

Pyface
======

Pyface enables programmers to interact with generic GUI objects, such as an
"MDI Application Window", rather than with raw GUI widgets. (Pyface is named by
analogy to JFace in Java.) TraitsUI uses Pyface to implement views and editors
for displaying and editing Traits-based objects.

Toolkit Backends
================

TraitsUI and Pyface define APIs that are independent of any GUI toolkit.
However, in order to actually produce user interfaces with them, you must
install a supported Python-based GUI toolkit and the appropriate
toolkit-specific backend project. Conversely, a "null" backend is
automatically used in the absence of a real backend.

Currently, the GUI toolkits are

* PySide2 and PySide6 (stable)
* PyQt5 (stable) and PyQt6 (in development)
* wxPython 4 (experimental)

NOTE: Although the code in this library is BSD licensed, when a PyQt backend
is used, the more restrictive terms of PyQt's GPL or proprietary licensing
will likely apply to your code.

Toolkit Backend Selection
-------------------------

Selecting the backend to use is possible via the singleton object **ETSConfig**
(importable from `traits.etsconfig.api`), which has a string attribute, toolkit,
that signifies the GUI toolkit.

The supported values of **ETSConfig.toolkit** are:

* ``'qt'`` or ``'qt4'``: PySide2, PySide6 or `PyQt <http://riverbankcomputing.co.uk/pyqt/>`_,
  which provide Python bindings for the `Qt <http://www.qt.io>`_ framework.
  Note that selecting ``qt4`` will turn on the backwards-compatibility for the
  :py:mod:`pyface.ui.qt4` sub-package (see below) but is otherwise not
  preferred in new code and will eventually be removed.
* ``'wx'``: `wxPython 4 <http://www.wxpython.org>`_, which provides Python bindings
  for the `wxWidgets <http://wxwidgets.org>`_ toolkit.
* ``'null'``: A do-nothing toolkit, for situations where neither of the other
  toolkits is installed.

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

Backwards Compatibility With ``pyface.ui.qt4``
----------------------------------------------

In Pyface 8.0 the :py:mod:`pyface.ui.qt4` sub-package was renamed to
:py:mod:`pyface.ui.qt`.  While most code does not import directly from
:py:mod:`pyface.ui.qt4` it is possible that there is some advanced code that
does use this namespace in downstream projects.  Pyface 8.0 contains backwards
compatible code for this namespace which is turned off by default, but can be
activated in a number of ways:

* by setting the ``ETS_QT4_IMPORTS`` environment variable to a non-empty value.
  This allows end-users of applications built to activate this code.
* by using the ``'qt4'`` for the ``ETS_TOOLKIT`` or ``ETSConfig.toolkit``.
* by explicitly registering a ``qt4`` :py:class:`~pyface.ui.ShadowModuleFinder`
  in :py:obj:`sys.meta_path` (advanced)

This backwards compatibility code will be removed in a future Pyface version.

Contents
========

.. toctree::
   :maxdepth: 3

   Overview <overview>
   Toolkits <toolkits>
   Widgets <widgets>
   Pyface Applications <applications>
   Pyface Trait Types <traits>
   Images in Pyface <image_types>
   Standard Dialogs <standard_dialogs>
   Submodules <submodules>
   Testing <testing>
   API Documentation <api/pyface>
   Change Log <changelog>
