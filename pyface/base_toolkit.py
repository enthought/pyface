# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Common toolkit loading utilities and classes

This module provides common code for ETS packages that need to do GUI toolkit
discovery and loading.  The common patterns that ETS has settled on are that
where different GUI toolkits require alternative implementations of features
the toolkit is expected to provide a callable object which takes a relative
module path and an object name, separated by a colon and return the toolkit's
implementation of that object (usually this is a class, but it could be
anything).  The assumption is that this is implemented by objects in
sub-modules of the toolkit, but plugin authors are free to use whatever methods
they like.

Which toolkit to use is specified via the :py:mod:`traits.etsconfig.etsconfig`
package, but if this is not explicitly set by an application at startup or via
environment variables, there needs to be a way of discovering and loading any
available working toolkit implementations.  The default mechanism is via the
now-standard :py:mod:`importlib_metadata` and :py:mod:`setuptools`
"entry point" system.

This module provides three things:

- a function :py:func:`import_toolkit` that attempts to find and load a toolkit
  entry point for a specified toolkit name

- a function :py:func:`find_toolkit` that attempts to find a toolkit entry
  point that works

- a class :py:class:`Toolkit` class that implements the standard logic for
  finding toolkit objects.

These are done in a library-agnostic way so that the same tools can be used
not just for different pyface backends, but also for TraitsUI and ETS
libraries where we need to switch between different GUI toolkit
implementations.

Note that there is no requirement for new toolkit implementations to use this
:py:class:`Toolkit` implementation, but they should be compatible with it.

Default toolkit loading logic
-----------------------------

The :py:func:`find_toolkit` function uses the following logic when attempting
to load toolkits:

- if ETSConfig.toolkit is set, try to load a plugin with a matching name.
  If it succeeds, we are good, and if it fails then we error out.

- after that, we try every 'pyface.toolkit' plugin we can find.  If one
  succeeds, we consider ourselves good, and set the ETSConfig.toolkit
  appropriately.  The order is configurable, and by default will try to load
  the `qt` toolkit first, `wx` next, then all others in arbitrary order,
  and `null` last.

- finally, if all else fails, we try to load the null toolkit.
"""

import logging
import os
import sys

try:
    # Starting Python 3.8, importlib.metadata is available in the Python
    # standard library and starting Python 3.10, the "select" interface is
    # available on EntryPoints.
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata

from traits.api import HasTraits, List, ReadOnly, Str
from traits.etsconfig.api import ETSConfig

logger = logging.getLogger(__name__)


TOOLKIT_PRIORITIES = {"qt": -2, "wx": -1, "null": float("inf")}
default_priorities = lambda plugin: TOOLKIT_PRIORITIES.get(plugin.name, 0)


class Toolkit(HasTraits):
    """ A basic toolkit implementation for use by specific toolkits.

    This implementation uses pathname mangling to find modules and objects in
    those modules.  If an object can't be found, the toolkit will return a
    class that raises NotImplementedError when it is instantiated.
    """

    #: The name of the package (eg. pyface)
    package = ReadOnly

    #: The name of the toolkit
    toolkit = ReadOnly

    #: The packages to look in for implementations.
    packages = List(Str)

    def __init__(self, package, toolkit, *packages, **traits):
        super().__init__(
            package=package, toolkit=toolkit, packages=list(packages), **traits
        )

    def __call__(self, name):
        """ Return the toolkit specific object with the given name.

        Parameters
        ----------
        name : str
            The name consists of the relative module path and the object name
            separated by a colon.
        """
        from importlib import import_module

        mname, oname = name.split(":")
        if not mname.startswith("."):
            mname = "." + mname

        for package in self.packages:
            try:
                module = import_module(mname, package)
            except ImportError as exc:
                # is the error while trying to import package mname or not?
                if all(
                    part not in exc.args[0]
                    for part in mname.split(".")
                    if part
                ):
                    # something else went wrong - let the exception be raised
                    raise

                # Ignore *ANY* errors unless a debug ENV variable is set.
                if "ETS_DEBUG" in os.environ:
                    # Attempt to only skip errors in importing the backend modules.
                    # The idea here is that this only happens when the last entry in
                    # the traceback's stack frame mentions the toolkit in question.
                    import traceback

                    frames = traceback.extract_tb(sys.exc_info()[2])
                    filename, lineno, function, text = frames[-1]
                    if package not in filename:
                        raise
            else:
                obj = getattr(module, oname, None)
                if obj is not None:
                    return obj

        toolkit = self.toolkit

        class Unimplemented(object):
            """ An unimplemented toolkit object

            This is returned if an object isn't implemented by the selected
            toolkit.  It raises an exception if it is ever instantiated.
            """

            def __init__(self, *args, **kwargs):
                msg = "the %s %s backend doesn't implement %s"
                raise NotImplementedError(msg % (toolkit, package, name))

        return Unimplemented


def import_toolkit(toolkit_name, entry_point="pyface.toolkits"):
    """ Attempt to import an toolkit specified by an entry point.

    Parameters
    ----------
    toolkit_name : str
        The name of the toolkit we would like to load.
    entry_point : str
        The name of the entry point that holds our toolkits.

    Returns
    -------
    toolkit_object : Callable
        A callable object that implements the Toolkit interface.

    Raises
    ------
    RuntimeError
        If no toolkit is found, or if the toolkit cannot be loaded for some
        reason.
    """

    # This compatibility layer can be removed when we drop support for
    # Python < 3.10. Ref https://github.com/enthought/pyface/issues/999.
    all_entry_points = importlib_metadata.entry_points()
    if hasattr(all_entry_points, "select"):
        entry_point_group = all_entry_points.select(group=entry_point)
    else:
        entry_point_group = all_entry_points[entry_point]

    plugins = [
        plugin for plugin in entry_point_group if plugin.name == toolkit_name
    ]
    if len(plugins) == 0:
        msg = "No {} plugin found for toolkit {}"
        msg = msg.format(entry_point, toolkit_name)
        logger.debug(msg)
        raise RuntimeError(msg)
    elif len(plugins) > 1:
        msg = "multiple %r plugins found for toolkit %r: %s"
        module_names = []
        for plugin in plugins:
            module_names.append(plugin.value.split(":")[0])
        module_names = ", ".join(module_names)
        logger.warning(msg, entry_point, toolkit_name, module_names)

    toolkit_exception = None
    for plugin in plugins:
        try:
            toolkit_object = plugin.load()
            return toolkit_object
        except (ImportError, AttributeError) as exc:
            msg = "Could not load plugin %r from %r"
            module_name = plugin.value.split(":")[0]
            logger.info(msg, plugin.name, module_name)
            logger.debug(exc, exc_info=True)
            toolkit_exception = exc

    msg = "No {} plugin could be loaded for {}"
    msg = msg.format(entry_point, toolkit_name)
    logger.info(msg)
    raise RuntimeError(msg) from toolkit_exception


def find_toolkit(
    entry_point="pyface.toolkits",
    toolkits=None,
    priorities=default_priorities,
):
    """ Find a toolkit that works.

    If ETSConfig is set, then attempt to find a matching toolkit.  Otherwise
    try every plugin for the entry_point until one works.  The ordering of the
    plugins is supplied via the priorities function which should be suitable
    for use as a sorting key function.  If all else fails, explicitly try to
    load the "null" toolkit backend.  If that fails, give up.

    Parameters
    ----------
    entry_point : str
        The name of the entry point that holds our toolkits.
    toolkits : collection of strings
        Only consider toolkits which match the given strings, ignore other
        ones.
    priorities : Callable
        A callable function that returns an priority for each plugin.

    Returns
    -------
    toolkit : Toolkit
        A callable object that implements the Toolkit interface.

    Raises
    ------
    RuntimeError
        If no ETSConfig.toolkit is set but the toolkit cannot be loaded for
        some reason.
    """
    if ETSConfig.toolkit:
        return import_toolkit(ETSConfig.toolkit, entry_point)

    # This compatibility layer can be removed when we drop support for
    # Python < 3.10. Ref https://github.com/enthought/pyface/issues/999.
    all_entry_points = importlib_metadata.entry_points()
    if hasattr(all_entry_points, "select"):
        entry_points = [
            plugin for plugin in all_entry_points.select(group=entry_point)
            if toolkits is None or plugin.name in toolkits
        ]
    else:
        entry_points = [
            plugin for plugin in all_entry_points[entry_point]
            if toolkits is None or plugin.name in toolkits
        ]

    for plugin in sorted(entry_points, key=priorities):
        try:
            with ETSConfig.provisional_toolkit(plugin.name):
                toolkit = plugin.load()
                return toolkit
        except (ImportError, AttributeError, RuntimeError) as exc:
            msg = "Could not load %s plugin %r from %r"
            module_name = plugin.value.split(":")[0]
            logger.info(msg, entry_point, plugin.name, module_name)
            logger.debug(exc, exc_info=True)

    # if all else fails, try to import the null toolkit.
    with ETSConfig.provisional_toolkit("null"):
        return import_toolkit("null", entry_point)
