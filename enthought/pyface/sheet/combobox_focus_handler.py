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
""" Workaround for combobox focus problem in wx 2.6. """

# Major package imports
import wx

class ComboboxFocusHandler(wx.EvtHandler):
    
    def __init__(self):
        wx.EvtHandler.__init__(self)
        wx.EVT_KILL_FOCUS(self, self._on_kill_focus)
        return

    def _on_kill_focus(self, evt):

        # this is pretty egregious. somehow the combobox gives up focus
        # as soon as it starts up, causing the sheet to remove the editor.
        # so we just don't let it give up focus. i suspect this will cause
        # some other problem down the road, but it seems to work for now.
        # fixme: remove this h*ck once the bug is fixed in wx.
        editor = evt.GetEventObject()
        if isinstance(editor, wx._controls.ComboBox):
            return
        evt.Skip()
        return

#### EOF ####################################################################
