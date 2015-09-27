#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

#
# Author: Riverbank Computing Limited
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------


# Local imports.
from traits.api import Event, Bool
from pyface.workbench.i_editor import MEditor


class Editor(MEditor):
    """ The toolkit specific implementation of an Editor.

    See the IEditor interface for the API documentation.

    """

    # Traits for showing spinner
    _loading = Event(Bool)
    _loading_on_open = Bool(False)

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the part. """

        from pyface.qt import QtCore, QtGui

        # By default we create a yellow panel!
        control = QtGui.QWidget(parent)

        pal = control.palette()
        pal.setColour(QtGui.QPalette.Window, QtCore.Qt.yellow)
        control.setPalette(pal)

        control.setAutoFillBackground(True)
        control.resize(100, 200)

        return control

    def destroy_control(self):
        """ Destroy the toolkit-specific control that represents the part. """

        if self.control is not None:
            # The `close` method emits a closeEvent event which is listened
            # by the workbench window layout, which responds by calling
            # destroy_control again.

            # We copy the control locally and set it to None immediately
            # to make sure this block of code is executed exactly once.

            _control = self.control
            self.control = None

            _control.hide()
            _control.close()
            _control.deleteLater()

        return

    def set_focus(self):
        """ Set the focus to the appropriate control in the part. """

        if self.control is not None:
            self.control.setFocus()

        return

#### EOF ######################################################################
