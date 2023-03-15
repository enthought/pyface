# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import importlib
from importlib.abc import MetaPathFinder, Loader
import sys


class PyfaceUIQt4Loader(Loader):
    """This loads pyface.ui.qt.* in place of a pyface.ui.qt4.*

    The basic operation is to take the name of the module, replace the
    "qt4" with "qt", load that module, and then add an alias into sys.modules.
    """

    def module_repr(self, module):
        return repr(module)

    def load_module(self, fullname):
        new_name = fullname.replace(".qt4.", ".qt.", 1)
        try:
            module = importlib.import_module(new_name)
        except ImportError:
            ...
        sys.modules[fullname] = module
        return module


class PyfaceUIQt4Finder(MetaPathFinder):
    """MetaPath-based finder for importing pyface.ui.qt4.*

    This matches imports from any path starting with pyface.ui.qt4. and
    returns a loader which will instead load from pyface.ui.qt.*
    """

    def find_module(self, fullname, path=None):
        if fullname.startswith('pyface.ui.qt4.'):
            return PyfaceUIQt4Loader()
