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

# Major package imports.
import wx


STYLE_TO_KIND_MAP = {
    'push'   : wx.ITEM_NORMAL,
    'radio'  : wx.ITEM_RADIO,
    'toggle' : wx.ITEM_CHECK
}


class _MenuItem_wx(object):
    """ The _MenuItem monkey patch for wx. """

    ###########################################################################
    # '_MenuItem' toolkit interface.
    ###########################################################################

    def _tk__menuitem_create(self, parent, menu):
        """ Create a menu item to be added to a menu. """

        # Create an appropriate menu item depending on the style of the action.
        #
        # N.B. Don't try to use -1 as the Id for the menu item... wx does not
        # ---- like it!
        action  = self.item.action
        label   = action.name
        kind    = STYLE_TO_KIND_MAP[action.style]
        longtip = action.description

        if len(action.accelerator) > 0:
            label = label + '\t' + action.accelerator
        
        self.control_id = wx.NewId()
        control = wx.MenuItem(menu, self.control_id, label, longtip, kind)
        menu.AppendItem(control)
        
        # Set the initial enabled/disabled state of the action.
        control.Enable(action.enabled)

        # Set the initial checked state.
        if action.style in ['radio', 'toggle']:
            control.Check(action.checked)    
        
        # Wire it up...create an ugly flag since some platforms dont skip the
        # event when we thought they would
        self._wx_skip_menu_event = False
        wx.EVT_MENU(parent, self.control_id, self._wx_on_menu)

        return control

    def _tk__menuitem_set_enabled(self, enabled):
        """ Set the enabled state of a menu item. """

        self.control.Enable(enabled)

        return

    def _tk__menuitem_set_checked(self, checked):
        """ Set the checked state of a menu item. """

        if self.item.action.style == 'radio':
            # fixme: Not sure why this is even here, we had to guard it to
            # make it work? Must take a look at svn blame!
            # ZZZ: Note that menu_checked() doesn't seem to exist, so we
            # comment it out and do the following instead.
            #if self.group is not None:
            #    self.group.menu_checked(self)

            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if checked:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False
                        
        # This will *not* emit a menu event because of this ugly flag
        self._wx_skip_menu_event = True
        self.control.Check(checked)
        self._wx_skip_menu_event = False
            
        return

    def _tk__menuitem_get_checked(self):
        """ Get the checked state of a menu item. """

        return self.control.IsChecked() == 1

    def _tk__menuitem_set_named(self, name):
        """ Set the name of a menu item. """

        self.control.SetText(name)

        return

    #### wx event handlers ####################################################

    def _wx_on_menu(self, event):
        """ Called when the menu item is clicked. """

        # if the ugly flag is set, do not perform the menu event
        if self._wx_skip_menu_event:
            return
        
        self._handle_tk__menuitem_clicked()

        return


class _Tool_wx(object):
    """ The _Tool monkey patch for wx. """

    ###########################################################################
    # '_Tool' toolkit interface.
    ###########################################################################

    def _tk__tool_create(self, parent, image_cache, show_labels):
        """ Create a tool to be added to a tool bar. """

        # Create an appropriate tool depending on the style of the action.
        action  = self.item.action
        label   = action.name

        # Tool bar tools never have '...' at the end!
        if label.endswith('...'):
            label = label[:-3]

        # And they never contain shortcuts.
        label = label.replace('&', '')

        image = action.image.create_image(self.tool_bar.GetToolBitmapSize())
        bmp   = image_cache.get_bitmap(action.image.absolute_path)

        kind    = STYLE_TO_KIND_MAP[action.style]
        tooltip = action.tooltip
        longtip = action.description

        if not show_labels:
            label = ''

        else:
            self.tool_bar.SetSize((-1, 50))
            
        self.control_id = wx.NewId()
        control = self.tool_bar.AddLabelTool(
            self.control_id, label, bmp, wx.NullBitmap, kind, tooltip, longtip
        )

        # Set the initial checked state.
        self.tool_bar.ToggleTool(self.control_id, action.checked)

        # Set the initial enabled/disabled state of the action.
        self.tool_bar.EnableTool(self.control_id, action.enabled)
            
        # Wire it up.
        wx.EVT_TOOL(parent, self.control_id, self._wx_on_tool)

        return control

    def _tk__tool_set_enabled(self, enabled):
        """ Set the enabled state of a tool bar tool. """

        self.tool_bar.EnableTool(self.control_id, enabled)

        return

    def _tk__tool_set_checked(self, checked):
        """ Set the checked state of a tool bar tool. """

        if self.item.action.style == 'radio':
            # ZZZ: Note that toolbar_checked() doesn't seem to exist, so we
            # comment it out and do the following instead.
            #self.group.toolbar_checked(self)

            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if checked:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False

        # This will *not* emit a tool event.
        self.tool_bar.ToggleTool(self.control_id, checked)

        return

    def _tk__tool_get_checked(self):
        """ Get the checked state of a tool bar tool. """

        return self.tool_bar.GetToolState(self.control_id) == 1

    #### wx event handlers ####################################################

    def _wx_on_tool(self, event):
        """ Called when the tool bar tool is clicked. """

        self._handle_tk__tool_clicked()

        return

#### EOF ######################################################################
