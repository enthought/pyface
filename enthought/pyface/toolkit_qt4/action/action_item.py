#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui


class _MenuItem_qt4(object):
    """ The _MenuItem monkey patch for Qt4. """

    ###########################################################################
    # '_MenuItem' toolkit interface.
    ###########################################################################

    def _tk__menuitem_create(self, parent, menu):
        """ Create a menu item added to a menu. """

        action = self.item.action

        # ZZZ: Is there any reason not to use any image provided by the action?
        # Possibly because there is a default image (and for menu items the
        # default should be no image).

        # ZZZ: This is a wx'ism and should be hidden in the toolkit code.
        self.control_id = None

        control = menu.addAction(action.name, self._qt4_on_triggered,
                action.accelerator)

        control.setToolTip(action.tooltip)
        control.setWhatsThis(action.description)
        control.setEnabled(action.enabled)

        if action.style == 'toggle':
            control.setCheckable(True)
            control.setChecked(action.checked)
        elif action.style == 'radio':
            # Create an action group if it hasn't already been done.
            try:
                ag = self.item.parent._qt4_ag
            except AttributeError:
                ag = self.item.parent._qt4_ag = QtGui.QActionGroup(parent)

            control.setActionGroup(ag)

            control.setCheckable(True)
            control.setChecked(action.checked)

        return control

    def _tk__menuitem_set_enabled(self, enabled):
        """ Set the enabled state of a menu item. """

        self.control.setEnabled(enabled)

    def _tk__menuitem_set_checked(self, checked):
        """ Set the checked state of a menu item. """

        self.control.setChecked(checked)

    def _tk__menuitem_get_checked(self):
        """ Get the checked state of a menu item. """

        return self.control.isChecked()

    def _tk__menuitem_set_named(self, name):
        """ Set the name of a menu item. """

        self.control.setText(name)

    #### Slot handlers ########################################################

    def _qt4_on_triggered(self):
        """ Called when the menu item is clicked. """

        self._handle_tk__menuitem_clicked()


class _Tool_qt4(object):
    """ The _Tool monkey patch for Qt4. """

    ###########################################################################
    # '_Tool' toolkit interface.
    ###########################################################################

    def _tk__tool_create(self, parent, image_cache, show_labels):
        """ Create a tool to be added to a tool bar. """

        action = self.item.action

        size = self.tool_bar.iconSize()
        image = action.image.create_image((size.width(), size.height()))
        image = image_cache.get_image(action.image.absolute_path)

        # ZZZ: This is a wx'ism and should be hidden in the toolkit code.
        self.control_id = None

        control = self.tool_bar.addAction(QtGui.QIcon(image), action.name,
                self._qt4_on_triggered)

        control.setToolTip(action.tooltip)
        control.setWhatsThis(action.description)
        control.setEnabled(action.enabled)

        if action.style == 'toggle':
            control.setCheckable(True)
            control.setChecked(action.checked)
        elif action.style == 'radio':
            # Create an action group if it hasn't already been done.
            try:
                ag = self.item.parent._qt4_ag
            except AttributeError:
                ag = self.item.parent._qt4_ag = QtGui.QActionGroup(parent)

            control.setActionGroup(ag)

            control.setCheckable(True)
            control.setChecked(action.checked)

        return control

    def _tk__tool_set_enabled(self, enabled):
        """ Set the enabled state of a tool bar tool. """

        self.control.setEnabled(enabled)

    def _tk__tool_set_checked(self, checked):
        """ Set the checked state of a tool bar tool. """

        self.control.setChecked(checked)

    def _tk__tool_get_checked(self):
        """ Get the checked state of a tool bar tool. """

        return self.control.isChecked()

    #### Slot handlers ########################################################

    def _qt4_on_triggered(self):
        """ Called when the tool bar tool is clicked. """

        self._handle_tk__tool_clicked()
