# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" View of an ActionManager drawn as a rectangle of buttons.
"""

import wx
from pyface.widget import Widget

from traits.api import Bool, Dict, Int, List, Tuple

# HTML templates.
# FIXME : Not quite the right color.
HTML = """

<html>
  <body bgcolor='#cccccc'>
    %s
  </body>
</html>

"""

PART = """<wxp module="wx" class="Panel"><param name="id" value="%s"><param name="size" value="%s"></wxp>"""


class ToolPalette(Widget):

    tools = List()

    id_tool_map = Dict()

    tool_id_to_button_map = Dict()

    button_size = Tuple((25, 25), Int, Int)

    is_realized = Bool(False)

    tool_listeners = Dict()

    # Maps a button id to its tool id.
    button_tool_map = Dict()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, **traits):
        """ Creates a new tool palette. """

        # Base class constructor.
        super().__init__(**traits)

        # Create the toolkit-specific control that represents the widget.
        self.control = self._create_control(parent)

        return

    # ------------------------------------------------------------------------
    # ToolPalette interface.
    # ------------------------------------------------------------------------

    def add_tool(self, label, bmp, kind, tooltip, longtip):
        """ Add a tool with the specified properties to the palette.

        Return an id that can be used to reference this tool in the future.
        """

        wxid = wx.NewIdRef()
        params = (wxid, label, bmp, kind, tooltip, longtip)
        self.tools.append(params)
        self.id_tool_map[wxid] = params

        if self.is_realized:
            self._reflow()

        return wxid

    def toggle_tool(self, id, checked):
        """ Toggle the tool identified by 'id' to the 'checked' state.

        If the button is a toggle or radio button, the button will be checked
        if the 'checked' parameter is True; unchecked otherwise.  If the button
        is a standard button, this method is a NOP.
        """

        button = self.tool_id_to_button_map.get(id, None)
        if button is not None and hasattr(button, "SetToggle"):
            button.SetToggle(checked)

    def enable_tool(self, id, enabled):
        """ Enable or disable the tool identified by 'id'. """

        button = self.tool_id_to_button_map.get(id, None)
        if button is not None:
            button.SetEnabled(enabled)

    def on_tool_event(self, id, callback):
        """ Register a callback for events on the tool identified by 'id'. """

        callbacks = self.tool_listeners.setdefault(id, [])
        callbacks.append(callback)

    def realize(self):
        """ Realize the control so that it can be displayed. """

        self.is_realized = True
        self._reflow()

    def get_tool_state(self, id):
        """ Get the toggle state of the tool identified by 'id'. """

        button = self.tool_id_to_button_map.get(id, None)
        if hasattr(button, "GetToggle"):
            if button.GetToggle():
                state = 1
            else:
                state = 0
        else:
            state = 0

        return state

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):

        html_window = wx.html.HtmlWindow(parent, -1, style=wx.CLIP_CHILDREN)

        return html_window

    def _reflow(self):
        """ Reflow the layout. """

        # Create a bit of html for each tool.
        parts = []
        for param in self.tools:
            parts.append(PART % (str(param[0]), self.button_size))

        # Create the entire html page.
        html = HTML % "".join(parts)

        # Set the HTML on the widget.  This will create all of the buttons.
        self.control.SetPage(html)

        for param in self.tools:
            self._initialize_tool(param)

    def _initialize_tool(self, param):
        """ Initialize the tool palette button. """

        wxid, label, bmp, kind, tooltip, longtip = param

        panel = self.control.FindWindowById(wxid)

        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        panel.SetWindowStyleFlag(wx.CLIP_CHILDREN)

        from wx.lib.buttons import GenBitmapToggleButton, GenBitmapButton

        if kind == "radio":
            button = GenBitmapToggleButton(
                panel, -1, None, size=self.button_size
            )

        else:
            button = GenBitmapButton(panel, -1, None, size=self.button_size)

        self.button_tool_map[button.GetId()] = wxid
        self.tool_id_to_button_map[wxid] = button
        panel.Bind(wx.EVT_BUTTON, self._on_button, button)
        button.SetBitmapLabel(bmp)
        button.SetToolTip(label)
        sizer.Add(button, 0, wx.EXPAND)

    def _on_button(self, event):

        button_id = event.GetId()
        tool_id = self.button_tool_map.get(button_id, None)
        if tool_id is not None:
            for listener in self.tool_listeners.get(tool_id, []):
                listener(event)

        return
