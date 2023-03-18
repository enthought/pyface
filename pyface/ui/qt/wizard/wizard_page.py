# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2008 Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


""" A page in a wizard. """


from pyface.qt import QtGui


from traits.api import Bool, HasTraits, provides, Str, Tuple
from pyface.wizard.i_wizard_page import IWizardPage, MWizardPage


@provides(IWizardPage)
class WizardPage(MWizardPage, HasTraits):
    """ The toolkit specific implementation of a WizardPage.

    See the IWizardPage interface for the API documentation.

    """

    # 'IWizardPage' interface ---------------------------------------------#

    id = Str()

    next_id = Str()

    last_page = Bool(False)

    complete = Bool(False)

    heading = Str()

    subheading = Str()

    size = Tuple()

    # ------------------------------------------------------------------------
    # 'IWizardPage' interface.
    # ------------------------------------------------------------------------

    def create_page(self, parent):
        """ Creates the wizard page. """

        content = self._create_page_content(parent)

        # We allow some flexibility with the sort of control we are given.
        if not isinstance(content, QtGui.QWizardPage):
            wp = _WizardPage(self)

            if isinstance(content, QtGui.QLayout):
                wp.setLayout(content)
            else:
                assert isinstance(content, QtGui.QWidget)

                lay = QtGui.QVBoxLayout()
                lay.addWidget(content)

                wp.setLayout(lay)

            content = wp

        # Honour any requested page size.
        if self.size:
            width, height = self.size

            if width > 0:
                content.setMinimumWidth(width)

            if height > 0:
                content.setMinimumHeight(height)

        content.setTitle(self.heading)
        content.setSubTitle(self.subheading)

        return content

    # ------------------------------------------------------------------------
    # Protected 'IWizardPage' interface.
    # ------------------------------------------------------------------------

    def _create_page_content(self, parent):
        """ Creates the actual page content. """

        # Dummy implementation - override!
        control = QtGui.QWidget(parent)

        palette = control.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("yellow"))
        control.setPalette(palette)
        control.setAutoFillBackground(True)

        return control


class _WizardPage(QtGui.QWizardPage):
    """ A QWizardPage sub-class that hooks into the IWizardPage's 'complete'
    trait. """

    def __init__(self, page):
        """ Initialise the object. """

        QtGui.QWizardPage.__init__(self)

        self.pyface_wizard = None

        page.observe(self._on_complete_changed, "complete")
        self._page = page

    def initializePage(self):
        """ Reimplemented to call the IWizard's 'next'. """

        if self.pyface_wizard is not None:
            self.pyface_wizard.next()

    def cleanupPage(self):
        """ Reimplemented to call the IWizard's 'previous'. """

        if self.pyface_wizard is not None:
            self.pyface_wizard.previous()

    def isComplete(self):
        """ Reimplemented to return the state of the 'complete' trait. """

        return self._page.complete

    def _on_complete_changed(self, event):
        """ The trait handler for when the page's completion state changes. """

        self.completeChanged.emit()
