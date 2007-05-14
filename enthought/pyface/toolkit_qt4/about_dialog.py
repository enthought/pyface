#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtCore, QtGui


DIALOG_TEXT = '''
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
      Enthought Library  -  Build #%s<br>
      <br>
      Python %s<br>
      PyQt %s<br>
      Qt %s<br>
      </p>
      <p>
      Copyright &copy; 2003-2007 Enthought, Inc.<br>
      Copyright &copy; 2007 Riverbank Computing Limited
      </p>
  </center>
  </body>
</html>
'''


class AboutDialog_qt4(object):
    """ The AboutDialog monkey patch for Qt4. """

    ###########################################################################
    # 'AboutDialog' toolkit interface.
    ###########################################################################

    def _tk_aboutdialog_create_contents(self, parent, version, py_version):
        """ Creates the dialog contents. """

        label = QtGui.QLabel()

        if parent.parent() is not None:
            title = parent.parent().windowTitle()
        else:
            title = ""

        # Set the title.
        self.title = "About %s" % title

        # Load the image to be displayed in the about box.
        image = self.image.create_image()
        path  = self.image.absolute_path

        # The additional strings.
        additions = '<br />'.join(self.additions)

        # Get the other version numbers.
        pyqt_version = QtCore.PYQT_VERSION_STR
        qt_version = QtCore.QT_VERSION_STR

        # Set the page contents.
        label.setText(DIALOG_TEXT % (path, additions, version, py_version, pyqt_version, qt_version))

        # Create the button.
        buttons = QtGui.QDialogButtonBox()

        if self.ok_button_label:
            buttons.addButton(self.ok_button_label, QtGui.QDialogButtonBox.AcceptRole)
        else:
            buttons.addButton(QtGui.QDialogButtonBox.Ok)

        buttons.connect(buttons, QtCore.SIGNAL('accepted()'), parent, QtCore.SLOT('accept()'))

        lay = QtGui.QVBoxLayout()
        lay.addWidget(label)
        lay.addWidget(buttons)
        parent.setLayout(lay)

        return None
