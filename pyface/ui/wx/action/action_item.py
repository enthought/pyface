# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The wx specific implementations the action manager internal classes.
"""


from inspect import getfullargspec


import wx


from traits.api import Any, Bool, HasTraits


from pyface.action.action_event import ActionEvent


_STYLE_TO_KIND_MAP = {
    "push": wx.ITEM_NORMAL,
    "radio": wx.ITEM_RADIO,
    "toggle": wx.ITEM_CHECK,
    "widget": None,
}


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

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, menu, item, controller):
        """ Creates a new menu item for an action item. """

        self.item = item

        # Create an appropriate menu item depending on the style of the action.
        #
        # N.B. Don't try to use -1 as the Id for the menu item... wx does not
        # like it!
        action = item.action
        label = action.name
        kind = _STYLE_TO_KIND_MAP[action.style]
        longtip = action.description or action.tooltip

        if action.style == "widget":
            raise NotImplementedError(
                "WxPython does not support widgets in menus"
            )

        if len(action.accelerator) > 0:
            label = label + "\t" + action.accelerator

        # This just helps with debugging when people forget to specify a name
        # for their action (without this wx just barfs which is not very
        # helpful!).
        if len(label) == 0:
            label = item.action.__class__.__name__

        if getattr(action, "menu_role", False):
            if action.menu_role == "About":
                self.control_id = wx.ID_ABOUT
            elif action.menu_role == "Preferences":
                self.control_id = wx.ID_PREFERENCES
            elif action.menu_role == "Quit":
                self.control_id = wx.ID_EXIT
        else:
            self.control_id = wx.ID_ANY
        self.control = wx.MenuItem(menu, self.control_id, label, longtip, kind)

        # If the action has an image then display it.
        if action.image is not None:
            try:
                self.control.SetBitmap(action.image.create_bitmap())
            except Exception:
                # Some platforms don't allow radio buttons to have
                # bitmaps, so just ignore the exception if it happens
                pass

        menu.Append(self.control)
        menu.menu_items.append(self)

        # Set the initial enabled/disabled state of the action.
        self.control.Enable(action.enabled and action.visible)

        # Set the initial checked state.
        if action.style in ["radio", "toggle"]:
            self.control.Check(action.checked)

        # Wire it up...create an ugly flag since some platforms dont skip the
        # event when we thought they would
        self._skip_menu_event = False
        parent.Bind(wx.EVT_MENU, self._on_menu, self.control)

        # Listen for trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        action.observe(self._on_action_enabled_changed, "enabled")
        action.observe(self._on_action_visible_changed, "visible")
        action.observe(self._on_action_checked_changed, "checked")
        action.observe(self._on_action_name_changed, "name")
        action.observe(self._on_action_image_changed, "image")

        if controller is not None:
            self.controller = controller
            controller.add_to_menu(self)

    def dispose(self):
        action = self.item.action
        action.observe(self._on_action_enabled_changed, "enabled", remove=True)
        action.observe(self._on_action_visible_changed, "visible", remove=True)
        action.observe(self._on_action_checked_changed, "checked", remove=True)
        action.observe(self._on_action_name_changed, "name", remove=True)
        action.observe(self._on_action_image_changed, "image", remove=True)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    # Trait event handlers -------------------------------------------------

    def _enabled_changed(self):
        """ Called when our 'enabled' trait is changed. """

        self.control.Enable(self.enabled and self.visible)

    def _visible_changed(self):
        """ Called when our 'visible' trait is changed. """

        self.control.Enable(self.visible and self.enabled)

    def _checked_changed(self):
        """ Called when our 'checked' trait is changed. """

        if self.item.action.style == "radio":
            # fixme: Not sure why this is even here, we had to guard it to
            # make it work? Must take a look at svn blame!
            # FIXME v3: Note that menu_checked() doesn't seem to exist, so we
            # comment it out and do the following instead.
            # if self.group is not None:
            #    self.group.menu_checked(self)

            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if self.checked:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False

        self.control.Check(self.checked)

    def _on_action_enabled_changed(self, event):
        """ Called when the enabled trait is changed on an action. """
        action = event.object
        self.control.Enable(action.enabled and action.visible)

    def _on_action_visible_changed(self, event):
        """ Called when the visible trait is changed on an action. """
        action = event.object
        self.control.Enable(action.visible and action.enabled)

    def _on_action_checked_changed(self, event):
        """ Called when the checked trait is changed on an action. """
        action = event.object
        if self.item.action.style == "radio":
            # fixme: Not sure why this is even here, we had to guard it to
            # make it work? Must take a look at svn blame!
            # FIXME v3: Note that menu_checked() doesn't seem to exist, so we
            # comment it out and do the following instead.
            # if self.group is not None:
            #    self.group.menu_checked(self)

            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if action.checked:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False

        # This will *not* emit a menu event because of this ugly flag
        self._skip_menu_event = True
        self.control.Check(action.checked)
        self._skip_menu_event = False

    def _on_action_name_changed(self, event):
        """ Called when the name trait is changed on an action. """
        action = event.object
        label = action.name
        if len(action.accelerator) > 0:
            label = label + "\t" + action.accelerator
        self.control.SetText(label)

    def _on_action_image_changed(self, event):
        """ Called when the name trait is changed on an action. """
        action = event.object
        if self.control is not None:
            self.control.SetIcon(action.image.create_icon())

        return

    # wx event handlers ----------------------------------------------------

    def _on_menu(self, event):
        """ Called when the menu item is clicked. """

        # if the ugly flag is set, do not perform the menu event
        if self._skip_menu_event:
            return

        action = self.item.action
        action_event = ActionEvent()

        is_checkable = action.style in ["radio", "toggle"]

        # Perform the action!
        if self.controller is not None:
            if is_checkable:
                # fixme: There is a difference here between having a controller
                # and not in that in this case we do not set the checked state
                # of the action! This is confusing if you start off without a
                # controller and then set one as the action now behaves
                # differently!
                self.checked = self.control.IsChecked() == 1

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
                action.checked = self.control.IsChecked() == 1

            # Most of the time, action's do no care about the event (it
            # contains information about the time the event occurred etc), so
            # we only pass it if the perform method requires it.
            argspec = getfullargspec(action.perform)

            # If the only argument is 'self' then don't pass the event!
            if len(argspec.args) == 1:
                action.perform()

            else:
                action.perform(action_event)


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

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(
        self, parent, tool_bar, image_cache, item, controller, show_labels
    ):
        """ Creates a new tool bar tool for an action item. """

        self.item = item
        self.tool_bar = tool_bar

        # Create an appropriate tool depending on the style of the action.
        action = self.item.action
        label = action.name

        # Tool bar tools never have '...' at the end!
        if label.endswith("..."):
            label = label[:-3]

        # And they never contain shortcuts.
        label = label.replace("&", "")

        # If the action has an image then convert it to a bitmap (as required
        # by the toolbar).
        if action.image is not None:
            image = action.image.create_image(
                self.tool_bar.GetToolBitmapSize()
            )
            path = action.image.absolute_path
            bmp = image_cache.get_bitmap(path)

        else:
            from pyface.api import ImageResource

            image = ImageResource("image_not_found")
            bmp = image.create_bitmap()

        kind = _STYLE_TO_KIND_MAP[action.style]
        tooltip = action.tooltip
        longtip = action.description

        if not show_labels:
            label = ""

        else:
            self.tool_bar.SetSize((-1, 50))

        if action.style == "widget":
            widget = action.create_control(self.tool_bar)
            self.control = tool_bar.AddControl(widget, label)
            self.control_id = self.control.GetId()
        else:
            self.control = tool_bar.AddTool(
                wx.ID_ANY,
                label,
                bmp,
                wx.NullBitmap,
                kind,
                tooltip,
                longtip,
                None,
            )
            self.control_id = self.control.GetId()

            # Set the initial checked state.
            tool_bar.ToggleTool(self.control_id, action.checked)

            if hasattr(tool_bar, "ShowTool"):
                # Set the initial enabled/disabled state of the action.
                tool_bar.EnableTool(self.control_id, action.enabled)

                # Set the initial visibility
                tool_bar.ShowTool(self.control_id, action.visible)
            else:
                # Set the initial enabled/disabled state of the action.
                tool_bar.EnableTool(
                    self.control_id, action.enabled and action.visible
                )

            # Wire it up.
            parent.Bind(wx.EVT_TOOL, self._on_tool, self.control)

        # Listen for trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        action.observe(self._on_action_enabled_changed, "enabled")
        action.observe(self._on_action_visible_changed, "visible")
        action.observe(self._on_action_checked_changed, "checked")

        if controller is not None:
            self.controller = controller
            controller.add_to_toolbar(self)

    def dispose(self):
        action = self.item.action
        action.observe(self._on_action_enabled_changed, "enabled", remove=True)
        action.observe(self._on_action_visible_changed, "visible", remove=True)
        action.observe(self._on_action_checked_changed, "checked", remove=True)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    # Trait event handlers -------------------------------------------------

    def _enabled_changed(self):
        """ Called when our 'enabled' trait is changed. """

        if hasattr(self.tool_bar, "ShowTool"):
            self.tool_bar.EnableTool(self.control_id, self.enabled)
        else:
            self.tool_bar.EnableTool(
                self.control_id, self.enabled and self.visible
            )

    def _visible_changed(self):
        """ Called when our 'visible' trait is changed. """

        if hasattr(self.tool_bar, "ShowTool"):
            self.tool_bar.ShowTool(self.control_id, self.visible)
        else:
            self.tool_bar.EnableTool(
                self.control_id, self.enabled and self.visible
            )

    def _checked_changed(self):
        """ Called when our 'checked' trait is changed. """

        if self.item.action.style == "radio":
            # FIXME v3: Note that toolbar_checked() doesn't seem to exist, so
            # we comment it out and do the following instead.
            # self.group.toolbar_checked(self)

            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if self.checked:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False

        self.tool_bar.ToggleTool(self.control_id, self.checked)

    def _on_action_enabled_changed(self, event):
        """ Called when the enabled trait is changed on an action. """
        action = event.object
        if hasattr(self.tool_bar, "ShowTool"):
            self.tool_bar.EnableTool(self.control_id, action.enabled)
        else:
            self.tool_bar.EnableTool(
                self.control_id, action.enabled and action.visible
            )

    def _on_action_visible_changed(self, event):
        """ Called when the visible trait is changed on an action. """
        action = event.object
        if hasattr(self.tool_bar, "ShowTool"):
            self.tool_bar.ShowTool(self.control_id, action.visible)
        else:
            self.tool_bar.EnableTool(
                self.control_id, self.enabled and action.visible
            )

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
        self.tool_bar.ToggleTool(self.control_id, event.new)

        return

    # wx event handlers ----------------------------------------------------

    def _on_tool(self, event):
        """ Called when the tool bar tool is clicked. """

        action = self.item.action
        action_event = ActionEvent()

        # Perform the action!
        if self.controller is not None:
            # fixme: There is a difference here between having a controller
            # and not in that in this case we do not set the checked state
            # of the action! This is confusing if you start off without a
            # controller and then set one as the action now behaves
            # differently!
            self.checked = self.tool_bar.GetToolState(self.control_id) == 1

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
            action.checked = self.tool_bar.GetToolState(self.control_id) == 1

            # Most of the time, action's do no care about the event (it
            # contains information about the time the event occurred etc), so
            # we only pass it if the perform method requires it.
            argspec = getfullargspec(action.perform)

            # If the only argument is 'self' then don't pass the event!
            if len(argspec.args) == 1:
                action.perform()

            else:
                action.perform(action_event)


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
                "WxPython does not support widgets in palettes"
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

    def dispose(self):
        action = self.item.action
        action.observe(self._on_action_enabled_changed, "enabled", remove=True)
        action.observe(self._on_action_checked_changed, "checked", remove=True)

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
