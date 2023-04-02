# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Functions to determine resource locations from the call stack.

This type of resource location is normally requested from the constructor for
an object whose resources are relative to the module constructing the object.

"""

import sys

from traits.trait_base import get_resource_path


def resource_module(level=2):
    """Return a module reference calculated from the caller's stack.

    Note that what we want is the reference to the package containing the
    module in the stack.  This is because we need a directory to search
    for our default resource sub-dirs as children.

    """
    module_name = sys._getframe(level).f_globals.get("__name__", "__main__")
    if "." in module_name:
        module_name = ".".join(module_name.split(".")[:-1])
    module = sys.modules.get(module_name)

    return module


def resource_path(level=2):
    """Return a resource path calculated from the caller's stack.

    """
    return get_resource_path(level + 1)
