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
""" Application window example. """


# Standard library imports.
import os, sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))

# Major package imports.
import wx
import wx.html
import wx.lib.wxpTag

# Enthought library imports.
from pyface.api import ApplicationWindow, GUI, ImageResource, ImageWidget
from pyface.action.api import Action, MenuManager, MenuBarManager


# HTML templates.
HTML = """

<html>
  <body>
    %s
  </body>
</html>

"""

PART = """<wxp module="wx" class="Panel"><param name="id" value="%s"><param name="size" value="(50, 50)"></wxp>"""

class MainWindow(ApplicationWindow):
    """ The main application window. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Creates a new application window. """

        # Base class constructor.
        super(MainWindow, self).__init__(**traits)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(
                Action(name='E&xit', on_perform=self.close),
                name = '&File',
            )
        )

        return

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents.

        This method is intended to be overridden if necessary.  By default we
        just create an empty (and blue!) panel.

        """

        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        N = 100
        wxid = wx.NewId()

        # Create the HTML.
        parts = []
        for i in range(N):
            parts.append(PART % str(wxid+i))

        html = HTML % "".join(parts)

        # Create the HTML window.
        html_window = wx.html.HtmlWindow(panel, -1, style=wx.CLIP_CHILDREN)
        html_window.SetPage(html)

        # Initialize all embedded wx controls.
        for i in range(N):
            self._initialize_window(html_window, wxid+i)

        sizer.Add(html_window, 1, wx.EXPAND)

        # Resize the panel to fit the sizer's minimum size.
        sizer.Fit(panel)

        return panel

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _initialize_window(self, parent, wxid):
        """ Initialize the window with the specified Id. """

        window = parent.FindWindowById(wxid)
        sizer = wx.BoxSizer(wx.VERTICAL)
        window.SetSizer(sizer)
        window.SetAutoLayout(True)

        window.SetBackgroundColour('white')
        window.SetWindowStyleFlag(wx.CLIP_CHILDREN)
        window.Refresh()
        image = ImageResource('closed_folder_24x24')
        bitmap = image.create_image().ConvertToBitmap()

        image_widget = ImageWidget(window, bitmap=bitmap)
        image_widget.control.SetBackgroundColour('white')
        sizer.Add(image_widget.control, 0, wx.EXPAND)

        text = wx.StaticText(window, -1, "Blah", style=wx.ALIGN_CENTRE)
        sizer.Add(text, 0, wx.EXPAND)

        # Resize the window to match the sizer's minimum size.
        sizer.Fit(window)

        return


# Application entry point.
if __name__ == '__main__':
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()

##### EOF #####################################################################
