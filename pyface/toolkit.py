#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
#------------------------------------------------------------------------------

# Standard library imports.
import os
import sys
import logging

# Enthought library imports.
from traits.etsconfig.api import ETSConfig

logger = logging.getLogger(__name__)

# This is set to the root part of the module path for the selected backend.
_toolkit_backend = None


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
    """ Initialise the current toolkit. """

    def import_toolkit(tk):
        try:
            # Try and import the toolkit's pyface backend init module.
            be = 'pyface.ui.%s.' % tk
            __import__(be + 'init')
        except:
            raise
        return be

    # Get the toolkit.
    if ETSConfig.toolkit:
        be = import_toolkit(ETSConfig.toolkit)
    else:
        # Toolkits to check for if none is explicitly specified.
        known_toolkits = ('qt4', 'wx', 'null')

        for tk in known_toolkits:
            try:
                with provisional_toolkit(tk):
                    be = import_toolkit(tk)
                break
            except ImportError as exc:
                msg = "Could not import Pyface backend '{0}'"
                logger.info(msg.format(tk))
                if logger.getEffectiveLevel() <= logging.INFO:
                    logger.exception(exc)
        else:
            # Try to import the null toolkit but don't set the ETSConfig toolkit
            try:
                be = import_toolkit('null')
                import warnings
                msg = ("Unable to import the '{0}' backend for pyface; " +
                       "using the 'null' backend instead.")
                warnings.warn(msg.format(toolkit_name), RuntimeWarning)
            except ImportError as exc:
                logger.exception(exc)
                raise ImportError("Unable to import a pyface backend for any "
                    "of the %s toolkits" % ", ".join(known_toolkits))

    # Save the imported toolkit module.
    global _toolkit_backend
    _toolkit_backend = be


# Do this once then disappear.
_init_toolkit()
del _init_toolkit


def toolkit_object(name):
    """ Return the toolkit specific object with the given name.

    Parameters
    ----------
    name : str
        The name consists of the relative module path and the object name
        separated by a colon.
    """

    mname, oname = name.split(':')
    be_mname = _toolkit_backend + mname

    class Unimplemented(object):
        """ An unimplemented toolkit object

        This is returned if an object isn't implemented by the selected
        toolkit.  It raises an exception if it is ever instantiated.
        """

        def __init__(self, *args, **kwargs):
            raise NotImplementedError("the %s pyface backend doesn't implement %s" % (ETSConfig.toolkit, oname))

    be_obj = Unimplemented

    try:
        __import__(be_mname)

        try:
            be_obj = getattr(sys.modules[be_mname], oname)
        except AttributeError:
            pass
    except ImportError as exc:
        # is the error while trying to import be_mname or not?
        if all(part not in exc.args[0] for part in mname.split('.')):
                # something else went wrong - let the exception be raised
                raise

        # Ignore *ANY* errors unless a debug ENV variable is set.
        if 'ETS_DEBUG' in os.environ:

            # Attempt to only skip errors in importing the backend modules.
            # The idea here is that this only happens when the last entry in
            # the traceback's stack frame mentions the toolkit in question.
            import traceback
            frames = traceback.extract_tb(sys.exc_traceback)
            filename, lineno, function, text = frames[-1]
            if not _toolkit_backend in filename:
                raise

    return be_obj
