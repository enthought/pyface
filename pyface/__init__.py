# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Reusable MVC-based components for Traits-based applications.
    Part of the TraitsGUI project of the Enthought Tool Suite.
"""

try:
    from pyface._version import full_version as __version__
except ImportError:
    __version__ = "not-built"


__requires__ = ["traits"]
__extras_require__ = {
    "wx": ["wxpython>=4", "numpy"],
    "pyqt": ["pyqt>=4.10", "pygments"],
    "pyqt5": ["pyqt>=5", "pygments"],
    "pyside": ["pyside>=1.2", "pygments"],
}
