========
Toolkits
========

Pyface is intended to provide a common API on top of distinct GUI backends to
permit the same code to be run on different systems with different GUI
toolkits and produce similar results.  Pyface comes with three built-in
backends in the core library---Qt, WxPython, and a null backend---but provides
hooks for other projects to contribute toolkits and have them be discoverable.

Toolkit Selection
=================

Pyface uses Traits' :py:mod:`traits.etsconfig` to determine the current
toolkit being used.  Applications can control which toolkit to use in two
ways:

- by setting the environment variable ``ETS_TOOLKIT`` to the name of the
  desired toolkit.
- by importing :py:obj:`ETSConfig` and setting its :py:attr:`toolkit`
  attribute appropriately::

    from tratis.etsconfig.api import ETSConfig
    ETSConfig.toolkit = 'qt4'

  This must be done _before_ any widget imports in your application, including
  importing :py:mod:`pyface.api`.  Precisely, this must be set before the
  first import of :py:mod:`pyface.toolkit`.

If for some reason Pyface can't load a deliberately specified toolkit, then it
will raise an exception.

If the toolkit is not specified, Pyface will try to load the ``qt4`` or ``wx``
toolkits, in that order, and then any other toolkits that it knows about
other than ``null``.  If all of those fail, then it will try to load the
``null`` toolkit.

Once selected, the toolkit infrastructure is largely transparent to the
application.

Toolkit Objects
===============

The selection of the correct backend object is carried out by each toolkit's
toolkit object.  For all built-in toolkits, this is an instance of the
:py:class:`pyface.base_toolkit.Toolkit` class, but it is possible that other
backends may use their own objects.  The toolkit object for the toolkit that
has been selected can be found as :py:obj:`pyface.toolkit.toolkit_object`.

This is a callable object which expects to be given an identifier for the
widget in the form of a relative module name and the object name, separated by
a ``':'``.  This is most often used when creating new widget types for Pyface.
The API module for the new widget class typically looks something like this::

    from pyface.toolkit import toolkit_object
    MyWidget = toolkit_object('my_package.my_widget:MyWidget')

The base toolkits use the identifier to select which module to import the
toolkit object by constructing a full module path from the partial path and
importing the object.  For example the ``qt4`` backend will look for the
concrete implementation in :py:mod:`pyface.ui.qt4.my_package.my_widget`
while the ``wx`` backend will look for
:py:mod:`pyface.ui.wx.my_package.my_widget`.

If no matching object is found, the toolkit will return a special
:py:class:`Undefined` class that will raise :py:exception:`NotImplementedError`
when instantiated.

The basic toolkit implementation provides two other features which may be of
use.  It has a trait that gives the name of the toolkit, and it has a list of
packages that it searches when trying to import a toolkit object.  This
second trait provides a hook where an application can insert other packages
into the search path to override the default implementations of a toolkit's
widgets, if needed.

Toolkit Entrypoints
===================

Pyface uses the standard ``importlib_metadata`` "entry point" system to allow
other libraries to contribute new toolkit implementations to Pyface.  The
toolkit selection process discussed above looks for things contributed to the
``pyface.toolkits`` entry point.  These are specified in the ``setup.py`` of
the third party library, something like this::

    setup(
        # ... a bunch of other standard setup.py stuff
        entry_points = {
            'pyface.toolkits': [
                'my_toolkit = my_project.my_toolkit.init:toolkit_object',
            ]
        }
    )

The left-hand side is the name of the toolkit, suitable for use with
:py:obj:`ETSConfig`, and the right-hand side is the location of a toolkit
object which matches the specification above: a callable object which takes
identifiers as specified and returns concrete implementations.  The easiest
way to do this is to follow the examples of the current toolkits and use
a :py:class:`pyface.base_toolkit.Toolkit` instance, but this is not required.
