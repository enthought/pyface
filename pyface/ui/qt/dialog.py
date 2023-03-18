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


from traits.api import (
    Any, Bool, Callable, Enum, Int, List, provides, Str, Tuple
)

from pyface.i_dialog import IDialog, MDialog
from pyface.constant import OK, CANCEL, YES, NO
from .window import Window


# Map PyQt dialog related constants to the pyface equivalents.
_RESULT_MAP = {
    QtGui.QDialog.DialogCode.Accepted: OK,
    QtGui.QDialog.DialogCode.Rejected: CANCEL,
    QtGui.QMessageBox.StandardButton.Ok: OK,
    QtGui.QMessageBox.StandardButton.Cancel: CANCEL,
    QtGui.QMessageBox.StandardButton.Yes: YES,
    QtGui.QMessageBox.StandardButton.No: NO,
}


@provides(IDialog)
class Dialog(MDialog, Window):
    """ The toolkit specific implementation of a Dialog.  See the IDialog
    interface for the API documentation.
    """

    # 'IDialog' interface -------------------------------------------------#

    cancel_label = Str()

    help_id = Str()

    help_label = Str()

    ok_label = Str()

    resizeable = Bool(True)

    return_code = Int(OK)

    style = Enum("modal", "nonmodal")

    # 'IWindow' interface -------------------------------------------------#

    title = Str("Dialog")

    # Private interface ---------------------------------------------------#

    #: A list of connected Qt signals to be removed before destruction.
    #: First item in the tuple is the Qt signal. The second item is the event
    #: handler.
    _connections_to_remove = List(Tuple(Any, Callable))

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_buttons(self, parent):
        buttons = QtGui.QDialogButtonBox()

        # 'OK' button.
        if self.ok_label:
            btn = buttons.addButton(
                self.ok_label, QtGui.QDialogButtonBox.ButtonRole.AcceptRole
            )
        else:
            btn = buttons.addButton(QtGui.QDialogButtonBox.StandardButton.Ok)

        btn.setDefault(True)
        btn.clicked.connect(self.control.accept)
        self._connections_to_remove.append((btn.clicked, self.control.accept))

        # 'Cancel' button.
        if self.cancel_label:
            btn = buttons.addButton(
                self.cancel_label, QtGui.QDialogButtonBox.ButtonRole.RejectRole
            )
        else:
            btn = buttons.addButton(QtGui.QDialogButtonBox.StandardButton.Cancel)

        btn.clicked.connect(self.control.reject)
        self._connections_to_remove.append((btn.clicked, self.control.reject))

        # 'Help' button.
        # FIXME v3: In the original code the only possible hook into the help
        # was to reimplement self._on_help().  However this was a private
        # method.  Obviously nobody uses the Help button.  For the moment we
        # display it but can't actually use it.
        if len(self.help_id) > 0:
            if self.help_label:
                buttons.addButton(
                    self.help_label, QtGui.QDialogButtonBox.ButtonRole.HelpRole
                )
            else:
                buttons.addButton(QtGui.QDialogButtonBox.StandardButton.Help)

        return buttons

    def _create_contents(self, parent):
        layout = QtGui.QVBoxLayout()

        if not self.resizeable:
            layout.setSizeConstraint(QtGui.QLayout.SizeConstraint.SetFixedSize)

        layout.addWidget(self._create_dialog_area(parent))
        layout.addWidget(self._create_buttons(parent))

        parent.setLayout(layout)

    def _create_dialog_area(self, parent):
        panel = QtGui.QWidget(parent)
        panel.setMinimumSize(QtCore.QSize(100, 200))

        palette = panel.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("red"))
        panel.setPalette(palette)
        panel.setAutoFillBackground(True)

        return panel

    def _show_modal(self):
        dialog = self.control
        dialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

        # Suppress the context-help button hint, which
        # results in a non-functional "?" button on Windows.
        dialog.setWindowFlags(
            dialog.windowFlags() & ~QtCore.Qt.WindowType.WindowContextHelpButtonHint
        )

        if hasattr(self.control, "exec"):
            retval = self.control.exec()
        else:
            retval = self.control.exec_()
        return _RESULT_MAP[retval]

    # -------------------------------------------------------------------------
    # 'IWidget' interface.
    # -------------------------------------------------------------------------

    def destroy(self):
        while self._connections_to_remove:
            signal, handler = self._connections_to_remove.pop()
            signal.disconnect(handler)

        super().destroy()

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        dlg = QtGui.QDialog(parent)

        # Setting return code and firing close events is handled for 'modal' in
        # MDialog's open method. For 'nonmodal', we do it here.
        if self.style == "nonmodal":
            dlg.finished.connect(self._finished_fired)
            self._connections_to_remove.append(
                (dlg.finished, self._finished_fired)
            )

        if self.size != (-1, -1):
            dlg.resize(*self.size)

        if self.position != (-1, -1):
            dlg.move(*self.position)

        dlg.setWindowTitle(self.title)

        return dlg

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _finished_fired(self, result):
        """ Called when the dialog is closed (and nonmodal). """

        self.return_code = _RESULT_MAP[result]
        self.close()
