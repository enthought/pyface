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

from pyface.base_toolkit import Toolkit


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
