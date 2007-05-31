#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enth373ought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" An action manager item that represents an actual action. """


# Standard libary imports.
from inspect import getargspec

# Enthought library imports.
from enthought.traits.api import Any, Bool, HasTraits, Instance, List
from enthought.traits.api import Property, Str

# Private Enthought library imports.
from enthought.pyface.toolkit import patch_toolkit

# Local imports.
from action import Action
from action_event import ActionEvent
from action_manager_item import ActionManagerItem


class ActionItem(ActionManagerItem):
    """ An action manager item that represents an actual action. """

    #### 'ActionManagerItem' interface ########################################

    # The item's unique identifier ('unique' in this case means unique within
    # its group)
    id = Property(Str)

    #### 'ActionItem' interface ###############################################

    # The action!
    action = Instance(Action)

    # The toolkit specific control created for this item.
    control = Any

    # The toolkit specific Id of the control created for this item.
    #
    # We have to keep the Id as well as the control because wx tool bar tools
    # are created as 'wxObjectPtr's which do not have Ids, and the Id is
    # required to manipulate the state of a tool via the tool bar 8^(
    # FIXME v3: Why is this part of the public interface?
    control_id = Any
    
    #### Private interface ####################################################

    # All of the internal instances that wrap this item.
    _wrappers = List(Any)

    ###########################################################################
    # 'ActionManagerItem' interface.
    ###########################################################################

    def _get_id(self):
        """ Return's the item's Id. """

        return self.action.id
    
    ###########################################################################
    # 'ActionItem' interface.
    ###########################################################################

    def add_to_menu(self, parent, menu, controller):
        """ Adds the item to a menu. """

        if (controller is None) or controller.can_add_to_menu(self.action): 
            wrapper = _MenuItem(parent, menu, self, controller)

            # fixme: Martin, who uses this information?
            if controller is None:
                self.control = wrapper.control
                self.control_id = wrapper.control_id

            self._wrappers.append(wrapper)

        return

    def add_to_toolbar(self, parent, tool_bar, image_cache, controller,
                       show_labels=True):
        """ Adds the item to a tool bar. """

        if (controller is None) or controller.can_add_to_toolbar(self.action): 
            wrapper = _Tool(
                parent, tool_bar, image_cache, self, controller, show_labels
            )
            
            # fixme: Martin, who uses this information?
            if controller is None:
                self.control = wrapper.control
                self.control_id = wrapper.control_id

            self._wrappers.append(wrapper)

        return

    def add_to_palette(self, tool_palette, image_cache, show_labels=True):
        """ Adds the item to a tool palette. """
        
        wrapper = _PaletteTool(tool_palette, image_cache, self, show_labels)

        self._wrappers.append(wrapper)

        return

    def destroy(self):
        """ Called when the action is no longer required.

        By default this method calls 'destroy' on the action itself.
        """

        self.action.destroy()
        
        return


class _MenuItem(HasTraits):
    """ A menu item representation of an action item. """

    __tko__ = '_MenuItem'

    #### '_MenuItem' interface ################################################
    
    # Is the item checked?
    checked = Bool(False)

    # A controller object we delegate taking actions through (if any).
    controller = Any
    
    # Is the item enabled?
    enabled = Bool(True)
    
    # The radio group we are part of (None if the menu item is not part of such
    # a group).
    group = Any
    
    ###########################################################################
    # 'object' interface.
    ###########################################################################
    
    def __init__(self, parent, menu, item, controller):
        """ Creates a new menu item for an action item. """

        patch_toolkit(self)

        self.item = item

        self.control = self._tk__menuitem_create(parent, menu)
        
        # Listen for trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        item.action.on_trait_change(self._on_action_enabled_changed, 'enabled')
        item.action.on_trait_change(self._on_action_checked_changed, 'checked')
        item.action.on_trait_change(self._on_action_name_changed, 'name')

        if controller is not None:
            self.controller = controller
            controller.add_to_menu(self)

        return
    
    ###########################################################################
    # Private interface. 
    ###########################################################################

    def _handle_tk__menuitem_clicked(self):
        """ Called by the toolkit when the menu item has been clicked. """

        action = self.item.action
        action_event = ActionEvent()
        
        is_checkable = action.style in ['radio', 'toggle']
        
        # Perform the action!
        if self.controller is not None:
            if is_checkable:
                # fixme: There is a difference here between having a controller
                # and not in that in this case we do not set the checked state
                # of the action! This is confusing if you start off without a
                # controller and then set one as the action now behaves
                # differently!
                self.checked = self._tk__menuitem_get_checked()

            # fixme: the 'perform' method without taking an event is
            # deprecated!
            args, varargs, varkw, dflts = getargspec(self.controller.perform)

            # If the only arguments are 'self' and 'action' then this is the
            # DEPRECATED interface.
            if len(args) == 2:
                self.controller.perform(action)
            
            else:
                self.controller.perform(action, action_event)
            
        else:
            if is_checkable:
                action.checked = self._tk__menuitem_get_checked()
                
            # fixme: the 'perform' method without taking an event is
            # deprecated!
            args, varargs, varkw, dflts = getargspec(action.perform)

            # If the only argument is 'self' then this is the DEPRECATED 
            # interface.
            if len(args) == 1:
                action.perform()
            
            else:
                action.perform(action_event)

        return

    #### Trait event handlers #################################################

    def _enabled_changed(self):
        """ Called when our 'enabled' trait is changed. """

        self._tk__menuitem_set_enabled(self.enabled)

        return
            
    def _checked_changed(self):
        """ Called when our 'checked' trait is changed. """

        self._tk__menuitem_set_checked(self.checked)

        return
        
    def _on_action_enabled_changed(self, action, trait_name, old, new):
        """ Called when the enabled trait is changed on an action. """

        self._tk__menuitem_set_enabled(action.enabled)

        return
    
    def _on_action_checked_changed(self, action, trait_name, old, new):
        """ Called when the checked trait is changed on an action. """

        self._tk__menuitem_set_checked(action.checked)

        return

    def _on_action_name_changed(self, action, trait_name, old, new):
        """ Called when the name trait is changed on an action. """

        self._tk__menuitem_set_named(action.name)

        return

    ###########################################################################
    # '_MenuItem' toolkit interface.
    ###########################################################################

    def _tk__menuitem_create(self, parent, menu):
        """ Create a menu item to be added to a menu.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk__menuitem_set_enabled(self, enabled):
        """ Set the enabled state of a menu item.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk__menuitem_set_checked(self, checked):
        """ Set the checked state of a menu item.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk__menuitem_get_checked(self):
        """ Get the checked state of a menu item.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk__menuitem_set_named(self, name):
        """ Set the name of a menu item.
        
        This must be reimplemented.
        """

        raise NotImplementedError


class _Tool(HasTraits):
    """ A tool bar tool representation of an action item. """

    __tko__ = '_Tool'

    #### '_Tool' interface ####################################################
    
    # Is the item checked?
    checked = Bool(False)

    # A controller object we delegate taking actions through (if any).
    controller = Any

    # Is the item enabled?
    enabled = Bool(True)

    # The radio group we are part of (None if the tool is not part of such a
    # group).
    group = Any

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, parent, tool_bar, image_cache, item, controller,
                 show_labels):
        """ Creates a new tool bar tool for an action item. """

        patch_toolkit(self)

        self.item = item
        self.tool_bar = tool_bar
        
        self.control = self._tk__tool_create(parent, image_cache, show_labels)

        # Listen for trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        item.action.on_trait_change(self._on_action_enabled_changed, 'enabled')
        item.action.on_trait_change(self._on_action_checked_changed, 'checked')
        
        if controller is not None:
            self.controller = controller
            controller.add_to_toolbar(self)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _handle_tk__tool_clicked(self):
        """ Called by the toolkit when the tool bar tool has been clicked. """

        action = self.item.action
        action_event = ActionEvent()

        # Perform the action!
        if self.controller is not None:
            # fixme: There is a difference here between having a controller
            # and not in that in this case we do not set the checked state
            # of the action! This is confusing if you start off without a
            # controller and then set one as the action now behaves
            # differently!
            self.checked = self._tk__tool_get_checked()

            # fixme: the 'perform' method without taking an event is
            # deprecated!
            args, varargs, varkw, dflts = getargspec(self.controller.perform)

            # If the only argument is 'self' then this is the DEPRECATED 
            # interface.
            if len(args) == 2:
                self.controller.perform(action)
            
            else:
                self.controller.perform(action, action_event)
            
        else:
            action.checked = self._tk__tool_get_checked()

            # fixme: the 'stop' method without taking a context is deprecated!
            args, varargs, varkw, dflts = getargspec(action.perform)

            # If the only argument is 'self' then this is the DEPRECATED 
            # interface.
            if len(args) == 1:
                action.perform()
            
            else:
                action.perform(action_event)
        
        return

    #### Trait event handlers #################################################

    def _enabled_changed(self):
        """ Called when our 'enabled' trait is changed. """

        self._tk__tool_set_enabled(self.enabled)

        return
    
    def _checked_changed(self):
        """ Called when our 'checked' trait is changed. """

        self._tk__tool_set_checked(self.checked)

        return

    def _on_action_enabled_changed(self, action, trait_name, old, new):
        """ Called when the enabled trait is changed on an action. """

        self._tk__tool_set_enabled(action.enabled)

        return
    
    def _on_action_checked_changed(self, action, trait_name, old, new):
        """ Called when the checked trait is changed on an action. """

        self._tk__tool_set_checked(action.checked)

        return

    ###########################################################################
    # '_Tool' toolkit interface.
    ###########################################################################

    def _tk__tool_create(self, parent, image_cache, show_labels):
        """ Create a tool to be added to a tool bar.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk__tool_set_enabled(self, enabled):
        """ Set the enabled state of a tool bar tool.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk__tool_set_checked(self, checked):
        """ Set the checked state of a tool bar tool.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk__tool_get_checked(self):
        """ Get the checked state of a tool bar tool.
        
        This must be reimplemented.
        """

        raise NotImplementedError


class _PaletteTool(HasTraits):
    """ A tool palette representation of an action item. """

    #### '_PaletteTool' interface #############################################
    
    # The radio group we are part of (None if the tool is not part of such a
    # group).
    group = Any

    # ZZZ: This hasn't been migrated to PyQt yet.
    def __init__(self, tool_palette, image_cache, item, show_labels):
        """ Creates a new tool palette tool for an action item. """

        self.item = item
        self.tool_palette = tool_palette

        action = self.item.action
        label = action.name

        # Tool palette tools never have '...' at the end.
        if label.endswith('...'):
            label = label[:-3]

        # And they never contain shortcuts.
        label = label.replace('&', '')

        image = action.image.create_image()
        path = action.image.absolute_path
        bmp = image_cache.get_bitmap(path)

        kind    = action.style
        tooltip = action.tooltip
        longtip = action.description

        if not show_labels:
            label = ''

        # Add the tool to the tool palette.
        self.tool_id = tool_palette.add_tool(label, bmp, kind, tooltip,longtip)
        tool_palette.toggle_tool(self.tool_id, action.checked)
        tool_palette.enable_tool(self.tool_id, action.enabled)
        tool_palette.on_tool_event(self.tool_id, self._on_tool)

        # Listen to the trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        action.on_trait_change(self._on_action_enabled_changed, 'enabled')
        action.on_trait_change(self._on_action_checked_changed, 'checked')

        return
        
    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait event handlers #################################################

    def _on_action_enabled_changed(self, action, trait_name, old, new):
        """ Called when the enabled trait is changed on an action. """

        self.tool_palette.enable_tool(self.tool_id, action.enabled)

        return
    
    def _on_action_checked_changed(self, action, trait_name, old, new):
        """ Called when the checked trait is changed on an action. """

        if action.style == 'radio':
            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if new:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False

        # This will *not* emit a tool event.
        self.tool_palette.toggle_tool(self.tool_id, new)
                
        return

    #### Tool palette event handlers ##########################################

    def _on_tool(self, event):
        """ Called when the tool palette button is clicked. """

        action = self.item.action

        is_checkable = (action.style == 'radio' or action.style == 'check')

        # Perform the action!
        action.checked = self.tool_palette.get_tool_state(self.tool_id) == 1
        action.perform()

        return
    
#### EOF ######################################################################
