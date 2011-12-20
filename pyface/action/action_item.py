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


# Enthought library imports.
from traits.api import Any, Instance, List, Property, Str, on_trait_change

# Local imports.
from action import Action
from action_manager_item import ActionManagerItem

# Import the toolkit specific versions of the internal classes.
from pyface.toolkit import toolkit_object
_MenuItem = toolkit_object('action.action_item:_MenuItem')
_Tool = toolkit_object('action.action_item:_Tool')
_PaletteTool = toolkit_object('action.action_item:_PaletteTool')


class ActionItem(ActionManagerItem):
    """ An action manager item that represents an actual action. """

    #### 'ActionManagerItem' interface ########################################

    # The item's unique identifier ('unique' in this case means unique within
    # its group).
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

    #### Trait properties #####################################################

    def _get_id(self):
        """ Return's the item's Id. """

        return self.action.id

    #### Trait change handlers ################################################

    def _enabled_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self.action.enabled = new

        return

    def _visible_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        self.action.visible = True

        return

    @on_trait_change('_wrappers.control')
    def _on_destroy(self, object, name, old, new):
        """ Handle the destruction of the wrapper.
        """
        if name == 'control' and new is None:
            self._wrappers.remove(object)

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

#### EOF ######################################################################
