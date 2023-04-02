# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A window that is split in two either horizontally or vertically. """


from pyface.application_window import ApplicationWindow
from pyface.split_widget import SplitWidget


class SplitApplicationWindow(ApplicationWindow, SplitWidget):
    """ A window that is split in two either horizontally or vertically. """

    # ------------------------------------------------------------------------
    # Protected 'ApplicationWindow' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        """ Creates the window contents.

        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control to be used as the parent for the
            splitter control.

        Returns
        -------
        control : toolkit control
            The splitter control to be used for contents of the window.
        """
        return self._create_splitter(parent)
