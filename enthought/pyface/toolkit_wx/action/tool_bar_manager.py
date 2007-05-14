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

# Major package imports.
import wx


class ToolBarManager_wx(object):
    """ The ToolBarManager monkey patch for wx. """

    ###########################################################################
    # 'ToolBarManager' toolkit interface.
    ###########################################################################

    def _tk_toolbarmanager_create_tool_bar(self, parent):
        """ Create a tool bar with the given parent. """

        # Determine the wx style for the tool bar based on any optional
        # settings.
        style = wx.NO_BORDER | wx.TB_FLAT | wx.CLIP_CHILDREN
        
        if self.show_tool_names:
            style |= wx.TB_TEXT

        if self.orientation == 'horizontal':
            style |= wx.TB_HORIZONTAL
        else:
            style |= wx.TB_VERTICAL
            
        if not self.show_divider:
            style |= wx.TB_NODIVIDER

        # Create the control.
        tool_bar = wx.ToolBar(parent, -1, style=style)
        
        # fixme: Setting the tool bitmap size seems to be the only way to
        # change the height of the toolbar in wx.
        tool_bar.SetToolBitmapSize(self.image_size)

        return tool_bar

    def _tk_toolbarmanager_add_separator(self, tool_bar):
        """ Add a separator to a toolbar. """

        tool_bar.AddSeparator()

        return

    def _tk_toolbarmanager_fixup(self, tool_bar):
        """ Handle any required fixups after the tool bar has been created. """

        # Make the tools appear in the tool bar (without this you will see
        # nothing!).
        tool_bar.Realize()

        # fixme: Without the following hack,  only the first item in a radio
        # group can be selected when the tool bar is first realised 8^()
        for group in self.groups:
            checked = False
            for item in group.items:
                # If the group is a radio group,  set the initial checked state
                # of every tool in it.
                if item.action.style == 'radio':
                    tool_bar.ToggleTool(item.control_id, item.action.checked)
                    checked = checked or item.action.checked

                # Every item in a radio group MUST be 'radio' style, so we
                # can just skip to the next group.
                else:
                    break

            # We get here if the group is a radio group.
            else:
                # If none of the actions in the group is specified as 'checked'
                # we will check the first one.
                if not checked and len(group.items) > 0:
                    group.items[0].action.checked = True
            
        return

#### EOF ######################################################################
