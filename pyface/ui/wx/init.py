# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import wx

from traits.trait_notifiers import set_ui_handler, ui_handler

from pyface.base_toolkit import Toolkit
from .gui import GUI

# It's possible that it has already been initialised.
_app = wx.GetApp()
if _app is None:
    _app = wx.App()


# stop logging to a modal window by default
# (apps can override by setting a different active target)
_log = wx.LogStderr()
wx.Log.SetActiveTarget(_log)


# create the toolkit object
toolkit_object = Toolkit("pyface", "wx", "pyface.ui.wx")


# ensure that Traits has a UI handler appropriate for the toolkit.
if ui_handler is None:
    # Tell the traits notification handlers to use this UI handler
    set_ui_handler(GUI.invoke_later)

# Fix for broken Pycrust introspect module.  Imported to patch pycrust.
# CJW: is this still needed? Has been in for years.
from pyface.util import fix_introspect_bug  # noqa: F401, E402
