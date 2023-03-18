# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from pyface.qt import QtCore, QtGui

from traits.api import Any, List, Str, provides

from pyface.constant import CANCEL
from pyface.i_single_choice_dialog import (
    ISingleChoiceDialog,
    MSingleChoiceDialog,
)
from .dialog import Dialog, _RESULT_MAP


@provides(ISingleChoiceDialog)
class SingleChoiceDialog(MSingleChoiceDialog, Dialog):
    """ A dialog that allows the user to chose a single item from a list.

    Note that due to limitations of the QInputDialog class, the cancel trait
    is ignored, and the list of displayed strings must be unique.
    """

    # 'ISingleChoiceDialog' interface -------------------------------------#

    #: List of objects to choose from.
    choices = List(Any)

    #: The object chosen, if any.
    choice = Any()

    #: An optional attribute to use for the name of each object in the dialog.
    name_attribute = Str()

    #: The message to display to the user.
    message = Str()

    def set_dialog_choice(self, choice):
        if self.control is not None:
            if self.name_attribute != "":
                choice = getattr(choice, self.name_attribute)
            self.control.setTextValue(str(choice))

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        """ Creates the window contents. """
        # In this case, Qt does it all for us in 'QInputDialog'
        pass

    def _show_modal(self):
        self.control.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        if hasattr(self.control, 'exec'):
            retval = self.control.exec()
        else:
            retval = self.control.exec_()
        if self.control is None:
            # dialog window closed, treat as Cancel, nullify choice
            retval = CANCEL
        else:
            retval = _RESULT_MAP[retval]
        return retval

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def close(self):
        """ Closes the window. """

        # Get the chosen object.
        if self.control is not None and self.return_code != CANCEL:
            text = self.control.textValue()
            choices = self._choice_strings()
            if text in choices:
                idx = self._choice_strings().index(text)
                self.choice = self.choices[idx]
            else:
                self.choice = None
        else:
            self.choice = None

        # Let the window close as normal.
        super().close()

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the window. """
        dialog = QtGui.QInputDialog(parent)

        dialog.setOption(QtGui.QInputDialog.InputDialogOption.UseListViewForComboBoxItems, True)
        dialog.setWindowTitle(self.title)
        dialog.setLabelText(self.message)

        # initialize choices: set initial value to first choice
        choices = self._choice_strings()
        dialog.setComboBoxItems(choices)
        dialog.setTextValue(choices[0])

        if self.size != (-1, -1):
            self.resize(*self.size)
        if self.position != (-1, -1):
            self.move(*self.position)

        return dialog
