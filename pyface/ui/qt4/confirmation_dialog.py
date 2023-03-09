# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


from pyface.qt import QtCore, QtGui


from traits.api import Bool, Dict, Enum, provides, Str


from pyface.i_confirmation_dialog import (
    IConfirmationDialog,
    MConfirmationDialog,
)
from pyface.constant import CANCEL, YES, NO
from pyface.ui_traits import Image
from .dialog import Dialog, _RESULT_MAP


@provides(IConfirmationDialog)
class ConfirmationDialog(MConfirmationDialog, Dialog):
    """ The toolkit specific implementation of a ConfirmationDialog.  See the
    IConfirmationDialog interface for the API documentation.
    """

    # 'IConfirmationDialog' interface -------------------------------------#

    cancel = Bool(False)

    default = Enum(NO, YES, CANCEL)

    image = Image()

    message = Str()

    informative = Str()

    detail = Str()

    no_label = Str()

    yes_label = Str()

    # If we create custom buttons with the various roles, then we need to
    # keep track of the buttons so we can see what the user clicked.  It's
    # not correct nor sufficient to check the return result from QMessageBox.exec().
    _button_result_map = Dict()

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        # In PyQt this is a canned dialog.
        pass

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        dlg = QtGui.QMessageBox(parent)

        dlg.setWindowTitle(self.title)
        dlg.setText(self.message)
        dlg.setInformativeText(self.informative)
        dlg.setDetailedText(self.detail)

        if self.size != (-1, -1):
            dlg.resize(*self.size)

        if self.position != (-1, -1):
            dlg.move(*self.position)

        if self.image is None:
            dlg.setIcon(QtGui.QMessageBox.Icon.Warning)
        else:
            dlg.setIconPixmap(self.image.create_image())

        # The 'Yes' button.
        if self.yes_label:
            btn = dlg.addButton(self.yes_label, QtGui.QMessageBox.ButtonRole.YesRole)
        else:
            btn = dlg.addButton(QtGui.QMessageBox.StandardButton.Yes)
        self._button_result_map[btn] = YES

        if self.default == YES:
            dlg.setDefaultButton(btn)

        # The 'No' button.
        if self.no_label:
            btn = dlg.addButton(self.no_label, QtGui.QMessageBox.ButtonRole.NoRole)
        else:
            btn = dlg.addButton(QtGui.QMessageBox.StandardButton.No)
        self._button_result_map[btn] = NO

        if self.default == NO:
            dlg.setDefaultButton(btn)

        # The 'Cancel' button.
        if self.cancel:
            if self.cancel_label:
                btn = dlg.addButton(
                    self.cancel_label, QtGui.QMessageBox.ButtonRole.RejectRole
                )
            else:
                btn = dlg.addButton(QtGui.QMessageBox.StandardButton.Cancel)

            self._button_result_map[btn] = CANCEL

            if self.default == CANCEL:
                dlg.setDefaultButton(btn)

        return dlg

    def _show_modal(self):
        self.control.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        if hasattr(self.control, "exec"):
            retval = self.control.exec()
        else:
            retval = self.control.exec_()
        if self.control is None:
            # dialog window closed
            if self.cancel:
                # if cancel is available, close is Cancel
                return CANCEL
            return self.default
        clicked_button = self.control.clickedButton()
        if clicked_button in self._button_result_map:
            retval = self._button_result_map[clicked_button]
        else:
            retval = _RESULT_MAP[retval]
        return retval
