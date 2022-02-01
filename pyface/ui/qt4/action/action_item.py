# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The PyQt specific implementations the action manager internal classes. """


from inspect import getfullargspec


from pyface.qt import QtGui


from traits.api import Any, Bool, HasTraits


from pyface.action.action_event import ActionEvent


class PyfaceWidgetAction(QtGui.QWidgetAction):
    def __init__(self, parent, action):
        super().__init__(parent)
        self.action = action

    def createWidget(self, parent):
        widget = self.action.create_control(parent)
        widget._action = self.action
        return widget


class _MenuItem(HasTraits):
    """ A menu item representation of an action item. """

    # '_MenuItem' interface ------------------------------------------------

    # Is the item checked?
    checked = Bool(False)

    # A controller object we delegate taking actions through (if any).
    controller = Any()

    # Is the item enabled?
    enabled = Bool(True)

    # Is the item visible?
    visible = Bool(True)

    # The radio group we are part of (None if the menu item is not part of such
    # a group).
    group = Any()

    # The toolkit control.
    control = Any()

    # The toolkit control id.
    control_id = None

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, menu, item, controller):
        """ Creates a new menu item for an action item. """

        self.item = item
        action = item.action

        # FIXME v3: This is a wx'ism and should be hidden in the toolkit code.
        self.control_id = None

        if action.style == "widget":
            self.control = PyfaceWidgetAction(parent, action)
            menu.addAction(self.control)
        elif action.image is None:
            self.control = menu.addAction(
                action.name, self._qt4_on_triggered, action.accelerator
            )
        else:
            self.control = menu.addAction(
                action.image.create_icon(),
                action.name,
                self._qt4_on_triggered,
                action.accelerator,
            )
        menu.menu_items.append(self)

        self.control.setToolTip(action.tooltip)
        self.control.setWhatsThis(action.description)
        self.control.setEnabled(action.enabled)
        self.control.setVisible(action.visible)

        if getattr(action, "menu_role", False):
            if action.menu_role == "About":
                self.control.setMenuRole(QtGui.QAction.MenuRole.AboutRole)
            elif action.menu_role == "Preferences":
                self.control.setMenuRole(QtGui.QAction.MenuRole.PreferencesRole)

        if action.style == "toggle":
            self.control.setCheckable(True)
            self.control.setChecked(action.checked)
        elif action.style == "radio":
            # Create an action group if it hasn't already been done.
            try:
                ag = item.parent._qt4_ag
            except AttributeError:
                ag = item.parent._qt4_ag = QtGui.QActionGroup(parent)

            self.control.setActionGroup(ag)

            self.control.setCheckable(True)
            self.control.setChecked(action.checked)

        # Listen for trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        action.observe(self._on_action_enabled_changed, "enabled")
        action.observe(self._on_action_visible_changed, "visible")
        action.observe(self._on_action_checked_changed, "checked")
        action.observe(self._on_action_name_changed, "name")
        action.observe(self._on_action_accelerator_changed, "accelerator")
        action.observe(self._on_action_image_changed, "image")
        action.observe(self._on_action_tooltip_changed, "tooltip")

        # Detect if the control is destroyed.
        self.control.destroyed.connect(self._qt4_on_destroyed)

        if controller is not None:
            self.controller = controller
            controller.add_to_menu(self)

    def dispose(self):
        action = self.item.action
        action.observe(self._on_action_enabled_changed, "enabled", remove=True)
        action.observe(self._on_action_visible_changed, "visible", remove=True)
        action.observe(self._on_action_checked_changed, "checked", remove=True)
        action.observe(self._on_action_name_changed, "name", remove=True)
        action.observe(
            self._on_action_accelerator_changed, "accelerator", remove=True
        )
        action.observe(self._on_action_image_changed, "image", remove=True)
        action.observe(self._on_action_tooltip_changed, "tooltip", remove=True)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _qt4_on_destroyed(self, control=None):
        """ Delete the reference to the control to avoid attempting to talk to
        it again.
        """
        self.control = None

    def _qt4_on_triggered(self):
        """ Called when the menu item has been clicked. """

        action = self.item.action
        action_event = ActionEvent()

        is_checkable = action.style in ["radio", "toggle"]

        # Perform the action!
        if self.controller is not None:
            if is_checkable:
                self.checked = action.checked = self.control.isChecked()

            # Most of the time, action's do no care about the event (it
            # contains information about the time the event occurred etc), so
            # we only pass it if the perform method requires it. This is also
            # useful as Traits UI controllers *never* require the event.
            argspec = getfullargspec(self.controller.perform)

            # If the only arguments are 'self' and 'action' then don't pass
            # the event!
            if len(argspec.args) == 2:
                self.controller.perform(action)

            else:
                self.controller.perform(action, action_event)

        else:
            if is_checkable:
                self.checked = action.checked = self.control.isChecked()

            # Most of the time, action's do no care about the event (it
            # contains information about the time the event occurred etc), so
            # we only pass it if the perform method requires it.
            argspec = getfullargspec(action.perform)

            # If the only argument is 'self' then don't pass the event!
            if len(argspec.args) == 1:
                action.perform()

            else:
                action.perform(action_event)

    # Trait event handlers -------------------------------------------------

    def _enabled_changed(self):
        """ Called when our 'enabled' trait is changed. """
        if self.control is not None:
            self.control.setEnabled(self.enabled)

    def _visible_changed(self):
        """ Called when our 'visible' trait is changed. """
        if self.control is not None:
            self.control.setVisible(self.visible)

    def _checked_changed(self):
        """ Called when our 'checked' trait is changed. """
        if self.control is not None:
            self.control.setChecked(self.checked)

    def _on_action_enabled_changed(self, event):
        """ Called when the enabled trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setEnabled(action.enabled)

    def _on_action_visible_changed(self, event):
        """ Called when the visible trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setVisible(action.visible)

    def _on_action_checked_changed(self, event):
        """ Called when the checked trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setChecked(action.checked)

    def _on_action_name_changed(self, event):
        """ Called when the name trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setText(action.name)

    def _on_action_accelerator_changed(self, event):
        """ Called when the accelerator trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setShortcut(action.accelerator)

    def _on_action_image_changed(self, event):
        """ Called when the accelerator trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setIcon(action.image.create_icon())

    def _on_action_tooltip_changed(self, event):
        """ Called when the accelerator trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setToolTip(action.tooltip)


class _Tool(HasTraits):
    """ A tool bar tool representation of an action item. """

    # '_Tool' interface ----------------------------------------------------

    # Is the item checked?
    checked = Bool(False)

    # A controller object we delegate taking actions through (if any).
    controller = Any()

    # Is the item enabled?
    enabled = Bool(True)

    # Is the item visible?
    visible = Bool(True)

    # The radio group we are part of (None if the tool is not part of such a
    # group).
    group = Any()

    # The toolkit control.
    control = Any()

    # The toolkit control id.
    control_id = None

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(
        self, parent, tool_bar, image_cache, item, controller, show_labels
    ):
        """ Creates a new tool bar tool for an action item. """

        self.item = item
        self.tool_bar = tool_bar
        action = item.action

        if action.style == "widget":
            widget = action.create_control(tool_bar)
            self.control = tool_bar.addWidget(widget)
        elif action.image is None:
            self.control = tool_bar.addAction(action.name)
        else:
            size = tool_bar.iconSize()
            image = action.image.create_icon((size.width(), size.height()))
            self.control = tool_bar.addAction(image, action.name)
        tool_bar.tools.append(self)

        self.control.triggered.connect(self._qt4_on_triggered)

        self.control.setToolTip(action.tooltip)
        self.control.setWhatsThis(action.description)
        self.control.setEnabled(action.enabled)
        self.control.setVisible(action.visible)

        if action.style == "toggle":
            self.control.setCheckable(True)
            self.control.setChecked(action.checked)
        elif action.style == "radio":
            # Create an action group if it hasn't already been done.
            try:
                ag = item.parent._qt4_ag
            except AttributeError:
                ag = item.parent._qt4_ag = QtGui.QActionGroup(parent)

            self.control.setActionGroup(ag)

            self.control.setCheckable(True)
            self.control.setChecked(action.checked)

        # Keep a reference in the action.  This is done to make sure we live as
        # long as the action (and still respond to its signals) and don't die
        # if the manager that created us is garbage collected.
        self.control._tool_instance = self

        # Listen for trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        action.observe(self._on_action_enabled_changed, "enabled")
        action.observe(self._on_action_visible_changed, "visible")
        action.observe(self._on_action_checked_changed, "checked")
        action.observe(self._on_action_name_changed, "name")
        action.observe(self._on_action_accelerator_changed, "accelerator")
        action.observe(self._on_action_image_changed, "image")
        action.observe(self._on_action_tooltip_changed, "tooltip")

        # Detect if the control is destroyed.
        self.control.destroyed.connect(self._qt4_on_destroyed)

        if controller is not None:
            self.controller = controller
            controller.add_to_toolbar(self)

    def dispose(self):
        action = self.item.action
        action.observe(self._on_action_enabled_changed, "enabled", remove=True)
        action.observe(self._on_action_visible_changed, "visible", remove=True)
        action.observe(self._on_action_checked_changed, "checked", remove=True)
        action.observe(self._on_action_name_changed, "name", remove=True)
        action.observe(
            self._on_action_accelerator_changed, "accelerator", remove=True
        )
        action.observe(self._on_action_image_changed, "image", remove=True)
        action.observe(self._on_action_tooltip_changed, "tooltip", remove=True)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _qt4_on_destroyed(self, control=None):
        """ Delete the reference to the control to avoid attempting to talk to
        it again.
        """
        self.control = None

    def _qt4_on_triggered(self):
        """ Called when the tool bar tool is clicked. """

        action = self.item.action
        action_event = ActionEvent()

        # Perform the action!
        if self.controller is not None:
            self.checked = action.checked = self.control.isChecked()

            # Most of the time, action's do no care about the event (it
            # contains information about the time the event occurred etc), so
            # we only pass it if the perform method requires it. This is also
            # useful as Traits UI controllers *never* require the event.
            argspec = getfullargspec(self.controller.perform)

            # If the only arguments are 'self' and 'action' then don't pass
            # the event!
            if len(argspec.args) == 2:
                self.controller.perform(action)

            else:
                self.controller.perform(action, action_event)

        else:
            self.checked = action.checked = self.control.isChecked()

            # Most of the time, action's do no care about the event (it
            # contains information about the time the event occurred etc), so
            # we only pass it if the perform method requires it.
            argspec = getfullargspec(action.perform)

            # If the only argument is 'self' then don't pass the event!
            if len(argspec.args) == 1:
                action.perform()

            else:
                action.perform(action_event)

    # Trait event handlers -------------------------------------------------

    def _enabled_changed(self):
        """ Called when our 'enabled' trait is changed. """
        if self.control is not None:
            self.control.setEnabled(self.enabled)

    def _visible_changed(self):
        """ Called when our 'visible' trait is changed. """
        if self.control is not None:
            self.control.setVisible(self.visible)

    def _checked_changed(self):
        """ Called when our 'checked' trait is changed. """
        if self.control is not None:
            self.control.setChecked(self.checked)

    def _on_action_enabled_changed(self, event):
        """ Called when the enabled trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setEnabled(action.enabled)

    def _on_action_visible_changed(self, event):
        """ Called when the visible trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setVisible(action.visible)

    def _on_action_checked_changed(self, event):
        """ Called when the checked trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setChecked(action.checked)

    def _on_action_name_changed(self, event):
        """ Called when the name trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setText(action.name)

    def _on_action_accelerator_changed(self, event):
        """ Called when the accelerator trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setShortcut(action.accelerator)

    def _on_action_image_changed(self, event):
        """ Called when the accelerator trait is changed on an action. """
        action = event.object
        if self.control is not None:
            size = self.tool_bar.iconSize()
            self.control.setIcon(
                action.image.create_icon((size.width(), size.height()))
            )

    def _on_action_tooltip_changed(self, event):
        """ Called when the accelerator trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.setToolTip(action.tooltip)


class _PaletteTool(HasTraits):
    """ A tool palette representation of an action item. """

    # '_PaletteTool' interface ---------------------------------------------

    # The radio group we are part of (None if the tool is not part of such a
    # group).
    group = Any()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, tool_palette, image_cache, item, show_labels):
        """ Creates a new tool palette tool for an action item. """

        self.item = item
        self.tool_palette = tool_palette

        action = self.item.action
        label = action.name

        if action.style == "widget":
            raise NotImplementedError(
                "Qt does not support widgets in palettes"
            )

        # Tool palette tools never have '...' at the end.
        if label.endswith("..."):
            label = label[:-3]

        # And they never contain shortcuts.
        label = label.replace("&", "")

        path = action.image.absolute_path
        bmp = image_cache.get_bitmap(path)

        kind = action.style
        tooltip = action.tooltip
        longtip = action.description

        if not show_labels:
            label = ""

        # Add the tool to the tool palette.
        self.tool_id = tool_palette.add_tool(
            label, bmp, kind, tooltip, longtip
        )
        tool_palette.toggle_tool(self.tool_id, action.checked)
        tool_palette.enable_tool(self.tool_id, action.enabled)
        tool_palette.on_tool_event(self.tool_id, self._on_tool)

        # Listen to the trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        action.observe(self._on_action_enabled_changed, "enabled")
        action.observe(self._on_action_checked_changed, "checked")

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    # Trait event handlers -------------------------------------------------

    def _on_action_enabled_changed(self, event):
        """ Called when the enabled trait is changed on an action. """
        action = event.object
        self.tool_palette.enable_tool(self.tool_id, action.enabled)

    def _on_action_checked_changed(self, event):
        """ Called when the checked trait is changed on an action. """
        action = event.object
        if action.style == "radio":
            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if event.new:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False

        # This will *not* emit a tool event.
        self.tool_palette.toggle_tool(self.tool_id, event.new)

        return

    # Tool palette event handlers -----------------------------------------#

    def _on_tool(self, event):
        """ Called when the tool palette button is clicked. """

        action = self.item.action
        action_event = ActionEvent()

        # Perform the action!
        action.checked = self.tool_palette.get_tool_state(self.tool_id) == 1
        action.perform(action_event)

        return

    def dispose(self):
        action = self.item.action
        action.observe(self._on_action_enabled_changed, "enabled", remove=True)
        action.observe(self._on_action_checked_changed, "checked", remove=True)
