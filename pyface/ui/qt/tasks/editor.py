# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.tasks.i_editor import IEditor, MEditor
from traits.api import Bool, Property, provides


from pyface.qt import QtGui


@provides(IEditor)
class Editor(MEditor):
    """ The toolkit-specific implementation of a Editor.

    See the IEditor interface for API documentation.
    """

    # 'IEditor' interface -------------------------------------------------#

    has_focus = Property(Bool)

    # ------------------------------------------------------------------------
    # 'IEditor' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        self.control = QtGui.QWidget(parent)

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        if self.control is not None:
            self.control.hide()
            self.control.deleteLater()
            self.control = None

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_has_focus(self):
        if self.control is not None:
            return self.control.hasFocus()
        return False
