#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#------------------------------------------------------------------------------

import wx

from traits.trait_notifiers import set_ui_handler, ui_handler

from pyface.base_toolkit import Toolkit
from .gui import GUI


# Check the version number is late enough.
if wx.VERSION < (2, 8):
    raise RuntimeError(
        "Need wx version 2.8 or higher, but got %s" % str(wx.VERSION)
    )


# It's possible that it has already been initialised.
_app = wx.GetApp()
if _app is None:
    _app = wx.App()


# stop logging to a modal window by default
# (apps can override by setting a different active target)
_log = wx.LogStderr()
wx.Log.SetActiveTarget(_log)


# create the toolkit object
toolkit_object = Toolkit('pyface', 'wx', 'pyface.ui.wx')


# ensure that Traits has a UI handler appropriate for the toolkit.
if ui_handler is None:
    # Tell the traits notification handlers to use this UI handler
    set_ui_handler(GUI.invoke_later)
