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

# Standard library imports.
import platform
import sys

# Major package imports.
from pyface.qt import QtCore, QtGui

# Enthought library imports.
from traits.api import Instance, List, provides, Unicode

# Local imports.
from pyface.i_about_dialog import IAboutDialog, MAboutDialog
from pyface.image_resource import ImageResource
from .dialog import Dialog

# The HTML displayed in the QLabel.
_DIALOG_TEXT = '''
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
      Copyright &copy; 2003-2010 Enthought, Inc.<br>
      Copyright &copy; 2007 Riverbank Computing Limited
      </p>
  </center>
  </body>
</html>
'''


@provides(IAboutDialog)
class AboutDialog(MAboutDialog, Dialog):
    """ The toolkit specific implementation of an AboutDialog.  See the
    IAboutDialog interface for the API documentation.
    """

    #### 'IAboutDialog' interface #############################################

    additions = List(Unicode)

    image = Instance(ImageResource, ImageResource('about'))

    ###########################################################################
    # Protected 'IDialog' interface.
    ###########################################################################

    def _create_contents(self, parent):
        label = QtGui.QLabel()

        if self.title == "":
            if parent.parent() is not None:
                title = parent.parent().windowTitle()
            else:
                title = ""

            # Set the title.
            self.title = "About %s" % title

        # Load the image to be displayed in the about box.
        image = self.image.create_image()
        path = self.image.absolute_path

        # The additional strings.
        additions = '<br />'.join(self.additions)

        # Get the version numbers.
        py_version = platform.python_version()
        qt_version = QtCore.__version__

        # Set the page contents.
        label.setText(_DIALOG_TEXT % (path, additions, py_version, qt_version))

        # Create the button.
        buttons = QtGui.QDialogButtonBox()

        if self.ok_label:
            buttons.addButton(self.ok_label, QtGui.QDialogButtonBox.AcceptRole)
        else:
            buttons.addButton(QtGui.QDialogButtonBox.Ok)

        buttons.accepted.connect(parent.accept)

        lay = QtGui.QVBoxLayout()
        lay.addWidget(label)
        lay.addWidget(buttons)

        parent.setLayout(lay)
