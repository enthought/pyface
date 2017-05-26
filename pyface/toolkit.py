#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# Copyright (c) 2015-2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
"""
This module provides the toolkit object for the current backend toolkit

When first imported this module will use the 'pyface.toolkit' entry points
from pkg_resources to load a plugin according to the following strategy:

- if ETSConfig.toolkit is set, try to load a plugin with a matching name.
  If it succeeds, we are good, and if it fails then we error out.
- if ETSConfig.toolkit is not set, we try to load the 'qt4' and 'wx' plugins
  in that order, and on success we consider ourselves good.  The
  ETSConfig.toolkit gets set appropriately.
- after that, we try every 'pyface.toolkit' plugin we can find except 'null'
  in an arbitrary order.  If one succeeds, we consider ourselves good, and
  set the ETSConfig.toolkit appropriately.
- after that, try the 'null' plugin.
- finally, if all else fails, we try to directly import the null backend's
  toolkit object.
"""

import logging

import pkg_resources

from traits.etsconfig.api import ETSConfig


logger = logging.getLogger(__name__)


try:
    provisional_toolkit = ETSConfig.provisional_toolkit
except AttributeError:
    from contextlib import contextmanager

    # for backward compatibility
    @contextmanager
    def provisional_toolkit(toolkit_name):
        """ Perform an operation with toolkit provisionally set

        This sets the toolkit attribute of the ETSConfig object set to the
        provided value. If the operation fails with an exception, the toolkit
        is reset to nothing.
        """
        if ETSConfig.toolkit:
            raise AttributeError("ETSConfig toolkit is already set")
        ETSConfig.toolkit = toolkit_name
        try:
            yield
        except:
            # reset the toolkit state
            ETSConfig._toolkit = ''
            raise


def _init_toolkit():
    """ Initialise a toolkit, if possible. """

    def import_toolkit(tk):
        plugins = list(pkg_resources.iter_entry_points('pyface.toolkits', tk))
        if len(plugins) == 0:
            msg = "no Pyface plugin found for toolkit '{}'"
            raise RuntimeError(msg.format(tk))
        elif len(plugins) > 1:
            msg = ("multiple Pyface plugins found for toolkit %r: %s")
            modules = ', '.join(plugin.module_name for plugin in plugins)
            logger.warning(msg, tk, modules)

        exception = None
        while plugins:
            plugin = plugins.pop(0)
            try:
                tk_object = plugin.load()
                return tk_object
            except ImportError as exception:
                logger.exception(exception)
                msg = "Could not load plugin %r from %r"
                logger.warning(msg, plugin.name, plugin.module_name)
        else:
            # no success
            if exception is not None:
                raise exception
            else:
                raise RuntimeError("No toolkit loaded or exception raised.")

    # Get the toolkit.
    if ETSConfig.toolkit:
        return import_toolkit(ETSConfig.toolkit)

    # Try known toolkits first.
    for tk in ('qt4', 'wx'):
        try:
            with provisional_toolkit(tk):
                return import_toolkit(tk)
        except RuntimeError as exc:
            exc_info = logger.getEffectiveLevel() <= logging.INFO
            level = logger.ERROR if exc_info else logging.INFO
            msg = "Could not import Pyface backend %r"
            logger.log(level, msg, tk, excinfo=exc_info)

    # Try all non-null plugins we can find until success.
    for plugin in pkg_resources.iter_entry_points('pyface.toolkits'):
        if plugin.name == 'null':
            continue
        try:
            with provisional_toolkit(plugin.name):
                return plugin.load()
        except ImportError as exc:
            logger.exception(exc)
            msg = "Could not load plugin %r from %r"
            logger.warning(msg, plugin.name, plugin.module_name)

    # Try to import the null toolkit properly
    try:
        with provisional_toolkit('null'):
            return import_toolkit('null')
    except RuntimeError as exc:
        if logger.getEffectiveLevel() <= logging.INFO:
            logger.exception(exc)
        logger.info("Could not import Pyface backend 'null'")
    except ImportError:
        logger.info("Could not import Pyface backend 'null'")

    try:
        from pyface.ui.null.init import toolkit_object
        return toolkit_object
    except ImportError as exc:
        logger.exception(exc)
        raise ImportError("Unable to import a pyface backend for any toolkit")

    # if everything else fails toolkit is None
    return None


# The toolkit object function.
toolkit_object = _init_toolkit()
