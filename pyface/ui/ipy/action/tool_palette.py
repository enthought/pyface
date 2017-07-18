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
""" View of an ActionManager drawn as a rectangle of buttons. """

from pyface.widget import Widget

from traits.api import Bool, Dict, Int, List, Tuple


class ToolPalette(Widget):

    tools = List

    id_tool_map = Dict

    tool_id_to_button_map = Dict

    button_size = Tuple((25, 25), Int, Int)

    is_realized = Bool(False)

    tool_listeners = Dict

    # Maps a button id to its tool id.
    button_tool_map = Dict

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, parent, **traits):
        """ Creates a new tool palette. """

        # Base class constructor.
        super(ToolPalette, self).__init__(**traits)

        # Create the toolkit-specific control that represents the widget.
        self.control = self._create_control(parent)

        return

    ###########################################################################
    # ToolPalette interface.
    ###########################################################################

    def add_tool(self, label, bmp, kind, tooltip, longtip):
        """ Add a tool with the specified properties to the palette.

        Return an id that can be used to reference this tool in the future.
        """

        return 1

    def toggle_tool(self, id, checked):
        """ Toggle the tool identified by 'id' to the 'checked' state.

        If the button is a toggle or radio button, the button will be checked
        if the 'checked' parameter is True; unchecked otherwise.  If the button
        is a standard button, this method is a NOP.
        """
        return

    def enable_tool(self, id, enabled):
        """ Enable or disable the tool identified by 'id'. """
        return

    def on_tool_event(self, id, callback):
        """ Register a callback for events on the tool identified by 'id'. """
        return

    def realize(self):
        """ Realize the control so that it can be displayed. """
        return

    def get_tool_state(self, id):
        """ Get the toggle state of the tool identified by 'id'. """
        state = 0

        return state


    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_control(self, parent):
        return None


#### EOF ######################################################################
