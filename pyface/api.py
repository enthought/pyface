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

from __future__ import absolute_import

from .about_dialog import AboutDialog
from .application_window import ApplicationWindow
from .beep import beep
from .clipboard import clipboard, Clipboard
from .confirmation_dialog import confirm, ConfirmationDialog
from .constant import OK, CANCEL, YES, NO
from .dialog import Dialog
from .directory_dialog import DirectoryDialog
from .file_dialog import FileDialog
from .filter import Filter
from .gui import GUI
from .heading_text import HeadingText
from .image_cache import ImageCache
from .image_resource import ImageResource
from .key_pressed_event import KeyPressedEvent
from .message_dialog import error, information, warning, MessageDialog
from .progress_dialog import ProgressDialog
from .python_editor import PythonEditor
from .python_shell import PythonShell
from .sorter import Sorter
from .splash_screen import SplashScreen
from .split_application_window import SplitApplicationWindow
from .split_dialog import SplitDialog
from .split_panel import SplitPanel
from .system_metrics import SystemMetrics
from .window import Window
from .widget import Widget


###############################################################################
# This part of the module handles widgets that are still wx specific.  This
# will all be removed when everything has been ported to PyQt and pyface
# becomes toolkit agnostic.
###############################################################################

from traits.etsconfig.api import ETSConfig
if ETSConfig.toolkit == 'wx':
    from .expandable_panel import ExpandablePanel
    from .image_widget import ImageWidget
    from .layered_panel import LayeredPanel
    from .mdi_application_window import MDIApplicationWindow
    from .mdi_window_menu import MDIWindowMenu
    from .multi_toolbar_window import MultiToolbarWindow
    from .single_choice_dialog import SingleChoiceDialog

    # Fix for broken Pycrust introspect module.
    from .util import fix_introspect_bug

del ETSConfig
