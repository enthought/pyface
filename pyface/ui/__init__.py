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


# Import hooks for loading pyface.ui.qt.* in place of a pyface.ui.qt4.*
# This is just the implementation, it is not connected in this module, but
# is available for applications which want to install it themselves.
# It is here rather than in pyface.ui.qt4 so it can be imported and used
# without generating the warnings from pyface.ui.qt4
#
# To use manually:
#
#     import sys
#     sys.meta_path.append(PyfaceUIQt4Finder())

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
        except ModuleNotFoundError as exc:
            # give better feedback about import failure
            if exc.name == new_name:
                raise ModuleNotFoundError(
                    f"No module named {fullname!r}",
                    name=fullname,
                    path=exc.path,
                )
            else:
                raise
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
