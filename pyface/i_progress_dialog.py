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
""" The interface for a dialog that allows the user to open/save files etc. """

# Enthought library imports.
from traits.api import Any, Bool, Int, Str

# Local imports.
from i_dialog import IDialog


class IProgressDialog(IDialog):
    """ A simple progress dialog window which allows itself to be updated
    """

    #### 'IProgressDialog' interface ##################################
    title = Str
    message = Str
    min = Int
    max = Int
    margin = Int(5)
    can_cancel = Bool(False)
    show_time = Bool(False)
    show_percent = Bool(False)


    # Label for the 'cancel' button
    cancel_button_label = Str

    ###########################################################################
    # 'IProgressDialog' interface.
    ###########################################################################

    def update(self, value):
        """
        updates the progress bar to the desired value. If the value is >=
        the maximum and the progress bar is not contained in another panel
        the parent window will be closed

        """


class MProgressDialog(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IProgressDialog interface.

    Implements: update()
    """

    progress_bar = Any

    ###########################################################################
    # 'IProgressDialog' interface.
    ###########################################################################

    def update(self, value):
        """
        updates the progress bar to the desired value. If the value is >=
        the maximum and the progress bar is not contained in another panel
        the parent window will be closed

        """

        if self.progress_bar is not None:
            self.progress_bar.update(value)

        if value >= self.max:
            self.close()
