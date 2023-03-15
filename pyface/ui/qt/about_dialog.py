# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import platform

from traits.api import Any, Callable, List, provides, Tuple

from pyface.qt import QtCore, QtGui
from pyface.i_about_dialog import IAboutDialog, MAboutDialog
from .dialog import Dialog


# The HTML displayed in the QLabel.
_DIALOG_TEXT = """
<html>
  <body>
    <center>
      <table width="100%%" cellspacing="4" cellpadding="0" border="0">
        <tr>
          <td align="center">
          <p>
            <img src="%s" alt="">
          </td>
        </tr>
      </table>

      <p>
      %s<br>
      <br>
      Python %s<br>
      Qt %s<br>
      </p>
      <p>
      %s
      </p>
      <p>
      Copyright &copy; 2003-2023 Enthought, Inc.<br>
      Copyright &copy; 2007 Riverbank Computing Limited
      </p>
  </center>
  </body>
</html>
"""


@provides(IAboutDialog)
class AboutDialog(MAboutDialog, Dialog):
    """ The toolkit specific implementation of an AboutDialog.  See the
    IAboutDialog interface for the API documentation.
    """

    # Private interface ---------------------------------------------------#

    #: A list of connected Qt signals to be removed before destruction.
    #: First item in the tuple is the Qt signal. The second item is the event
    #: handler.
    _connections_to_remove = List(Tuple(Any, Callable))

    # -------------------------------------------------------------------------
    # 'IWidget' interface.
    # -------------------------------------------------------------------------

    def destroy(self):
        while self._connections_to_remove:
            signal, handler = self._connections_to_remove.pop()
            signal.disconnect(handler)

        super().destroy()

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        label = QtGui.QLabel()

        if self.title == "":
            if parent.parent() is not None:
                title = parent.parent().windowTitle()
            else:
                title = ""

            # Set the title.
            self.title = "About %s" % title

        # Set the page contents.
        label.setText(self._create_html())

        # Create the button.
        buttons = QtGui.QDialogButtonBox()

        if self.ok_label:
            buttons.addButton(self.ok_label, QtGui.QDialogButtonBox.ButtonRole.AcceptRole)
        else:
            buttons.addButton(QtGui.QDialogButtonBox.StandardButton.Ok)

        buttons.accepted.connect(parent.accept)
        self._connections_to_remove.append((buttons.accepted, parent.accept))

        lay = QtGui.QVBoxLayout()
        lay.addWidget(label)
        lay.addWidget(buttons)

        parent.setLayout(lay)

    def _create_html(self):
        # Load the image to be displayed in the about box.
        path = self.image.absolute_path

        # The additional strings.
        additions = "<br />".join(self.additions)

        # Get the version numbers.
        py_version = platform.python_version()
        qt_version = QtCore.__version__

        # The additional copyright strings.
        copyrights = "<br />".join(
            ["Copyright &copy; %s" % line for line in self.copyrights]
        )

        return _DIALOG_TEXT % (
            path,
            additions,
            py_version,
            qt_version,
            copyrights,
        )
