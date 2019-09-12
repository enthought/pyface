# Copyright (c) 2019, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" Toolkit-specific utilities. """

# Import the toolkit specific version.
from __future__ import absolute_import

from pyface.qt import is_pyqt


# ----------------------------------------------------------------------------
# Toolkit utility functions
# ----------------------------------------------------------------------------

def destroy_later(control):
    """ Schedule a toolkit control for later destruction.

    Parameters
    ----------
    control : QObject subclass
        The object that is to be destroyed.
    """
    control.deleteLater()


def is_destroyed(control):
    """ Checks if a control has had the underlying C++ object destroyed.

    Parameters
    ----------
    control : QObject subclass
        The control that is being tested.
    """
    if is_pyqt:
        import sip
        return sip.isdeleted(control)
    else:
        import shiboken
        return not shiboken.isValid(control)
