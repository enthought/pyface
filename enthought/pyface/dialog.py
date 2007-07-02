#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" The abstract interface for all pyface dialogs. """


# Enthought library imports.
from enthought.traits.api import Bool, Enum, Int, Str, Unicode

# Local imports.
from constant import OK
from window import IWindow


class IDialog(IWindow):
    """ The abstract interface for all pyface dialogs.

    Usage: Sub-class this class and either override '_create_contents' or
    more simply, just override the two methods that do the real work:-

    1) '_create_dialog_area' creates the main content of the dialog.
    2) '_create_buttons'     creates the dialog buttons.
    """

    #### 'IDialog' interface ##################################################

    # The label for the 'cancel' button.  The default is toolkit specific.
    cancel_label = Unicode

    # The context sensitive help Id (the 'Help' button is only shown iff this
    # is set).
    help_id = Str

    # The label for the 'help' button.  The default is toolkit specific.
    help_label = Unicode

    # The label for the 'ok' button.  The default is toolkit specific.
    ok_label = Unicode

    # Is the dialog resizeable?
    resizeable = Bool(True)

    # The return code after the window is closed to indicate whether the dialog
    # was closed via 'Ok' or 'Cancel').
    return_code = Int(OK)

    # The dialog style (is it modal or not).
    # FIXME v3: It doesn't seem possible to use non-modal dialogs.  (How do you
    # get access to the buttons?)
    style = Enum('modal', 'nonmodal')

    ###########################################################################
    # 'IDialog' interface.
    ###########################################################################

    def open(self):
        """ Opens the dialog.

        If the dialog is modal then the dialog's event loop is entered and the
        dialog closed afterwards.  The 'return_code' trait is updated according
        to the button the user pressed and this value is also returned.

        If the dialog is non-modal 'OK' is returned.
        """

    ###########################################################################
    # Protected 'IDialog' interface.
    ###########################################################################

    def _create_buttons(self, parent):
        """ Create and return the buttons.

        parent is the parent control.
        """

    def _create_contents(self, parent):
        """ Create the dialog contents.

        parent is the parent control.
        """

    def _create_dialog_area(self, parent):
        """ Create and return the main content of the dialog.

        parent is the parent control.
        """

    def _show_modal(self):
        """ Opens the dialog as a modal dialog and returns the return code. """


class MDialog(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IDialog interface.

    Implements: open()
    Reimplements: _add_event_listeners(), _create()
    """

    ###########################################################################
    # 'IDialog' interface.
    ###########################################################################

    def open(self):
        """ Opens the dialog. """

        super(MDialog, self).open()

        if self.style == 'modal':
            self.return_code = self._show_modal()
            self.close()

        else:
            self.return_code = OK

        return self.return_code

    ###########################################################################
    # Protected 'IWidget' interface.
    ###########################################################################

    def _create(self):
        """ Creates the window's widget hierarchy. """

        super(MDialog, self)._create()

        self._create_contents(self.control)

    ###########################################################################
    # Protected 'IWindow' interface.
    ###########################################################################

    def _add_event_listeners(self):
        """ Adds any event listeners required by the window. """

        # We don't bother for dialogs.
        pass


# The following will be removed when everything has been moved to interfaces.

# Enthought library imports.
from enthought.logger import logger

# Local imports.
from window import Window


class Dialog(Window):
    """ The abstract base-class for all Pyface dialogs.

    Usage: Sub-class this class and either override '_create_contents' or
    more simply, just override the two methods that do the real work:-

    1) '_create_dialog_area' creates the main content of the dialog.
    2) '_create_buttons'     creates the dialog buttons.

    """

    __tko__ = 'Dialog'

    #### 'Window' interface ###################################################

    # The dialog title.
    title = Str('Dialog')
    
    #### 'Dialog' interface ###################################################

    # The context sensitive help Id (the 'Help' button is only shown iff this
    # is set).
    help_id = Str

    # Is the dialog resizeable?
    resizeable = Bool(True)
    
    # The dialog style (is it modal or not).
    style = Enum('modal', 'nonmodal')

    # The size of the border around the dialog area.
    # FIXME v3: This should be removed (or at least made a hint).
    dialog_area_border = Int(5)

    # Label for the 'ok' button.  The default is toolkit specific.
    ok_button_label = Str

    # Label for the 'cancel' button.  The default is toolkit specific.
    cancel_button_label = Str

    # Label for the 'help' button.  The default is toolkit specific.
    help_button_label = Str

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def open(self):
        """ Opens the window. """

        if self.control is None:
            self._create()

            if self.style == 'modal':
                self.return_code = self._tk_dialog_show_modal()
                self.close()

            else:
                self.show(True)
                self.return_code = OK
        else:
            logger.debug('dialog is already open %s' % str(self))

        return self.return_code

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents.

        Sub-classes can either override this method completely, or instead
        override the two methods that do the real work:-

        1) '_create_dialog_area' creates the main content of the dialog.
        2) '_create_buttons'     creates the dialog buttons.

        """

        dialog_area = self._create_dialog_area(parent)
        buttons = self._create_buttons(parent)
        self._tk_dialog_assemble(parent, dialog_area, buttons)

        return parent

    ###########################################################################
    # Protected 'Dialog' interface.
    ###########################################################################

    def _create_dialog_area(self, parent):
        """ Creates the main content of the dialog. """

        return self._tk_dialog_create_area(parent)

    def _create_buttons(self, parent):
        """ Creates the buttons. """

        return self._tk_dialog_create_buttons(parent)

    ###########################################################################
    # 'Dialog' toolkit interface.
    ###########################################################################

    def _tk_dialog_show_modal(self):
        """ Show a modal dialog and return the pyface result.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_dialog_create_area(self, parent):
        """ Creates the main content of the dialog.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_dialog_create_buttons(self, parent):
        """ Creates the buttons.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_dialog_assemble(self, dialog, dialog_area, buttons):
        """ Complete the dialog by assembling the various components.
        
        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
