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

# Standard library imports.
import sys

# Enthought library imports.
from enthought.etsconfig.api import ETSConfig


# Get the toolkit agnostic parts of the API.
from constant import OK, CANCEL, YES, NO
from key_pressed_event import KeyPressedEvent
from widget import IWidget, MWidget
from window import IWindow, MWindow


def _init_toolkit():
    """ Initialise the current toolkit. """

    # Toolkits to check for if none is explicitly specified.
    known_toolkits = ('wx', 'qt4')

    # Get the toolkit.
    toolkit = ETSConfig.toolkit

    if toolkit:
        toolkits = (toolkit, )
    else:
        toolkits = known_toolkits

    for tk in toolkits:
        # Import the toolkit's pyface backend's API.
        api = 'enthought.pyface.ui.%s.api' % tk

        try:
            __import__(api)
            break
        except ImportError:
            pass
    else:
        if toolkit:
            raise ImportError, "unable to import a pyface backend for the %s toolkit" % toolkit
        else:
            raise ImportError, "unable to import a pyface backend for any of the %s toolkits" % ", ".join(known_toolkits)

    # In case we have just decided on a toolkit, tell everybody else.
    ETSConfig.toolkit = tk

    # Update this module with the backend's API.
    mdict = sys.modules[__name__].__dict__

    for k, v in sys.modules[api].__dict__.iteritems():
        if not k.startswith('_'):
            mdict[k] = v


# Get the toolkit specific parts of the API then disappear.
_init_toolkit()
del _init_toolkit


# The rest of this module handles widgets that are wx specific or those that
# use the ETS v2.x method of doing toolkit selection (which was never properly
# used because we decided to break backwards compatibility and do it better in
# ETS v3.x).  This will all be removed when everything has been ported to v3.x
# and pyface becomes toolkit agnostic.

try:
    import wx
    
    # Application window needs these (for the toolbar manager).
    from image_cache import ImageCache

    from about_dialog import AboutDialog
    from application_window import ApplicationWindow
    from background_progress_dialog import BackgroundProgressDialog
    from confirmation_dialog import ConfirmationDialog, confirm
    from dialog import Dialog
    from directory_dialog import DirectoryDialog
    from expandable_panel import ExpandablePanel
    from file_dialog import FileDialog
    from filter import Filter
    from gui import GUI
    from heading_text import HeadingText
    from image_resource import ImageResource
    from image_widget import ImageWidget
    from layered_panel import LayeredPanel
    from mdi_application_window import MDIApplicationWindow
    from mdi_window_menu import MDIWindowMenu
    from message_dialog import MessageDialog, error, information, warning
    from multi_toolbar_window import MultiToolbarWindow
    from python_editor import PythonEditor
    from python_shell import PythonShell
    from single_choice_dialog import SingleChoiceDialog
    from sorter import Sorter
    from splash_screen import SplashScreen
    from split_application_window import SplitApplicationWindow
    from split_dialog import SplitDialog
    from split_panel import SplitPanel
    from system_metrics import SystemMetrics

    # Fix for broken Pycrust introspect module.
    import util.fix_introspect_bug

except ImportError:
    # Application window needs these (for the toolbar manager).
    from image_cache import ImageCache

    from about_dialog import AboutDialog
    from application_window import ApplicationWindow
    from confirmation_dialog import ConfirmationDialog, confirm
    from dialog import Dialog
    from directory_dialog import DirectoryDialog
    from file_dialog import FileDialog
    from gui import GUI
    from image_resource import ImageResource
    from message_dialog import MessageDialog, error, information, warning
    from python_shell import PythonShell
    from splash_screen import SplashScreen
    from system_metrics import SystemMetrics
