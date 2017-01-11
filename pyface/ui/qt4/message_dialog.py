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


# Major package imports.
from pyface.qt import QtGui

# Enthought library imports.
from traits.api import Enum, provides, Unicode

# Local imports.
from pyface.i_message_dialog import IMessageDialog, MMessageDialog
from .dialog import Dialog


# Map the ETS severity to the corresponding PyQt standard icon.
_SEVERITY_TO_ICON_MAP = {
    'information':  QtGui.QMessageBox.Information,
    'warning':      QtGui.QMessageBox.Warning,
    'error':        QtGui.QMessageBox.Critical
}


@provides(IMessageDialog)
class MessageDialog(MMessageDialog, Dialog):
    """ The toolkit specific implementation of a MessageDialog.  See the
    IMessageDialog interface for the API documentation.
    """


    #### 'IMessageDialog' interface ###########################################

    message = Unicode

    informative = Unicode

    detail = Unicode

    severity = Enum('information', 'warning', 'error')

    ###########################################################################
    # Protected 'IDialog' interface.
    ###########################################################################

    def _create_contents(self, parent):
        # In PyQt this is a canned dialog.
        pass

    ###########################################################################
    # Protected 'IWidget' interface.
    ###########################################################################

    def _create_control(self, parent):
        # FIXME: should be possble to set ok_label, but not implemented
        message_box = QtGui.QMessageBox(_SEVERITY_TO_ICON_MAP[self.severity],
                self.title, self.message, QtGui.QMessageBox.Ok, parent)
        message_box.setInformativeText(self.informative)
        message_box.setDetailedText(self.detail)

        if self.size != (-1, -1):
            message_box.resize(*self.size)

        if self.position != (-1, -1):
            message_box.move(*self.position)

        return message_box
