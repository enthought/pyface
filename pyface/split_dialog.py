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
""" A dialog that is split in two either horizontally or vertically. """


# Local imports.
from pyface.dialog import Dialog
from pyface.split_widget import SplitWidget


class SplitDialog(Dialog, SplitWidget):
    """ A dialog that is split in two either horizontally or vertically. """

    ###########################################################################
    # Protected 'Dialog' interface.
    ###########################################################################

    def _create_dialog_area(self, parent):
        """ Creates the main content of the dialog.

        Parameters
        ----------
        parent : toolkit control
            A toolkit control to be used as the parent for the splitter.

        Returns
        -------
        control : toolkit control
            The splitter control.
        """
        return self._create_splitter(parent)
