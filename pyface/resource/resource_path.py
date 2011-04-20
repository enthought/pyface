#------------------------------------------------------------------------------
# Copyright (c) 2005-2009 Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#------------------------------------------------------------------------------
""" Functions to determine resource locations from the call stack.

This type of resource location is normally requested from the constructor for
an object whose resources are relative to the module constructing the object.

"""

import sys

from os import getcwd
from os.path import dirname, exists


def resource_module(level = 2):
    """Return a module reference calculated from the caller's stack.

    Note that what we want is the reference to the package containing the
    module in the stack.  This is because we need a directory to search
    for our default resource sub-dirs as children.

    """
    module_name = sys._getframe(level).f_globals.get('__name__', '__main__')
    if '.' in module_name:
        module_name = '.'.join(module_name.split('.')[:-1])
    module = sys.modules.get(module_name)

    return module


def resource_path(level = 2):
    """Return a resource path calculated from the caller's stack.

    """
    module = sys._getframe(level).f_globals.get('__name__', '__main__')

    if module != '__main__':
        # Return the path to the module:
        try:
            return dirname(getattr(sys.modules.get(module), '__file__'))
        except:
            # Apparently 'module' is not a registered module...treat it like
            # '__main__':
            pass

    # '__main__' is not a real module, so we need a work around:
    for path in [ dirname(sys.argv[0] ), getcwd()]:
        if exists(path):
            break

    return path

#### EOF ######################################################################
