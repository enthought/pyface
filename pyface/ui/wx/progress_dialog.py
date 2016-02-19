#------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: Enthought, Inc.
#
#------------------------------------------------------------------------------

""" A simple progress bar intended to run in the UI thread
"""

import wx
import time

# Enthought library imports
from traits.api import Bool, Enum, Instance, Int, Property, provides, Str

# Local imports
from pyface.i_progress_dialog import IProgressDialog, MProgressDialog
from .widget import Widget
from .window import Window

class ProgressBar(Widget):
    """ A simple progress bar dialog intended to run in the UI thread """

    #: The progress bar's parent control.
    parent = Instance(wx.Window)

    #: The progress bar's control.
    control = Instance(wx.Gauge)

    #: The orientation of the progress bar.
    direction = Enum('horizontal', 'horizontal', 'vertical')

    #: The maximum value for the progress bar.
    _max = Int

    def __init__(self, parent, minimum=0, maximum=100, direction='horizontal',
                 size=(200, -1)):
        """
        Constructs a progress bar which can be put into a panel, or optionaly,
        its own window

        """
        self._max = maximum
        self.parent = parent

        style = wx.GA_HORIZONTAL
        if direction == "vertical":
            style = wx.GA_VERTICAL

        self.control = wx.Gauge(parent, -1, maximum, style=style, size=size)

    def update(self, value):
        """ Update the progress bar to the desired value. """
        if self._max == 0:
            self.control.Pulse()
        else:
            self.control.SetValue(value)

        self.control.Update()

    def _show(self):
        # Show the parent
        self.parent.Show()

        # Show the toolkit-specific control in the parent
        self.control.Show()


class ProgressDialog(MProgressDialog, Window):
    """ A simple progress dialog window which allows itself to be updated """

    #: The progress bar
    progress_bar = Instance(ProgressBar)

    #: The window title
    title = Str

    #: The text message to display in the dialog
    message = Property()

    #: The minimum value of the progress range
    min = Int

    #: The minimum value of the progress range
    max = Int

    #: The margin around the progress bar
    margin = Int(5)

    #: Whether or not the progress dialog can be cancelled
    can_cancel = Bool(False)

    #: Whether or not to show the time taken
    show_time = Bool(False)

    #: Whether or not to show the percent completed
    show_percent = Bool(False)

    #: Whether or not the dialog was cancelled by the user
    _user_cancelled = Bool(False)

    #: The text of the message label
    _message_text = Str()

    #: The size of the dialog
    dialog_size = Instance(wx.Size)

    # Label for the 'cancel' button
    cancel_button_label = Str('Cancel')

    #: The widget showing the message text
    _message_control = Instance(wx.StaticText)

    #: The widget showing the time elapsed
    _elapsed_control = Instance(wx.StaticText)

    #: The widget showing the estimated time to completion
    _estimated_control = Instance(wx.StaticText)

    #: The widget showing the estimated time remaining
    _remaining_control = Instance(wx.StaticText)

    def __init__(self, *args, **kw):
        if 'message' in kw:
            self._message_text = kw.pop('message')

        # initialize the start time in case some tries updating
        # before open() is called
        self._start_time = 0

        super(ProgressDialog, self).__init__( *args, **kw)

    #-------------------------------------------------------------------------
    # IWindow Interface
    #-------------------------------------------------------------------------

    def open(self):
        """ Opens the window. """
        super(ProgressDialog, self).open()
        self._start_time = time.time()
        wx.GetApp().Yield(True)

    def close(self):
        """ Closes the window. """
        if self.progress_bar is not None:
            self.progress_bar.destroy()
            self.progress_bar = None

        if self._message_control is not None:
            self._message_control = None

        super(ProgressDialog, self).close()

    #-------------------------------------------------------------------------
    # IProgressDialog Interface
    #-------------------------------------------------------------------------

    def change_message(self, value):
        """ Change the displayed message in the progress dialog

        Parameters
        ----------
        message : str or unicode
            The new message to display.

        """
        self._message_text = value

        if self._message_control is not None:
            self._message_control.SetLabel(value)
            self._message_control.Update()

            msg_control_size = self._message_control.GetSize()
            self.dialog_size.x = max(self.dialog_size.x, msg_control_size.x + 2*self.margin)
            if self.control is not None:
                self.control.SetClientSize(self.dialog_size)

                self.control.GetSizer().Layout()

    def update(self, value):
        """ Update the progress bar to the desired value

        If the value is >= the maximum and the progress bar is not contained
        in another panel the parent window will be closed.

        Parameters
        ----------
        value :
            The progress value to set.
        """

        if self.progress_bar is None:
            # the developer is trying to update a progress bar which is already
            # done. Allow it, but do nothing
            return (False, False)

        self.progress_bar.update(value)

        # A bit hackish, but on Windows if another window sets focus, the
        # other window will come to the top, obscuring the progress dialog.
        # Only do this if the control is a top level window, so windows which
        # embed a progress dialog won't keep popping to the top
        # When we do embed the dialog, self.control may be None since the
        # embedding might just be grabbing the guts of the control. This happens
        # in the Traits UI ProgressEditor.

        if self.control is not None and self.control.IsTopLevel():
            self.control.Raise()

        if self.max > 0:
            percent = (float(value) - self.min)/(self.max - self.min)

            if self.show_time and (percent != 0):
                current_time = time.time()
                elapsed = current_time - self._start_time
                estimated = elapsed/percent
                remaining = estimated - elapsed

                self._set_time_label(elapsed,
                                 self._elapsed_control)
                self._set_time_label(estimated,
                                 self._estimated_control)
                self._set_time_label(remaining,
                                 self._remaining_control)

            if self.show_percent:
                self._percent_control = "%3f" % ((percent * 100) % 1)

            if value >= self.max or self._user_cancelled:
                self.close()
        else:
            if self._user_cancelled:
                self.close()

        wx.GetApp().Yield(True)

        return (not self._user_cancelled, False)

    #-------------------------------------------------------------------------
    # Private Interface
    #-------------------------------------------------------------------------

    def _on_cancel(self, event):
        self._user_cancelled = True
        self.close()

    def _on_close(self, event):
        self._user_cancelled = True
        return self.close()

    def _set_time_label(self, value, control):
        hours = value / 3600
        minutes = (value % 3600) / 60
        seconds = value % 60
        label = "%u:%02u:%02u" % (hours, minutes, seconds)

        control.SetLabel(label)

    def _get_message(self):
        return self._message_text

    def _create_buttons(self, dialog, parent_sizer):
        """ Creates the buttons. """

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._cancel = None

        if self.can_cancel == True:
            # 'Cancel' button.
            self._cancel = cancel = wx.Button(dialog, wx.ID_CANCEL,
                                              self.cancel_button_label)
            wx.EVT_BUTTON(dialog, wx.ID_CANCEL, self._on_cancel)
            sizer.Add(cancel, 0, wx.LEFT, 10)

            button_size = cancel.GetSize()
            self.dialog_size.x = max(self.dialog_size.x, button_size.x + 2*self.margin)
            self.dialog_size.y += button_size.y + 2*self.margin

            parent_sizer.Add(sizer, 0, wx.ALIGN_RIGHT | wx.ALL, self.margin)

    def _create_label(self, dialog, parent_sizer, text):
        local_sizer = wx.BoxSizer()
        dummy = wx.StaticText(dialog, -1, text)
        label = wx.StaticText(dialog, -1, "unknown")

        local_sizer.Add(dummy, 1, wx.ALIGN_LEFT)
        local_sizer.Add(label, 1, wx.ALIGN_LEFT | wx.ALIGN_RIGHT, self.margin)
        parent_sizer.Add(local_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, self.margin)

        return label

    def _create_gauge(self, dialog, parent_sizer):
        self.progress_bar = ProgressBar(dialog, self.min, self.max)
        parent_sizer.Add(self.progress_bar.control, 0, wx.CENTER | wx.ALL, self.margin)

        horiz_spacer = 50

        progress_bar_size = self.progress_bar.control.GetSize()
        self.dialog_size.x = max(self.dialog_size.x, progress_bar_size.x + 2*self.margin + horiz_spacer)
        self.dialog_size.y += progress_bar_size.y + 2*self.margin

    def _create_message(self, dialog, parent_sizer):
        self._message_control = wx.StaticText(dialog, -1, self.message)
        parent_sizer.Add(self._message_control, 0, wx.LEFT | wx.TOP, self.margin)

        msg_control_size = self._message_control.GetSize()
        self.dialog_size.x = max(self.dialog_size.x, msg_control_size.x + 2*self.margin)
        self.dialog_size.y += msg_control_size.y + 2*self.margin

    def _create_percent(self, dialog, parent_sizer):
        if not self.show_percent:
            return

        raise NotImplementedError

    def _create_timer(self, dialog, parent_sizer):
        if not self.show_time:
            return

        self._elapsed_control = self._create_label(dialog, parent_sizer, "Elapsed time : ")
        self._estimated_control = self._create_label(dialog, parent_sizer, "Estimated time : ")
        self._remaining_control = self._create_label(dialog, parent_sizer, "Remaining time : ")

        elapsed_size = self._elapsed_control.GetSize()
        estimated_size = self._estimated_control.GetSize()
        remaining_size = self._remaining_control.GetSize()

        timer_size = wx.Size()
        timer_size.x = max(elapsed_size.x, estimated_size.x, remaining_size.x)
        timer_size.y = elapsed_size.y + estimated_size.y + remaining_size.y

        self.dialog_size.x = max(self.dialog_size.x, timer_size.x + 2*self.margin)
        self.dialog_size.y += timer_size.y + 2*self.margin

    def _create_control(self, parent):
        """ Creates the window contents.

        This method is intended to be overridden if necessary.  By default we
        just create an empty panel.

        """
        style = wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_WINDOW_MENU | wx.CLIP_CHILDREN

        dialog = wx.Frame(parent, -1, self.title, style=style, size=self.size,
                pos=self.position)

        sizer = wx.BoxSizer(wx.VERTICAL)
        dialog.SetSizer(sizer)
        dialog.SetAutoLayout(True)
        dialog.SetBackgroundColour(wx.NullColour)

        self.dialog_size = wx.Size()

        # The 'guts' of the dialog.
        self._create_message(dialog, sizer)
        self._create_gauge(dialog, sizer)
        self._create_percent(dialog, sizer)
        self._create_timer(dialog, sizer)
        self._create_buttons(dialog, sizer)

        dialog.SetClientSize(self.dialog_size)

        dialog.CentreOnParent()

        return dialog
