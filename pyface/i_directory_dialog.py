#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" The interface for a dialog that allows the user to browse for a directory.
"""


# Enthought library imports.
from traits.api import Bool, Unicode

# Local imports.
from pyface.i_dialog import IDialog


class IDirectoryDialog(IDialog):
    """ The interface for a dialog that allows the user to browse for a
    directory.
    """

    #### 'IDirectoryDialog' interface #########################################

    #: The default path.  The default (ie. the default default path) is toolkit
    #: specific.
    # FIXME v3: The default should be the current directory.  (It seems wx is
    # the problem, although the file dialog does the right thing.)
    default_path = Unicode

    #: The message to display in the dialog.  The default is toolkit specific.
    message = Unicode

    #: True iff the dialog should include a button that allows the user to
    #: create a new directory.
    new_directory = Bool(True)

    #: The path of the chosen directory.
    path = Unicode


class MDirectoryDialog(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IDirectoryDialog interface.
    """
