
# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Utilities for handling optional import dependencies."""

import contextlib
import logging


_PYFACE_LOGGER = logging.getLogger("pyface")


@contextlib.contextmanager
def optional_import(dependency_name, msg):
    """ Context manager for capturing ImportError for a particular optional
    dependency. If such an error occurs, it will be silenced and a debug
    message will be logged.

    Parameters
    ----------
    dependency_name : str
        Name of the module that may fail to be imported.
        If matched, the ImportError will be silenced
    msg : str
        Log message to be emitted.
    """
    try:
        yield
    except ImportError as exception:
        if exception.name == dependency_name:
            _PYFACE_LOGGER.debug(msg, exc_info=True)
        else:
            raise
