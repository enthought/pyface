#------------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
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
""" Module to handle drag-drop on widgets.
Work-in-progress, interface may change without warnings. """

# System library imports
import wx

# Enthought library imports
from pyface.drop_handler import DragEvent, PyMimeData, BaseDropHandler
from pyface.ui.wx.clipboard import PythonObject
from pyface.wx.drag_and_drop import clipboard


drop_action_map = {'copy':wx.DragCopy,
                   'move':wx.DragMove,
                   'link':wx.DragLink,
                   None: wx.DragNone
                   }

inv_drop_action_map = {value:key for key,value in drop_action_map.items()}



class _DropEventHandler(wx.PyDropTarget):
    def __init__(self, widget):
        super(_DropEventHandler, self).__init__()

        self.target = None
        self.widget = widget

        self._drop_evt = None
        self._handler = None
        self._handlers = []

        # Specify the type of data we will accept.
        self.data_object = wx.DataObjectComposite()
        self.data = wx.CustomDataObject(PythonObject)
        self.data_object.Add(self.data, preferred=True)
        self.SetDataObject(self.data_object)

    def OnDragOver(self, x, y, default):
        self._handler = self._drop_evt = None
        data = PyMimeData.coerce(self.GetDataObject())
        data.set_instance(clipboard.data)
        evt = DragEvent(data=data, target=self.target,
                        widget=self.widget, source=self.widget)
        for handler in self._handlers:
            if handler.can_handle_drop(evt):
                self._drop_evt = evt
                self._handler = handler
                if evt._action is None:
                    return default
                else:
                    return drop_action_map[evt._action]
        return drop_action_map[None]

    def OnData(self, x, y, default):
        """ Called when OnDrop returns True. """
        evt = self._drop_evt
        if evt is None:
            return drop_action_map[None]
        try:
            evt.source = self.widget
            self._handler.handle_drop(evt)
        finally:
            self._handler = self._drop_evt = None
            return drop_action_map[evt._action]

    def OnLeave(self):
        """ Called when the mouse leaves the drop target. """
        pass

    def OnDrop(self, x, y):
        """ Called when the user drops a data object on the target.

        Return 'False' to veto the operation.

        """
        return True

    def add_handler(self, handler):
        self._handlers.append(handler)


def _get_emitter_for_widget(widget):
    drop_target = widget.GetDropTarget()
    if drop_target is None:
        drop_target = _DropEventHandler(widget)
        widget.SetDropTarget(drop_target)
        return drop_target
    elif isinstance(drop_target, _DropEventHandler):
        return drop_target
    else:
        raise RuntimeError('Cannot set DropTarget on widget which already has '
                           'it set: %s'%widget)


def set_drop_target(widget, target):
    """ Sets the drop target for the given widget. """
    emitter = _get_emitter_for_widget(widget)
    emitter.target = target


def add_drop_handler(widget, drop_handler):
    """ Add drop handler to widget.

    Parameters
    ----------
    widget - The widget on which drop events are listened for.
    handler - The drop handler to add.

    """
    emitter = _get_emitter_for_widget(widget)
    emitter.add_handler(drop_handler)


if __name__ == '__main__':
    from pyface.wx.drag_and_drop import PythonDropSource, PythonDropTarget
    app = wx.PySimpleApp(0)

    drag_data = 'foo-bar-baz'

    frame = wx.Frame(None, -1, "")
    text_ctrl = wx.TextCtrl(frame, -1, "", style=wx.TE_MULTILINE)
    def on_drop():
        print 'drop 1'
    text_ctrl.SetDropTarget(PythonDropTarget(on_drop))


    def can_handle_drop(evt):
        print 'can_drop'
        return True
    def handle_drop(evt):
        print 'drop 2', evt.data.formats()
        text_ctrl.Clear()
        for format in evt.data.formats():
            text_ctrl.WriteText('format: %s\n'%evt.data.data(format))
    text_ctrl_2 = wx.TextCtrl(frame, -1, "", style=wx.TE_MULTILINE)
    drop_handler = BaseDropHandler(on_can_handle=can_handle_drop,
                                   on_handle=handle_drop)
    add_drop_handler(text_ctrl_2, drop_handler)


    button = wx.StaticText(frame, -1, label='Drag Me')
    def start_drag(evt):
        print 'starting drag'
        PythonDropSource(button, drag_data)

    button.Bind(wx.EVT_LEFT_DOWN, start_drag)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(text_ctrl, 0, wx.EXPAND, 0)
    sizer.Add(button, 1, wx.EXPAND, 0)
    sizer.Add(text_ctrl_2, 2, wx.EXPAND, 0)
    frame.SetSizer(sizer)
    sizer.Fit(frame)
    text_ctrl.SetSize((400,400))
    frame.SetSize((400,400))
    frame.Layout()

    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()

